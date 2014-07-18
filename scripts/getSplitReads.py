#!/usr/bin/env python


##
#Attempts to print split reads from m4 file
##



import sys
from m4io import getAlignments, longestNonOverlapping
from nucio import recordToString

if not len(sys.argv) == 2:
    sys.exit("getSplitReads.py in.m4")


inm4 = sys.argv[1]

for read,alignments in getAlignments(inm4, longestNonOverlapping):
    if len(alignments) > 1:
        astrings = map(recordToString, alignments)
        print "\n".join(astrings)
