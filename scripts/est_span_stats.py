#!/usr/bin/env python

##estimate the spanning statistics
# For a certain size region how
# probable is it that we have a read
# that spans it

import sys

from nucio import M4Record, M4RecordTypes
from nucio import fileIterator, lineRecordIterator

if not len(sys.argv) == 2:
    sys.exit("est_span_stats.py in.m4")


itemIterator = lambda f : lineRecordIterator(f, M4Record, M4RecordTypes)

#just read alignments into memory
alignments = list(fileIterator(sys.argv[1], itemIterator))








