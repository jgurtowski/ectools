#!/usr/bin/env python

#Concatenate delta files

import sys
import os

if not len(sys.argv) >= 4:
    sys.exit("deltacat.py querypath 1.delta 2.delta [3.delta ...] \n")

querypath = sys.argv[1]

deltafiles = sys.argv[2:]

noexist = filter(lambda p : not os.path.exists(p) , deltafiles)

if bool(noexist):
    s = "Cannot find: \n %s \n" % "\n".join(noexist)
    sys.exit(s)


h1 = None
h2 = None

for deltafile in deltafiles:
    with open(deltafile) as fh:
        if not h1 or not h2:
            h1 = fh.readline().strip().split()
            h2 = fh.readline().strip()
            print h1[0],querypath
            print h2
        else:
            fh.readline()
            fh.readline()

        for line in fh:
            print line.strip()
