#!/usr/bin/env python

##Converts a fasta file
#To fastq by just using 'I' for quality

import sys
from seqio import fastaIterator, FastqRecord, fastqRecordToString


QUAL_STR = "I"

if not len(sys.argv) == 2:
    sys.exit("fastaToFastq.py in.fa \n")

fn = sys.argv[1]

with open(fn) as fh:
    for record in fastaIterator(fh):
        fqr = FastqRecord(record.name, record.seq,
                          "", QUAL_STR * len(record.seq))
        print fastqRecordToString(fqr)
