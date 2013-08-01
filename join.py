#!/usr/bin/env python

#join on db field

import sys
from itertools import imap

if not len(sys.argv) == 3:
    print "join.py db file.txt"
    sys.exit(1)

dbfh = open(sys.argv[1])
sys.stderr.write("Loading db ...\n")
db = dict(imap(lambda line: (line.strip().split()[0],line.strip().split()[1:]),dbfh))
sys.stderr.write("done\n")

infh = open(sys.argv[2])

for line in infh:
    arr = line.strip().split()
    key = arr[0]
    if not db.has_key(key):
        sys.stderr.write("Key not in db: %s\n" % key) 
        continue
    print "\t".join(db[key]+arr[1:])

infh.close()
dbfh.close()
