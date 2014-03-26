#!/usr/bin/env python

import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np

from nucio import lineRecordIterator, NucRecord, NucRecordTypes
from operator import attrgetter


if not len(sys.argv) == 3:
    sys.exit("graphpid.py delta.sc title\n")

igetter = attrgetter("pctid", "qlen")

mpl.rc('font', family='normal',weight="normal",
              size=10)
mpl.rc('xtick', labelsize=5)
mpl.rc('ytick', labelsize=5)

with open(sys.argv[1]) as fh:
    records = lineRecordIterator(fh, NucRecord, NucRecordTypes)
    items = map(igetter, records)
    (pctids, lens) = zip(*items)

    pp = PdfPages("out.pdf")

    (fig, axScatter) = plt.subplots(figsize=(8.5,5.5))
    axScatter.scatter(lens, pctids, color="blue", s=0.001) 
    axScatter.set_xticks(range(0,80000,2000))
    axScatter.set_yticks(range(0,100,5))
    fig.suptitle(sys.argv[2])
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
    axHistx.axis('off')
    axHisty.hist(pctids, bins=pid_bins, orientation='horizontal', color="green")
    axHisty.axis('off')

    plt.savefig(pp, format="pdf")

    pp.close()

        

