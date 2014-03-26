#!/usr/bin/env python

#Downsample a library
import sys

from nucio import typeify, fileIterator
from seqio import iteratorFromExtension, recordToString, seqlen



if not len(sys.argv) == 5:
    sys.exit("Usage: downsample.py genome_size desired_cov input.{fa,fq} output.{fa,fq}\n")


types = [int, float, str, str]
sysins = sys.argv[1:len(types)+1]
(genome_size, target_cov, infn, outfn) =  typeify(sysins,types)

max_bases = genome_size * target_cov 
total_bases = 0

with open(outfn, "w") as of:
    for record in fileIterator(infn,iteratorFromExtension(infn)):
        length = seqlen(record)
        if "N" in record.seq:
            continue
        if total_bases > max_bases:
            break
        of.write(recordToString(record))
        of.write("\n")
        total_bases += length
    
