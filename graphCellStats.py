#!/usr/bin/env python

#Takes as input schtats output files,
#one per SMRTcell and graphs them.
#file names are expected to be from the deplex
#script

import sys
from itertools import chain, imap, cycle
from operator import itemgetter
import math

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from numpy import arange

from args import parseArgs, getHelpStr, CLArgument
from nucio import fileIterator, lineItemIterator
from args import argflag

description = ("Usage: graphCellStats.py [options] title in.schtats [in2.schtats ...]\n\n"
               "Graph SMRTCell Stats")

argument_list = [["lengreater", "lengreater", int, 10000,
                  ("The y-axis will be of reads greater than this "
                   "argument. Make sure that all schatats outputs "
                   "have this increment: ex: #>10000 "
                   "Default: 10000 ")],
                 ["counts", "counts", argflag, False,
                  ("Graph counts instead of bases ie. number of reads")],
                 ["out","out", str, "cellstats.pdf",
                  ("Output filename. Default: 'cellstats.pdf'")]]

arguments = map(CLArgument._make, argument_list)


if not len(sys.argv) > 1:
    sys.exit(getHelpStr(description, arguments) + "\n")

(p_arg_map, args_remaining) = parseArgs(sys.argv[1:], arguments)


if not len(args_remaining) >= 1:
    sys.exit(getHelpStr(description, arguments) + "\n")

title = args_remaining[0]
infiles = args_remaining[1:]

cellnames = map(lambda f : f.split(".")[0].split("_")[0], infiles)

fit_gen = lambda filename : fileIterator(filename, lineItemIterator)
file_iterators = map(fit_gen, infiles)

def getBasesFromLineArr(arr):
    if not bool(arr):
        return
    if arr[0].startswith("n="):
        return arr[6].split("=")[1]
    if arr[0].startswith("#>%d" % p_arg_map["lengreater"]):
        return arr[1].split("=")[1]

def getCountsFromLineArr(arr):
    if not bool(arr):
        return
    if arr[0].startswith("n="):
        return arr[0].split("=")[1]
    if arr[0].startswith("#>%d" % p_arg_map["lengreater"]):
        return arr[0].split("=")[1]

intlog = lambda x : math.log(int(x))
data = []
dgetter = getCountsFromLineArr if p_arg_map["counts"] else getBasesFromLineArr
for cellname, it in zip(cellnames,file_iterators):
    d = map(intlog,filter(bool,imap(dgetter, it)))
    d.append(cellname)
    data.append(d)



mpl.rc('xtick', labelsize=6)
mpl.rc('ytick', labelsize=6)

pp = PdfPages(p_arg_map["out"])

colors = cycle("bgrcmyk")
markers = "ooooooooxxxxxxxx++++++++" 

cellset = sorted(list(set(cellnames)))
cmap = dict(zip(cellset, zip(colors,markers)))

h = []
for cellgroup in cellset:
    groupdata = filter(lambda x : x[2] == cellgroup, data)
    (alld, dgreater, cells) =  zip(*groupdata)    
    h.append(plt.scatter(alld, dgreater, marker=cmap[cellgroup][1], c=cmap[cellgroup][0]))

plt.legend(h,cellset, loc='upper left', fontsize=8, scatterpoints=1)

if p_arg_map["counts"]:
    plt.xlabel("Log (Total Number of Reads)")
    plt.ylabel("Log (Total Number of Reads > %d)" % p_arg_map["lengreater"])
else:
    plt.xlabel("Log (Total Cell Bases)")
    plt.ylabel("Log (Bases > %d )" % p_arg_map["lengreater"])

plt.suptitle(title)

plt.savefig(pp, format="pdf")

pp.close()
