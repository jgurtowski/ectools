#!/usr/bin/env python

import sys

from Bio import SeqIO

if not len(sys.argv) == 2:
    print "qualgen.py read.fa"
    sys.exit(1)

reads = sys.argv[1]

with open(reads) as rfh:
    for record in SeqIO.parse(rfh,"fasta"):
        print ">"+str(record.name)
        print " ".join(["60"]*len(record.seq))
