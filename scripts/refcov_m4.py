#!/usr/bin/env python

## gets cov of reference from m4 file

#0x5e9f5c35_0181253	0xd5588546_0148247	-4395	84.0701	0	1689	2937	6828	1	3376	4618	7601	0

import sys

cov = None

for line in sys.stdin:
    arr = line.strip().split()
    start,end,length = map(int,arr[9:12])
    if not cov:
        cov = [0] * length
    for i in range(start-1,end,1):
        cov[i] += 1

print cov
            
