#!/usr/bin/env python

#Takes novoalign native output
#and tries to find good pairs
#as well as report some stats

#novo align is nice and outputs
#a record for every read so
#the pairs should be in the same
#order in both files

import sys

from itertools import ifilter, izip
from functools import partial
from operator import itemgetter

import numpy as np

from nucio import fileIterator, lineItemIterator

MAPQ_THRESH = 30

#novoalign output has a varying number of columns
#just use hard coded indicies rather than named tuples
name = itemgetter(0)
seq = itemgetter(2)
qual = itemgetter(3)
status = itemgetter(4)
ascore = itemgetter(5)
aqual = lambda r : int(itemgetter(6)(r))
ref = itemgetter(7)
pos = lambda r : int(itemgetter(8)(r))
strand = itemgetter(9)

if not len(sys.argv) == 3:
    sys.exit("filterpairs.py read1.novo read2.novo\n")


names_eq = lambda name1,name2: name1.split("/")[0] == name2.split("/")[0]

filenames = sys.argv[1:3]
#filter out header lines
headfilt = lambda x : not x.startswith("#")
filt_lii = partial(lineItemIterator, filter_func=headfilt)

filt_fits = map( lambda fn : fileIterator(fn, filt_lii), filenames)

failrepeat = 0
failmapq = 0
failsameref = 0
total = 0
passed = 0
insertNotRF = []
insertRF = []


for read1,read2 in izip(*filt_fits):
    total += 1
    if not names_eq(name(read1), name(read2)):
        sys.exit("Error: %s not equal to %s\n" % (name(read1),name(read2)))
    
    if not status(read1) == "U" or not status(read2) == "U":
        failrepeat += 1
        continue
    if not aqual(read1) >= MAPQ_THRESH or not aqual(read2) >= MAPQ_THRESH:
        failmapq += 1
        continue
    
    if ref(read1) == ref(read2):
        failsameref += 1
        if not (strand(read1) == "R" and strand(read2) =="F"):
            insertNotRF.append(pos(read2) - pos(read1))
        else:
            insertRF.append(pos(read2) - pos(read1))
        continue

    #just have good pairs print them
    print "\n".join(map("\t".join, [read1,read2]))
    passed += 1

with open("filterpairs.stats", "w") as ofh:
    ofh.write("All numbers are counts of mates: \n")
    ofh.write("One or both reads in repeat or failed to align: %d\n" % failrepeat)
    ofh.write("One or both reads <= mapq %d : %d \n" % (MAPQ_THRESH, failmapq))
    ofh.write("Map to same contig : %d \n" % failsameref)
    ofh.write("Map to different contigs (kept ones): %d of %d : %f\n\n" % (passed, total, float(passed)/total)) 
    ofh.write("Histogram of Mates not in RF orientation \n")
    h = np.histogram(insertNotRF,bins=1000)
    for v,b in zip(*h):
        ofh.write("%d %d\n" % (b,v))
    ofh.write("\n\n")
    ofh.write("Histogram of Mates in RF orientation \n")        
    h = np.histogram(insertRF, bins=1000)
    for v,b in zip(*h):
        ofh.write("%d %d\n" % (b,v))
