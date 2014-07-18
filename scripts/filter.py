#!/usr/bin/env python

##
#Filters file's first column by first column of db
# -dbentry flag outputs the entry in the database instead of the
# query
##

import sys
import os

if len(sys.argv) < 3:
    print "filter.py db file.txt [-dbentry]"
    sys.exit(1)


db = {}

dbentry = False
if sys.argv > 3:
    if "-dbentry" in sys.argv[3:]:
        dbentry = True

(dbfile,infile) = sys.argv[1:3]

if not os.path.exists(infile):
    sys.exit("Can't find %s" % infile)

sys.stderr.write("Loading db...")
with open(dbfile) as dbfh:
    for line in dbfh:
        db[line.strip().split()[0]] = line
sys.stderr.write("done\n")

with open(infile) as infh:
    for line in infh:
        k = line.strip().split()[0]
        l = line
        if db.has_key(k):
            if dbentry:
                l = db[k] 
            sys.stdout.write(l)

        
