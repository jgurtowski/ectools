#!/usr/bin/env python

import sys

from itertools import groupby, imap
from operator import itemgetter

if not len(sys.argv) == 3:
    print "group_by.py file column"
    sys.exit(1)

col = int(sys.argv[2])
infh = sys.stdin if sys.argv[1] == "-" else open(sys.argv[1])

for key,groups in groupby(imap(lambda line: line.strip().split(), infh),itemgetter(col)):
    print key+"\t"+"\t".join(imap(lambda items: "\t".join(items[:col]+items[(col+1):]),groups))
    
infh.close()
