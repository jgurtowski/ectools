#!/usr/bin/env python

import sys
import os
from itertools import starmap, chain

from seqio import iteratorFromExtension, recordToString, fastaRecordToString, seqlen
from nucio import fileIterator
from args import parseArgs, getHelpStr, argflag, CLArgument

description = ("Usage: partition.py [-options] "
               "<reads_per_file (int)> <files_per_dir (int)> <input.{fa,fq}> [input2.{fa,fq} ...]")

argument_list = [["sameformat", "samefmt", argflag, False,
                  ("Output files will be in the same format "
                   "as the input files. By default they are converted "
                   "to fasta.")],
                 ["minlen", "minlen", int, 1,
                  ("Only output reads that are greater than or equal to 'minlen' "
                   "Default: 1")]]

arguments = map(CLArgument._make, argument_list)

if not len(sys.argv) > 1:
    sys.exit(getHelpStr(description,arguments) + "\n")

(p_arg_map, args_remaining) = parseArgs(sys.argv[1:], arguments)

if not len(args_remaining) >= 3:
    sys.exit(getHelpStr(description,arguments) + "\n")

def pstr(num):
    return "%04d" % num

(rpf,fpd) = map(int,args_remaining[:2])

in_files = args_remaining[2:]
input_data = chain.from_iterable(starmap(fileIterator,
                                         zip(in_files, map(iteratorFromExtension, in_files))))

total_reads = 0
dnum = 0
fnum = 0
fh = None
readidx_fh = open("ReadIndex.txt", "w")

recordString = recordToString if p_arg_map["samefmt"] else fastaRecordToString

for record in input_data:

    if seqlen(record) < p_arg_map["minlen"]:
        continue

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
    clean_record = record._replace(name=clean_name)
    readidx_fh.write(clean_name +"\t" + current_file + "\n")
    
    fh.write(recordString(clean_record))
    fh.write("\n")

    total_reads += 1

readidx_fh.close()
fh.close()

