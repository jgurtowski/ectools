#!/usr/bin/env python

#Deplexes combined pb reads into 1 file per smrtcell

import sys

from itertools import starmap,izip,chain

from seqio import iteratorFromExtension, fastaRecordToString
from nucio import fileIterator

if not len(sys.argv) >= 2:
    sys.exit("deplex_pb.py in.{fa,fq} [in2.{fa,fq} ..]\n")

files = sys.argv[1:]
its = map(iteratorFromExtension, files)

file_its = starmap(fileIterator, izip(files,its))


fh_h = {}

for entry in chain.from_iterable(file_its):
    h = entry.name.split("/")[0]
    if not h in fh_h:
        fh_h[h] = open(h+".fa","w")
    fh_h[h].write(fastaRecordToString(entry))
    fh_h[h].write("\n")
            
