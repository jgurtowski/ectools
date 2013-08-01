#!/usr/bin/env python

import sys
from itertools import groupby,ifilter,izip_longest,count

from io import getNucmerAlignmentIterator
from cov import fillc, getMarkedRanges, getCoverageFromNucAlignments

if not len(sys.argv) == 4:
    print "pb_uncovered.py <in.nuc.sc> <min_gap> <out_prefix>"
    sys.exit(1)

fh = open(sys.argv[1])

COV_GAP_MIN = int(sys.argv[2])

fhist = open(sys.argv[3] + ".uncov.hist", "w")
freg = open(sys.argv[3] + ".uncov.regions", "w")
ftbases = open(sys.argv[3] + ".uncov.total.bases", "w")

pcov = [] #pct cov

total_bases = 0
total_uncovered_bases = 0

for pbname,alignments in groupby(getNucmerAlignmentIterator(fh), lambda x: x.sname):
    a = list(alignments)
    cov = getCoverageFromNucAlignments(a)

    #mark the 0 coverage regions
    zcov = map(lambda c: 1 if c == 0 else 0, cov)
    
    #ranges with 0 coverage
    zcov_ranges = getMarkedRanges(zcov)
    
    #only look at the gaps larger than the min gap size
    zcov_ranges_filt = filter(lambda (x,y) : y-x > COV_GAP_MIN ,zcov_ranges )

    #write out the regions that pass filter to region file
    freg.write("\t".join([pbname, " ".join(map(lambda t: "%d,%d" % t, zcov_ranges_filt))]) + "\n")

    total_bases += a[0].slen
    for rbeg,rend in zcov_ranges_filt:
        total_uncovered_bases += rend - rbeg
    
    pct_ranges = map(lambda (rb,re) : (int(float(rb)/(a[0].slen-1)*100),int(float(re)/(a[0].slen-1)*100)), zcov_ranges_filt)
    
    for pr_b,pr_e in pct_ranges:
        fillc(pcov,pr_b,pr_e) 

ftbases.write("%d / %d = %f\n" % (total_uncovered_bases,total_bases, float(total_uncovered_bases)/total_bases))

#print nicely
map(lambda t: fhist.write("%d\t%d\n" % t), izip_longest(range(100),pcov,fillvalue=0))


fh.close()
fhist.close()
freg.close()
ftbases.close()
    
    
    

