#!/usr/bin/env python

#analyzes split reads across unitigs
#assumes you have unitigs.layout.reads.sorted type file
#with columsn pb_read[tab]clr_range[tab]unitig_id

import sys

from itertools import groupby, imap
from collections import namedtuple

if not len(sys.argv) == 2:
    print "split_read_layout.py unitigs.layout.reads.sorted"
    sys.exit(1)

MIN_CLR_RANGE = 1000


fh = open(sys.argv[1])

Record = namedtuple("Record", ["pb_name","clr_range","unitig_id"])

record_it = imap(lambda line: Record._make(line.strip().split()) , fh)

for pb_read,record in groupby(record_it, lambda x: x.pb_name):
    records = list(record)
    if len(records) < 2:
        continue
    #all same unitig?
    if all(imap(lambda x: x.unitig_id == records[0].unitig_id, records)):
        continue

    #filter with small clr ranges
    if not all(imap(lambda x: int(x.clr_range.split("_")[1])-int(x.clr_range.split("_")[0]) > MIN_CLR_RANGE, records)):
        continue

    print "\t".join([pb_read,",".join(map(lambda x: x.clr_range, records)),",".join(map(str,sorted(map(int,map(lambda y: y.unitig_id, records)))))])
