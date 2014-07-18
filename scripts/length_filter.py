#!/usr/bin/env python

import sys
import os

from itertools import starmap, chain, ifilter, imap
from seqio import iteratorFromExtension, seqlen, recordToString
from nucio import fileIterator
from args import parseArgs, getHelpStr, CLArgument


description = ("Usage: length_filter.py [options] min_length(int) in1.{fa.fq} [in2.{fa,fq} ...]\n\n"
               "Filter reads by their lengths")

argument_list = [["maxlen", "maxlen", int, -1, "Maximum length of reads"]]

arguments = map(CLArgument._make, argument_list)

if not len(sys.argv) > 2:
    sys.exit(getHelpStr(description, arguments) +"\n")

(p_arg_map, args_remaining) = parseArgs(sys.argv[1:], arguments)


minlen = int(args_remaining[0])

files = args_remaining[1:]

if not all(map(os.path.exists,files)):
    sys.exit("Not all files exist")

file_readers = starmap(fileIterator, zip(files, map(iteratorFromExtension, files)))

filt_cond = lambda record : seqlen(record) > minlen
if p_arg_map["maxlen"] > 1:
    filt_cond = lambda record: seqlen(record) > minlen and seqlen(record) <= p_arg_map["maxlen"]

filtered_records = ifilter(filt_cond, chain.from_iterable(file_readers))

filtered_seqs = imap(recordToString, filtered_records)

for seq in filtered_seqs:
    print seq


