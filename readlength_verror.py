#!/usr/bin/env python

##
#Script just scans blasr (m4) output
#and graphs the difference between
#the original read length and the 
#aligned read length for buckets of
#read length
##

import sys
from itertools import starmap
from operator import div
from m4io import getAlignments, longestNonOverlapping

if not len(sys.argv) == 2:
    sys.exit("readlength_verror.py in.m4")

binsize = 1000
inm4 = sys.argv[1]

bins = {}

for read,alignments in getAlignments(inm4, longestNonOverlapping):
    a0 = alignments[0]
    bin = a0.qseqlength / binsize
    readlen = a0.qseqlength
    bases_lost = readlen - sum(map( lambda a : a.qend - a.qstart, alignments))
    prev = bins.get(bin, (0.0,0.0,0) )
    bins[bin] = (prev[0] + bases_lost, prev[1] + readlen, prev[2] + 1)
    
data =  map(lambda (k,v) : (k, (v[0]/v[1], v[2])) ,bins.iteritems())


for bin, values in data:
    print "\t".join(map(str,[bin,values[0],values[1]]))

