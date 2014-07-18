#!/usr/bin/env

import sys

from seqio import iteratorFromExtension
from nucio import fileIterator

if not len(sys.argv) == 2:
    sys.exit("sequencToLine.py in.{fa.fq}\n")

it = iteratorFromExtension(sys.argv[1])
for record in fileIterator(sys.argv[1], it):
    if hasattr(record, "desc"):
        print "\t".join([record.name, record.seq, record.desc, record.qual])
    else:
        print "\t".join([record.name, record.seq])

