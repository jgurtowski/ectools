#!/usr/bin/env python

#Deplexes combined pb reads into 1 file per smrtcell

import sys

from seqio import fastaIterator, fastaRecordToString

if not len(sys.argv) == 2:
    sys.exit("deplex_pb.py in.fa")

fh_h = {}

with open(sys.argv[1]) as fh:
    for entry in fastaIterator(fh):
        h = entry.name.split("/")[0]
        if not h in fh_h:
            fh_h[h] = open(h+".fa","w")
        fh_h[h].write(fastaRecordToString(entry))
        fh_h[h].write("\n")
            
