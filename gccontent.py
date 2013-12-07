#!/usr/bin/env python

import sys
from seqio import fastaIterator

def getGCSlidingWindow(sequence, window_size):
    '''Calculates %GC in sequence of sliding window window_size'''
    return map(lambda x: (x.count("G")+x.count("C")) / float(window_size), 
               map(lambda r: sequence[r:r+window_size], 
                   range(len(sequence)-window_size+1)))


def getGCPrintMatrix(gc,resolution):
    '''resolution is the number of y axis ticks, since gc is from 0 to 1
    we just multiply gc * resultion to find the box to put a '*' in 
    '''
    rowl = resolution
    coll = len(gc)
    mat = []
    for r in range(rowl):
        mat.append([" "] * coll)

    for entry in range(len(gc)):
        mat[int(gc[entry]*resolution)][entry] = '*'

    return mat


def printGCGraph(name, seq, windowsize, resolution):
    gc = getGCSlidingWindow(seq, windowsize)
    mat = getGCPrintMatrix(gc,resolution)
    print " " * 4 +name
    print " " * 4 +seq
    for res in reversed(range(resolution)):
        sys.stdout.write("%.2f" % (res/float(resolution)))
        print "".join(mat[res])

if __name__ == "__main__":
    import sys
    
    if not len(sys.argv) == 4:
        sys.exit("gccontent.py in.fa window_size graph_res")

    windowsize = int(sys.argv[2])
    graphres = int(sys.argv[3])

    with open(sys.argv[1]) as fh:
        for record in fastaIterator(fh):
            printGCGraph(record.name, record.seq, windowsize, graphres)
            
