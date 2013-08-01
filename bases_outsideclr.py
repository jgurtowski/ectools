#!/usr/bin/env python

import sys

from itertools import imap

#clear ranges are just file like: {read [tab] clr_start [tab] clr_end}

if not len(sys.argv) == 3:
    print "bases_outsideclr.py db.clr in.uncov.regions"
    sys.exit(1)

def cdb_line_to_record(line):
    arr = line.strip().split()
    return (arr[0], (int(arr[1]),int(arr[2])))

cdbfh = open(sys.argv[1])
rfh = open(sys.argv[2])

cdb = dict(imap(cdb_line_to_record , cdbfh))


for line in rfh:
    arr = line.strip().split()
    rname = arr[0]
    if not cdb.has_key(rname):
        sys.stderr.write("Error: could not find %s in db\n" % rname)
        continue
    (clr_start, clr_stop) = cdb[rname]
    bases_outside_clr = 0
    for uncov_start, uncov_end in imap(lambda x: tuple(map(int,x.split(","))), arr[1:]):
        bases_outside_clr += max(0,uncov_end - clr_stop) - max(0,uncov_start-clr_stop)
        bases_outside_clr += max(0,clr_start - uncov_start) - max(0,clr_start-uncov_end)

    print "\t".join(map(str,[rname,clr_start,clr_stop,bases_outside_clr,"\t".join(arr[1:])]))

cdbfh.close()
rfh.close()
