"""
**__utils__** private module to handle sequence data
**Copyright** 2019  Jose Sergio Hleap

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

E-mail: jshleap@squalus.org
"""
import gzip
import os
import shelve
from itertools import zip_longest
from subprocess import run, PIPE, CalledProcessError
from typing import Optional, Iterator, Tuple

import matplotlib.pyplot as plt
import numpy as np
from joblib import Parallel, delayed
from psutil import virtual_memory
from tqdm import tqdm

plt.style.use('ggplot')


def stdin_run(args: list, inpt: Optional[str], env=None,
              **kwargs) -> Tuple[bytes, str]:
    if env is None:
        env = {}
    if inpt is None:
        exe = run(args, stderr=PIPE, stdout=PIPE, env=env, **kwargs)
    else:
        inpt = inpt.encode('utf-8') if isinstance(inpt, str) else input
        exe = run(args, input=inpt, stderr=PIPE, stdout=PIPE, env=env,
                  **kwargs)
    try:
        exe.check_returncode()
    except CalledProcessError:
        raise Exception(exe.stdout, exe.stderr)
    return exe.stdout


class FastX(object):
    """
    Class to handle a fast* files
    """
    h5 = None
    ids = np.array([], dtype=object)
    lengths = np.array([], dtype=int)
    shelve_name = None
    cpus = -1
    bigfile = False

    def __init__(self, filename: str, trimm: Optional[int] = None,
                 outprefix: str = None, cpus: int = -1) -> None:
        """
        FastX constructor
        :param filename: Name of sequence file
        :param trimm: Trim sequence up to this value
        :param outprefix: Prefix or output
        """
        self.filename = filename
        self.trimm = trimm
        self.tipo = filename
        self.outprefix = outprefix
        self.populate()

    def __str__(self):
        return '\n'.join(self.yield_seq(as_fasta=self.tipo == 'a'))

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, filename: str) -> None:
        try:
            with gzip.open(filename, 'rb') as fi:
                line = fi.readline().decode('utf-8')
                self.open = gzip.open
        except OSError:
            with open(filename) as fi:
                line = fi.readline()
                self.open = open
        if line.startswith('>'):
            self._tipo = 'a'
        elif line.startswith('@'):
            self._tipo = 'q'
        else:
            raise Exception("Not an acceptable file format")

    @property
    def outprefix(self):
        return self._outprefix

    @outprefix.setter
    def outprefix(self, out: str) -> None:
        if out is None:
            out = self.filename[: self.filename.rfind('.')]
        self._outprefix = out

    def populate(self):
        if self.tipo == 'a':
            self.parse_fasta(self.filename)
        else:
            self.parse_fastq(self.filename)

    def yield_seq(self, as_fasta: bool = True) -> Iterator[str]:
        with shelve.open(self.shelve_name) as f:
            for name in self.ids:
                if as_fasta:
                    seq = '>%s\n%s' % (name, f[name][0])
                else:
                    seq = '@%s\n%s\n+\n%s' % (name, f[name][0], f[name][0])
                yield seq

    def parse_fastq(self, file_name: str) -> None:
        self.shelve_name = '%s.shelf' % self.outprefix
        with self.open(file_name) as handle:
            file_size = os.fstat(handle.fileno()).st_size / (
                    1024 * 1024 * 1024)
            avail_mem = virtual_memory().available / (1024 * 1024 * 1024)
            if file_size <= avail_mem:
                shelf = {}
            else:
                shelf = shelve.open(self.shelve_name)
                self.bigfile = True
            args = [iter(handle)] * 4
            if not os.path.isfile('%s.shelve' % self.outprefix):
                aln = Parallel(n_jobs=self.cpus, prefer="threads")(
                    delayed(self.run_parser_fastq)(chunk, self.trimm, shelf)
                    for chunk in tqdm(zip_longest(*args, fillvalue=None),
                                      desc="Parsing %s" % file_name))
                self.ids, self.lengths = zip(*aln)
            if self.bigfile:
                shelf.close()

    @staticmethod
    def run_parser_fastq(chunk, trimm, shelf):
        name = chunk[0].decode('utf-8').strip() if isinstance(
            chunk[0], bytes) else chunk[0].strip()[1:]
        seq = chunk[1].decode('utf-8').strip() if isinstance(
            chunk[1], bytes) else chunk[0].strip()
        seq = seq if trimm is None else seq[:trimm]
        qual = chunk[3].decode('utf-8').strip() if isinstance(
            chunk[3], bytes) else chunk[0].strip()
        shelf[name] = (seq, qual)
        return name, len(seq)

    def parse_fasta(self, file_name: str) -> None:
        name, seq = None, ''
        fn = file_name[: file_name.rfind('.')]
        self.shelve_name = '%s.shelf' % fn
        with shelve.open(self.shelve_name) as shelf, self.open(
                file_name) as handle:
            for line in tqdm(handle, desc="Parsing %s" % file_name):
                line = line.decode('utf-8').strip() if isinstance(
                    line, bytes) else line.strip()
                if line.startswith(">"):
                    if name:
                        seq = seq if self.trimm is None else seq[:self.trimm]
                        shelf[name] = (seq, None)
                        self.ids = np.append(self.ids, name)
                    name = line[1:]
                    seq = ''
                else:
                    seq += line
            if name:
                seq = seq if self.trimm is None else seq[:self.trimm]
                shelf[name] = (seq, '')
                self.ids = np.append(self.ids, name)

    def write(self, fasta: bool = True) -> None:
        if fasta:
            self.tipo = 'a'
            outfile = '%s.fasta' % self.outprefix
        else:
            self.tipo = 'q'
            outfile = '%s.fastq.gz' % self.outprefix
        with self.open(outfile, 'w') as out:
            out.write(str(self))

    def plot_length(self):
        plt.xlabel('Length')
        plt.ylabel('Counts')
        plt.title('Sequence length of %s' % self.filename)
        plt.hist(self.lengths, bins=20)
        plt.grid(True)
        plt.savefig('%s.pdf' % self.outprefix)


if __name__ == '__main__':
    print('just a utility module')
