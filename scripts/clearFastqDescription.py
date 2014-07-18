#!/usr/bin/env python

##Clears the fastq description

import sys

from seqio import fastqIterator, fastqRecordToString

if not len(sys.argv) == 2:
    sys.exit("clearFastqDescription.py in.fq\n")


with open(sys.argv[1]) as fh:
    for record in fastqIterator(fh):
        clean_rec = record._replace(desc="")
        print fastqRecordToString(clean_rec)
