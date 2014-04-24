#!/usr/bin/env python

## takes an m4 file and a region chrx:start-end
## and finds all alignments that intersect that region

import sys

from itertools import ifilter, imap

from nucio import lineRecordIterator, fileIterator
from nucio import M4Record, M4RecordTypes, recordToString
from args import parseArgs, getHelpStr, argflag, CLArgument

description = ("Usage: m4region.py [options] input.m4 chr:start-end\n"
               "Returns alignments that touch a region\n")

argument_list = [["span","span", argflag, False, "Only alignments that span the region"]]

arguments = map(CLArgument._make, argument_list)

(p_arg_map, args_remaining) = parseArgs(sys.argv[1:], arguments)

if not len(args_remaining) == 2:
    sys.exit(getHelpStr(description,arguments) + "\n")


inm4 = args_remaining[0]
(chrom, rest) = args_remaining[1].split(":")
(start,end) = map(int,rest.split("-"))

it = lambda fh : lineRecordIterator(fh, M4Record, M4RecordTypes)

cond = lambda r : r.tname == chrom and not r.tend < start and not r.tstart > end
if p_arg_map["span"]:
    cond = lambda r : r.tname == chrom and r.tstart < start and r.tend > end

filt_records = ifilter(cond,fileIterator(inm4, it))

for r in imap(recordToString, filt_records):
    print r





