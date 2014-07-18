
from operator import itemgetter,attrgetter
from collections import namedtuple
from itertools import groupby, imap
from functools import partial
from nucio import fileIterator, lineRecordIterator
from nucio import M4Record, M4RecordTypes
from misc import identityFunc


def getRawAlignments(fn):
    '''fn is the filename
       returns An iterator over raw M4Records'''
    itemIterator = lambda f : lineRecordIterator(f, M4Record, M4RecordTypes)
    return fileIterator(fn, itemIterator)

def getAlignments(fn, filter_func=identityFunc):
    '''fn is the filename 
       returns alignments grouped by their name
       filter_func works on a group of alignments for a specific read
    '''
    raw_alignments = getRawAlignments(fn)
    groupby_first = itemgetter(0)
    grouped = groupby(raw_alignments,groupby_first)
    return imap(lambda (k,v) : (k,filter_func(list(v))), grouped)


def filterLongest(alignments):
    ''' Get the longest alignment '''
    align_len = lambda r : r.qend - r.qstart
    return max(alignments,key=align_len)

def filterBestScore(alignments):
    '''Get the best scoring alignment'''
    score_getter = attrgetter("score")
    return min(alignments,key=score_getter)

def longestNonOverlapping(alignments):
    '''
    Gets the best non-overlapping alignment sections 
    with respect to the query sequence
    
    Just greedily sorts the
    alignments by length and adds them sequentially as long
    as they don't overlap another alignment (with respect to the query)
    '''

    align_len = lambda r : r.qend - r.qstart
    alignments.sort(key=align_len, reverse=True)

    newset = []
    not_overlaps = lambda y,other : y.qend < other.qstart or y.qstart > other.qend    

    for a in alignments:
        if all(map(partial(not_overlaps, a), newset)):
            newset.append(a)
    
    return newset
    
