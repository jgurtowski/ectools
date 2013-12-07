#!/usr/bin/env python

import sys

from math import fabs

from io import getDeltaAlignmentIterator, deltaRecordToOriginalFormat
from io import deltaRecordHeaderToString, deltaAlignmentHeaderToString



def alignment_is_good(record, a):
    
    subj_wiggle = record.slen * WIGGLE_PCT
    qury_wiggle = record.qlen * WIGGLE_PCT

    if not fabs(a.send - a.sstart) > MIN_ALIGNMENT_SIZE:
        return False
    
    #pb read contained in utg
    if( fabs(a.send - a.sstart) > (record.slen * CONTAINED_PCT) and
        record.qlen > record.slen):
        return True
     
    #utg contained
    if( fabs(a.qend - a.qstart) > (record.qlen * CONTAINED_PCT) and
          record.slen > record.qlen):
        return True

    #else proper overlap off end of pb read
    if( (a.sstart < subj_wiggle or (record.slen-a.send) < subj_wiggle) and
          (a.qstart < qury_wiggle or a.qend < qury_wiggle or
           (record.qlen - a.qstart) < qury_wiggle or (record.qlen - a.qend) < qury_wiggle)):
        return True
    
    return False

if not len(sys.argv) == 6:
    sys.exit("pre_delta_filter.py in.delta wiggle_pct contained_pct min_alignment_size out_file")

WIGGLE_PCT = float(sys.argv[2])
CONTAINED_PCT = float(sys.argv[3])
MIN_ALIGNMENT_SIZE = int(sys.argv[4])

outfilename = sys.argv[5]
ofh = open(outfilename, "w")
efh = open(outfilename+".log", "w")

fh = open(sys.argv[1])

delta_header = fh.readline() + fh.readline().strip()

ofh.write(delta_header)
ofh.write("\n")
for record in getDeltaAlignmentIterator(fh):

    #get alignments that pass basic filtering
    pfalignments = []
    for alnmt in record.alignments:
        if alignment_is_good(record, alnmt):
            pfalignments.append(alnmt)
        else:
            efh.write("Remove Alignment:\n")
            efh.write(deltaRecordHeaderToString(record) + "\n")
            efh.write(deltaAlignmentHeaderToString(alnmt)+ "\n")
            
    #0 or 1 alignments, good to go! Otherwise idk
    #just log them and output them anyway
    if len(pfalignments) > 1:
        efh.write("Multiple Alignments\n")
        efh.write(deltaRecordHeaderToString(record) + "\n")
        for a in pfalignments:
            efh.write(deltaAlignmentHeaderToString(a)+ "\n")

    #substitute old alignments with filtered ones
    record.alignments[:] = [] 
    for al in pfalignments:
        record.alignments.append(al)
    
    #delta spec only outputs record if there are alignments
    if(len(record.alignments) > 0):
        ofh.write( deltaRecordToOriginalFormat(record))
        ofh.write("\n")

fh.close()
efh.close()
ofh.close()

