#!/usr/bin/env python

###
#Takes a bunch of seq files and outputs
#only unique reads based on their names
# (only up to first space in their names)
#everything becomes fasta format
###

import sys

from itertools import starmap, chain
from functools import partial

from seqio import iteratorFromExtension, fastaRecordToString
from nucio import fileIterator, openerFromExtension

if not len(sys.argv) > 1:
    sys.exit("uniqreads.py in.{fa,fq} [in2.{fa.fq} ...]\n")

files = sys.argv[1:]

(openers,nfiles) = zip(*map(partial(openerFromExtension, default=open), files))

its = map(iteratorFromExtension, nfiles)

fileits = starmap(fileIterator, zip(files, its, openers))

namehash = {}
for record in chain.from_iterable(fileits):
    cleanname = record.name.split()[0]
    if not namehash.get(cleanname, False):
        namehash[cleanname] = True
        nr = record._replace(name=cleanname)
        print fastaRecordToString(nr)
    else:
        sys.stderr.write("Duplicate : %s \n" % cleanname)





