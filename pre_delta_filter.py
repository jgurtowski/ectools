#!/usr/bin/env python

import sys

from io import getDeltaAlignmentIterator, deltaRecordToOriginalFormat

if not len(sys.argv) == 2:
    sys.exit("pre_delta_filter.py in.delta")
    

fh = open(sys.argv[1])


for record in getDeltaAlignmentIterator(fh):
    print deltaRecordToOriginalFormat(record)

fh.close()
