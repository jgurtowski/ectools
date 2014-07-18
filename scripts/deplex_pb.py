#!/usr/bin/env python

#Deplexes combined pb reads into 1 file per smrtcell

import sys

from itertools import starmap,izip,chain

from seqio import iteratorFromExtension, recordToString, FastqRecord
from nucio import fileIterator
from args import parseArgs, getHelpStr, CLArgument

description = ("Usage: deplex_pb.py [options] file1.{fa,fq} [file2.{fa,fq} ..]\n\n"
               "Deplexes a file based on some delimiter")

argument_list = [["delim", "delim", str, "/", "Delimiter to split the input"]]

arguments = map(CLArgument._make, argument_list)

if not len(sys.argv) >= 2:
    sys.exit(getHelpStr(description, arguments) + "\n")

(p_arg_map, args_remaining) = parseArgs(sys.argv[1:], arguments)

its = map(iteratorFromExtension, args_remaining)

file_its = starmap(fileIterator, izip(args_remaining,its))

fh_h = {}

for entry in chain.from_iterable(file_its):
    h = entry.name.split(p_arg_map["delim"])[0]
    ext = ".fastq" if isinstance(entry, FastqRecord) else ".fasta"
    if not h in fh_h:
        fh_h[h] = open(h+ext,"w")
    fh_h[h].write(recordToString(entry))
    fh_h[h].write("\n")
            
