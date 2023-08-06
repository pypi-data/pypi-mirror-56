from __future__ import print_function, division, absolute_import, with_statement

import sys
import os
import shutil
from array import array
from collections import namedtuple

Batch = namedtuple('Batch', ['chr', 'fastas', 'output_folder'])
nucleotide_complements = {'A': 'T', 'G': 'C', 'T': 'A', 'C': 'G', 'N': 'N', 'X': 'X'}


def complement(plus_strand):
    return nucleotide_complements[plus_strand]


def rev_comp(plus_strand):
    return ''.join([nucleotide_complements[a] for a in reversed(plus_strand)])


class ReverseComplement(object):
    def __init__(self, seq, annotation=False):
        """Lazy generator for being able to pull out small reverse complement
        sections out of large chromosomes"""
        self.seq = seq
        self.length = len(seq)
        self.annotation = annotation

    def __getitem__(self, key):
        if isinstance(key, slice):
            end = self.length - key.start
            begin = self.length - key.stop
            if end < 0 or begin < 0 or end > self.length:
                raise IndexError("%i %i vs. length %i" % (end, begin, self.length))
            piece = self.seq[begin: end]
            return rev_comp(piece) if not self.annotation else ''.join(reversed(piece))
        letter = self.seq[self.length - key - 1]
        return complement(letter) if not self.annotation else letter

    def __len__(self):
        return 0


def pp(variable):
    """Short method for formatting output in the way I like it using duck typing"""
    rep = variable
    if isinstance(variable, int):
        rep = '{:,}'.format(variable)
    elif isinstance(variable, float):
        if 2.0 > variable > .00001:
            rep = '{:%}'.format(variable)
        elif variable > 2.0:
            rep = '{:.3}'.format(variable)
    return rep


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        import errno
        try:
            os.makedirs(dst)
        except OSError as e:  # exist_ok=True
            if e.errno != errno.EEXIST:
                raise
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


def chunks(seq, size):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def first_word(string):
    import re
    string = os.path.basename(string)
    return re.split('[\W_]+', string)[0]


class BlankIterator(object):
    def __init__(self, filler):
        self.filler = filler

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.filler * (index.stop - index.start)
        else:
            return self.filler


def editable_str(initial_str):# -> array
    """Exactly the same as array.array except that it switches types based on Python Version:
    Python 2: character, one byte
    Python 3: unicode, two to four bytes"""
    array_type = 'u'
    if sys.version_info < (3, 0):
        array_type = 'c'
    return array(array_type, initial_str)


def first(iterable):
    if isinstance(iterable, dict):
        return next(iter(iterable.items()))
    return next(iter(iterable))


class LoopList(list):
    def __getitem__(self, index):
        index = index % len(self)
        return super(LoopList, self).__getitem__(index)



