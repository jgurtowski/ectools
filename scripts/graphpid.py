#!/usr/bin/env python

import sys
from operator import attrgetter

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np

from nucio import lineRecordIterator,M4Record, M4RecordTypes
from args import parseArgs, getHelpStr, CLArgument

description = ("Usage: graphpid.py [options] title alignments.m4\n\n"
               "Graph Alignments from blasr's m4 output")

argument_list = [["tophist_maxy", "tophist_maxy", int, -1,
                  "Maximum y value for top histogram"]]

arguments = map(CLArgument._make, argument_list)


if not len(sys.argv) > 1:
    sys.exit(getHelpStr(description, arguments) + "\n")

(p_arg_map, args_remaining) = parseArgs(sys.argv[1:], arguments)

if not len(args_remaining) == 2:
    sys.exit(getHelpStr(description, arguments) + "\n")

igetter = attrgetter("pctsimilarity", "qseqlength")

mpl.rc('font', family='normal',weight="normal",
              size=10)
mpl.rc('xtick', labelsize=5)
mpl.rc('ytick', labelsize=5)

with open(args_remaining[1]) as fh:
    records = lineRecordIterator(fh, M4Record, M4RecordTypes)
    items = map(igetter, records)
    (pctids, lens) = zip(*items)

    pp = PdfPages("out.pdf")

    (fig, axScatter) = plt.subplots(figsize=(8.5,5.5))
    axScatter.scatter(lens, pctids, color="blue", s=0.001) 
    axScatter.set_xticks(range(0,80000,2000))
    axScatter.set_yticks(range(0,100,5))
    fig.suptitle(args_remaining[0])
    plt.xlabel("Read Length (bp)")
    plt.ylabel("Alignment Identity (%)")

    divider = make_axes_locatable(axScatter)
    axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
    axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)

    plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(), visible=False)

    len_binsize=250
    len_bins = np.arange(0,50000+len_binsize,len_binsize)
    pid_binsize=0.1
    pid_bins = np.arange(-100.0,100.0+pid_binsize,pid_binsize)

    axHistx.hist(lens,bins=len_bins, color="orange")
    (ax1,ax2,ay1,ay2) = axHistx.axis()
    if p_arg_map["tophist_maxy"] > 0:
        axHistx.axis((ax1,ax2,ay1,p_arg_map["tophist_maxy"]))
    #axHistx.axis('off')
    axHisty.hist(pctids, bins=pid_bins, orientation='horizontal', color="green")
    axHisty.axis('off')

    plt.savefig(pp, format="pdf")
    pp.close()

        

