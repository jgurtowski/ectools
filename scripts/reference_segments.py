#!/usr/bin/env python

#Outputs a genome's chromosome segments
# i.e. splits the genome according to the formula
# in the assembly complexity paper
#   no stretch of more than 1 million N's
import sys

from seqio import fastaIterator
from nucio import fileIterator
from itertools import repeat

if not len(sys.argv) == 2:
    sys.exit("reference_segments.py in.fa")



store_table = {'A':[],
         'C':[],
         'G':[],
         'T':[],
         'N':[]}

previous = 0
curr_count = 1
table = 2
accumulator = ["N",-1,store_table]    

def runs(acc, nxt):
    prev_letter = acc[previous]
    acc[curr_count] += 1
    if not prev_letter == nxt:
        if acc[curr_count] > 0:
            acc[table][prev_letter].append(acc[curr_count])
        acc[previous] = nxt
        acc[curr_count] = 0

    return accumulator

for entry in fileIterator(sys.argv[1],fastaIterator):
    reduce(runs, entry.seq, accumulator)
    runs(accumulator, 'X') #get last sequence
    accumulator[previous] = 'N'
    accumulator[curr_count] = -1

print max(store_table['N'])
