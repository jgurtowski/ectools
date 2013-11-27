#!/usr/bin/env python

import sys

from itertools import groupby

from io import getNucmerAlignmentIterator
from operator import attrgetter


if not len(sys.argv) == 2:
    sys.exit("filter_cluster.py in.sc\n")

def edit_distance(in1, in2):
    len1 = len(in1)
    len2 = len(in2)
    mat = [[0]*(len2+1) for _ in range(len1+1)]

    #for i in range(0,len1+1):
    #    mat[i][0] = i
    #for j in range(0,len2+1):
    #    mat[0][j] = j
    
    for i in range(1, len1+1):
        for j in range(1,len2+1):
            if in1[i-1] == in2[j-1]:
                mat[i][j] = mat[i-1][j-1]
            else:
                mat[i][j] = min( mat[i][j-1], mat[i-1][j], mat[i-1][j-1]) + 1

    return mat


def print_matrix(mat):
    l1 = len(mat)
    for i in range(l1):
        print "\t".join(map(lambda x: str(x), mat[i]))

afh = open(sys.argv[1])

alignment_it = getNucmerAlignmentIterator(afh)

for pbname, alignment in groupby(alignment_it, lambda x : x.sname):
    print pbname, map(attrgetter("qname"), alignment)



afh.close()
