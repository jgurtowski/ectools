#!/usr/bin/env python

##
#Filters out the entries in the db

import sys
import os

if len(sys.argv) < 3:
    print "filter_out.py db file.txt"
    sys.exit(1)


db = {}

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
        if not db.has_key(k):
            sys.stdout.write(l)

        
