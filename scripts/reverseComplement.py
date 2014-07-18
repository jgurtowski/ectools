#!/usr/bin/env python

import sys

from seqio import iteratorFromExtension, recordToString
from nucio import fileIterator 
from misc import reverse_complement

if not len(sys.argv) == 2:
    sys.exit("reverseComplement.py in.{fa,fq}")

f = sys.argv[1]

for record in fileIterator(f,iteratorFromExtension(f)):
    print recordToString(record._replace(seq=reverse_complement(record.seq)))
