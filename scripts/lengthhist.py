#!/usr/bin/env python

import sys
from operator import attrgetter, itemgetter
from itertools import imap

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np

from nucio import lineRecordIterator, M4Record, M4RecordTypes, lineItemIterator
from args import arglist, parseArgs, getHelpStr, CLArgument, argflag

description = ("lengthhist.py [options] title alginments.m4 [alignments2.m4...]\n"
               "Plot Make histograms from alignment (nucmer show-coords) "
               "files")

argument_list = [["labels","labels",arglist,["Ectools","PacbioToCA"], "Labels for each dataset"],
                 ["ymax", "ymax", int, -1, "Maximum Y-value"],
                 ["lenfiles", "lenfiles", int, -1, ("Input files are just a column of lengths, "
                                                    "argument specifies the column")]]

args = map(CLArgument._make, argument_list)

(parg_map, args_remaining) = parseArgs(sys.argv[1:],args)

if not len(args_remaining) >= 3:
    sys.exit(getHelpStr(description,args) + "\n")

title = args_remaining[0]
igetter = attrgetter("qseqlength")

flens = []
for fname in args_remaining[1:]:
    with open(fname) as fh:
        if parg_map["lenfiles"] < 0:
            records = lineRecordIterator(fh, M4Record, M4RecordTypes)
            flens.append( map(igetter, records) )
        else:
            getter = itemgetter(parg_map["lenfiles"])
            flens.append( map(int, imap(getter, lineItemIterator(fh) )))

pp = PdfPages("hist.pdf")
fig = plt.figure()
fig.suptitle(args_remaining[0])
len_binsize = 250

plt.xlabel("Read Length")
plt.ylabel("Frequency")

if parg_map["ymax"] > 0:
    plt.ylim(1,parg_map["ymax"])

labels = parg_map["labels"]
colors = ["red","blue","green","black"]
plt.hist(flens, bins=np.arange(0,50000,len_binsize), histtype='step', color=colors[:len(labels)],label=labels)
plt.legend()

plt.savefig(pp, format="pdf")
    
pp.close()
