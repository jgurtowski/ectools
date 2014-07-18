#!/usr/bin/env python

import sys
from itertools import imap

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from nucio import lineItemIterator, fileIterator

from args import parseArgs, getHelpStr, CLArgument

description = ("Usage: plot_hist.py [options] input.txt\n\n"
               "Plot histograms from file (usually Jellyfish)\n"
               "First col is occ, second col is count\n")

argument_list = [
    ["minx","minx", int, 0,"minimum x axis value"],
    ["maxx", "maxx", int, -1,"maximum x axis value"],
    ["miny","miny", int, 0,"minimum y axis value"],
    ["maxy","maxy", int, -1,"maximmum y axis value"],
    ["out","out", str, "out.pdf", "output file name (default out.pdf)"],
    ["title","title", str, "", "Title for graph"]]

arguments = map(CLArgument._make, argument_list)

(p_args, args_remaining) = parseArgs(sys.argv[1:], arguments)

if not len(args_remaining) == 1:
    sys.exit(getHelpStr(description, arguments) + "\n")

conv = lambda (i,j) : (int(i),int(j))
(x,y) = zip(*imap(conv,fileIterator(args_remaining[0], lineItemIterator)))

pp = PdfPages(p_args["out"])

plt.plot(x,y)
(minx,maxx)=plt.xlim()
(miny,maxy)=plt.ylim()

minx = p_args["minx"] if p_args["minx"] > minx else minx
maxx = p_args["maxx"] if p_args["maxx"] > 0 else maxx
miny = p_args["miny"] if p_args["miny"] > miny else miny
maxy = p_args["maxy"] if p_args["maxy"] > 0 else maxy
plt.xlim((minx,maxx))
plt.ylim((miny,maxy))

plt.xlabel("Kmer Coverage")
plt.ylabel("Frequency")
plt.suptitle(p_args["title"])
plt.savefig(pp, format="pdf")

pp.close()
