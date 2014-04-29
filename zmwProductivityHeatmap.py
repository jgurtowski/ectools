#!/usr/bin/env python

import sys

from operator import itemgetter,attrgetter
from itertools import imap, starmap, repeat,izip
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
print Counter(zmw_prods)

print filter( lambda (prod,l): prod == 2 , zip( zmw_prods, map(lambda z: len(z.read()), all_seq_zmws)))

#print zmw_prods[:20]
xy = map(attrgetter("holeXY"), all_seq_zmws)
xyl = map(list,xy)
print "length:" + str(len(xyl))
colors="rgy"

(x,y) =  zip(*xyl)

pp = PdfPages(infile.split(".")[0] + ".pdf")
colormap = map(lambda c: colors[c], zmw_prods)
plt.scatter(x, y, marker='o', s=3,lw=0, c=colormap, edgecolor=colormap)
#plt.legend(["0","1","2"])

plt.savefig(pp, format="pdf")

pp.close()


