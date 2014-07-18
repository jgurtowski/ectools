#!/usr/bin/env python

import sys

from collections import namedtuple
from math import fabs

from nucio import getDeltaAlignmentIterator, deltaRecordToOriginalFormat
from nucio import deltaRecordHeaderToString, deltaAlignmentHeaderToString

if not len(sys.argv) == 6:
    sys.exit("pre_delta_filter.py in.delta wiggle_pct contained_pct min_alignment_size out_file")

def alignment_is_good(record, a, arange):
    trimmed_slen = arange.end - arange.start    
    if trimmed_slen < 0:
        sys.exit("BUG: trimmed_slen bad value\n")

    qury_wiggle = record.qlen * WIGGLE_PCT

    if not fabs(a.send - a.sstart) > MIN_ALIGNMENT_SIZE:
        return False
    
    #pb read contained in utg
    if( fabs(a.send - a.sstart) >= (trimmed_slen * CONTAINED_PCT) and
        record.qlen > record.slen):
        return True
     
    #utg contained
    if( fabs(a.qend - a.qstart) > (record.qlen * CONTAINED_PCT) and
          record.slen > record.qlen):
        return True

    #else proper overlap off end of pb read
    if( (a.sstart == arange.start or arange.end == a.send) and
          (a.qstart < qury_wiggle or a.qend < qury_wiggle or
           (record.qlen - a.qstart) < qury_wiggle or (record.qlen - a.qend) < qury_wiggle)):
        return True
    
    return False


AlignmentRange = namedtuple('AlignmentRange',["start","end"])

WIGGLE_PCT = float(sys.argv[2])
CONTAINED_PCT = float(sys.argv[3])
MIN_ALIGNMENT_SIZE = int(sys.argv[4])

outfilename = sys.argv[5]

fh = open(sys.argv[1])

delta_header = fh.readline() + fh.readline().strip()

#read all alignments into memory,
#could be bad for large delta files
deltaHash={}
for record in getDeltaAlignmentIterator(fh):
    if not deltaHash.has_key(record.sname):
        deltaHash[record.sname] = []
    deltaHash[record.sname].append(record)
fh.close()

#figure out the first and last alignment of each
#pb read, so we can trim.
#populate readRange with 
#key: readname
#value: tuple(start,end)
readRange = {}
for readname, drecord_list in deltaHash.iteritems():
    (start,end) = (drecord_list[0].slen, 0)
    for drecord in drecord_list:
        for alignment in drecord.alignments:
            l = min(alignment.sstart,alignment.send)
            if l < start:
                start = l
            r = max(alignment.sstart,alignment.send)
            if r > end:
                end = r
    readRange[readname] = AlignmentRange(start,end)

ofh = open(outfilename, "w")
efh = open(outfilename+".log", "w")

ofh.write(delta_header)
ofh.write("\n")
for readname,drecord_list in deltaHash.iteritems():
    alignment_range = readRange[readname]
    for record in drecord_list:
       #get alignments that pass basic filtering
        pfalignments = []
        for alnmt in record.alignments:
            if alignment_is_good(record, alnmt, alignment_range):
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

efh.close()
ofh.close()

