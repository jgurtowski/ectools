import operator
from itertools import repeat,count,compress


#increment coverage (l)
def fillc(l,s,e):
    '''l is an array
    s and e are start and end of
    a region the coverage should be incremented in'''

    if(len(l) < e):
        l += list(repeat(0, e-len(l)))
    for cr in range(s,e):
        l[cr] += 1

def pairwise(iterable,func=operator.add):
    it = iter(iterable)
    prev = next(it)
    for el in it:
        yield func(el,prev)
        prev = el

def accumulate_mod(iterable, func=operator.add):
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        if element == 0:
            total = 0
        else:
            total = func(total,element)
        yield total

def getMarkedRanges(v):
    '''Takes an array v with wanted elements marked as 1
    all other elements are 0. This function returns
    the index ranges of these 1's'''
    
    #subtract adjacent elements to find -1
    #flip these to 1's and change everything else to 0
    #so that we can use it to find the index
    breaks = map(lambda x: 1 if x == -1 else 0 , pairwise(v + [0],operator.sub))

    #create a cumsum of the inverse to know how many elements
    #are a part of this region
    lengths = accumulate_mod(v)

    #zip up the indexes with the lengths
    z = zip(count(),list(lengths))

    #use the breaks to select only the indexes we want
    #and use the cumsum to know how many elements came
    #previously
    endAndLength = compress(z,breaks)

    return map(lambda (e,l): (e-l+1,e), endAndLength)


def getCoverageFromNucAlignments(alignments):
    '''Gets coverage from nucmer alignments'''
    it = iter(alignments)
    n = it.next()
    cov = list(repeat(0,n.slen))
    fillc(cov,n.sstart-1, n.send-1)
    for g in alignments:
        fillc(cov, g.sstart-1, g.send-1)
    return cov

