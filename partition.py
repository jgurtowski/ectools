#!/usr/bin/env python

import sys
import os
from seqio import iteratorFromExtension

if not len(sys.argv) == 4:
    print "partition.py <reads_per_file (int)> <files_per_dir (int)> <input.{fa,fq}>"
    sys.exit(1)

def pstr(num):
    return "%04d" % num

rpf = int(sys.argv[1])
fpd = int(sys.argv[2])
in_fn = sys.argv[3]
seqIt = iteratorFromExtension(in_fn)
fa_fh = open(sys.argv[3])

total_reads = 0
dnum = 0
fnum = 0
fh = None
readidx_fh = open("ReadIndex.txt", "w")

for record in seqIt(fa_fh):
    if total_reads % rpf == 0:
        if total_reads % (rpf * fpd) == 0:
            dnum += 1
            fnum = 0
            os.mkdir(pstr(dnum))
        fnum += 1
        if fh:
            fh.close()
        current_file ="%s/p%s" % (pstr(dnum),pstr(fnum))
        fh = open(current_file, "w") 

    clean_name = str(record.name).split()[0]
    readidx_fh.write(clean_name +"\t" + current_file + "\n")
    fh.write(">"+clean_name+"\n")
    fh.write(str(record.seq)+"\n")

    total_reads += 1

readidx_fh.close()
fh.close()
fa_fh.close()
