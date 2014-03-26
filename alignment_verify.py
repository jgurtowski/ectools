#!/usr/bin/env python

import sys
from nucio import getNucmerAlignmentIterator, nucRecordToString
from itertools import groupby
from operator import attrgetter

#dist from the end 
#that is considered in the middle
END_CUTOFF =  200

if not len(sys.argv) == 2:
    sys.exit("alignment_verify.py alignments.sc")

fh = open(sys.argv[1])


for pbname, alignments in groupby(getNucmerAlignmentIterator(fh), attrgetter("sname")):
    al = list(alignments)

    ##if all alignments are to the same unitig
    if all(map(lambda x: x.qname == al[0].qname , al)):
        continue
    
    for aln in al:
        if (aln.qstart > END_CUTOFF and aln.qstart < (aln.qlen-END_CUTOFF) 
            and aln.qend > END_CUTOFF and aln.qend < (aln.qlen-END_CUTOFF)):
            print nucRecordToString(aln)+"\tMIDDLE"
        else:
            print nucRecordToString(aln)

fh.close()    
