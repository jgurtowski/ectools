#!/usr/bin/env python

## takes an m4 file and a region chrx:start-end
## and finds all alignments that intersect that region

import sys

from itertools import ifilter, imap

from nucio import lineRecordIterator, fileIterator
from nucio import M4Record, M4RecordTypes, recordToString

if not len(sys.argv) == 3:
    sys.exit("region.py in.m4 chr:start-end")

inm4 = sys.argv[1]
(chrom, rest) = sys.argv[2].split(":")
(start,end) = map(int,rest.split("-"))

it = lambda fh : lineRecordIterator(fh, M4Record, M4RecordTypes)

cond = lambda r : r.tname == chrom and not r.tend < start and not r.tstart > end

filt_records = ifilter(cond,fileIterator(inm4, it))

for r in imap(recordToString, filt_records):
    print r





