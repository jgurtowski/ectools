#!/usr/bin/env python

import sys
import os

from itertools import starmap, chain, ifilter, imap
from seqio import iteratorFromExtension, seqlen, recordToString
from nucio import fileIterator

if not len(sys.argv) > 2:
    sys.exit("length_filter.py min_length(int) in1.{fa,fq} [in2.{fa,fq} ...]\n")

minlen = int(sys.argv[1])

files = sys.argv[2:]

if not all(map(os.path.exists,files)):
    sys.exit("Not all files exist")

file_readers = starmap(fileIterator, zip(files, map(iteratorFromExtension, files)))

filt_cond = lambda record : seqlen(record) > minlen

filtered_records = ifilter(filt_cond, chain.from_iterable(file_readers))

filtered_seqs = imap(recordToString, filtered_records)

for seq in filtered_seqs:
    print seq


