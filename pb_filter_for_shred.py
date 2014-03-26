#!/usr/bin/env python

#If the illumina unitigs are very long,
#ie. the average unitig is longer than the
#average pb read, might want to shred the unitigs
#and filter out pb reads that are contained in
#those long unitigs.

#This script probably does that.
#It takes the show-coords output and
#marks which pb reads should be kept

import sys
from nucio import getNucmerAlignmentIterator, nucRecordToString

from itertools import groupby, imap, izip, starmap
from operator import attrgetter, eq
from misc import append_str

if not len(sys.argv) > 1:
    print "pb_filter_for_shred.py all.sc [significant_alignment_length(int)(default:200)]"
    sys.exit(1)

#length of alignment to label "significant"
SIG_ALN_LEN = 200
if len(sys.argv) > 2:
    SIG_ALN_LEN = int(sys.argv[2])

afh = open(sys.argv[1])
alignment_it = getNucmerAlignmentIterator(afh)

for pbname, alignment in groupby(alignment_it, lambda x : x.sname):
    status = "KEEP"
    message = "DEFAULT"
    raw_alignments = list(alignment)

    al_list = filter(lambda al: al.qalen >= SIG_ALN_LEN,raw_alignments)
    utg_list = map(attrgetter("qname"), al_list)

    if all(starmap( eq, izip(utg_list[:-1],utg_list[1:]))):
        status = "REMOVE"
        message = "ALL ALIGNMENTS TO A SINGLE UTG"
            
    print "\n".join(
        imap(append_str("\t"+"\t".join([status,message])),
             imap(nucRecordToString,raw_alignments)))
    
