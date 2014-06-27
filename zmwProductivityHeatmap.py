#!/usr/bin/env python

import sys

from operator import itemgetter,attrgetter
from itertools import imap, starmap, repeat,izip,ifilter
from pbcore.io import BasH5Reader
from collections import Counter

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


if not len(sys.argv) == 2:
    sys.exit("zmwProductivityHeatmap.py input.bas.h5\n")

infile = sys.argv[1]
cell = BasH5Reader(infile)

get_prod = lambda o : getattr(o, "zmwMetric")("Productivity")

zmwgetters = map(itemgetter, cell.allSequencingZmws)
all_seq_zmws = list(starmap(apply,zip(zmwgetters, repeat([cell]))))
zmw_prods = map(get_prod, all_seq_zmws)


prod_lens = zip(zmw_prods, imap(lambda z: len(z.read()), all_seq_zmws))

prod1_lens = map(itemgetter(1), ifilter(lambda (p,l): p==1, prod_lens))
prod2_lens = map(itemgetter(1), ifilter(lambda (p,l): p==2, prod_lens))

xy = map(attrgetter("holeXY"), all_seq_zmws)
xyl = map(list,xy)

colors="rgy"
(x,y) =  zip(*xyl)

cellname = infile.split(".")[0] 
pp = PdfPages(cellname + ".pdf")
colormap = map(lambda c: colors[c], zmw_prods)
plt.scatter(x, y, marker='o', s=3,lw=0, c=colormap, edgecolor=colormap)
plt.suptitle(cellname)

plt.savefig(pp, format="pdf")
plt.legend()

plt.figure()

plt.hist([prod1_lens,prod2_lens],bins=100,normed=True, histtype='bar', label=["prod1", "prod2"])
plt.legend()
plt.xlabel("Read Length")
plt.ylabel("Frequency")
plt.suptitle(cellname)

plt.savefig(pp, format="pdf")

pp.close()


