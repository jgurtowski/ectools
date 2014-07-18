#!/usr/bin/env python

import sys
import operator

from seqio import fastaIterator
from itertools import groupby,izip,imap

from nucio import NucRecord, NucRecordTypes, getNucmerAlignmentIterator
from cov import fillc, getMarkedRanges, getCoverageFromNucAlignments
from gccontent import getGCSlidingWindow

GC_WINDOW_SIZE = 300
GC_THRESHOLD = 0.7
MIN_COV_GAP = 100

if not len(sys.argv) == 4:
    print "gc_count.py reads.fa alignments.sc outprefix"
    sys.exit(1)


rfh = open(sys.argv[1])
afh = open(sys.argv[2])
ofh = open(sys.argv[3]+".uncov.gc.bases","w")

reads = {}

for entry in fastaIterator(rfh):
    reads[str(entry.name)] = str(entry.seq)
sys.stderr.write("Loaded reads\n")

alignmentIt = getNucmerAlignmentIterator(afh)

sys.stderr.write("Loaded Alignments\n");

counter = 0
for name,group in groupby(alignmentIt, lambda x: x.sname):

    #build coverage vector
    cov = getCoverageFromNucAlignments(group)
    
    #mark the regions with 0 (no) coverage as 1 and change
    #everything else to 0
    cov_inv = map(lambda c: 1 if c == 0 else 0, cov)
    
    #ranges with zero coverage
    zero_cov_ranges = getMarkedRanges(cov_inv)
        
    seq = reads[name]

    #calculate GC % for windows of GC_WINDOW_SIZE
    gc_sliding_window = getGCSlidingWindow(seq, GC_WINDOW_SIZE)
    
    #filter gaps that are at > MIN_COV_GAP
    #and have at least one base > GC_THRESHOLD
    #take the sum of the lengths of all of the regions
    gc_gap_bases = sum(map(lambda (s,e): 
                           e-s if e-s > MIN_COV_GAP and any(map(lambda x: True if x > GC_THRESHOLD else False, gc_sliding_window[s:e])) else 0, 
                           zero_cov_ranges))
    
    ofh.write("%s\t%d\n" % (name,gc_gap_bases))
    if counter % 10000 == 0:
        sys.stderr.write("Read num: %d\n" % counter)
    counter += 1

rfh.close()
afh.close()
ofh.close()
