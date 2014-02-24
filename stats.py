
from itertools import imap
from collections import namedtuple
from operator import add
from math import sqrt

BasicStats = namedtuple('BasicStats', ["n","min","max",
                                  "mean","stdev",
                                  "sum","cov"])

NStarType = namedtuple('NStar', ['star','count',
                                 'length'])

BigIncrement = namedtuple('BigIncrement', ['increment',
                                           'count',
                                           'bases',
                                           'coverage'])

##types in this tuple are above
ExtendedStats = namedtuple('ExtendedStats', ['basic',
                                             'nstar',
                                             'bigs',
                                             'genome_size'])


def NStar(increments, genome_size):
    '''Retuns a list of functions that will
    calculate N_[increment]'''
    
    def _Nstar(inc):
        def _N(data):
            '''Note data must be reverse sorted'''
            cutoff = genome_size * (inc/100.0)
            cumsum = 0
            cnt = 0
            for l in data:
                cnt += 1
                cumsum += l
                if cumsum >= cutoff:
                    return NStarType(inc,cnt,l)
            return NStarType(inc,float('NaN'),float('NaN'))
                
        return _N

    return map(_Nstar, increments)

def LBig(length_increments,genome_size=None):
    '''Returns a list of functions that will
    calculate the 'BigIncrement's of some lengths''' 

    def _LBig(inc):
        def _L(data):
            '''Note data must be reverse sorted'''
            cnt = 0
            bases = 0
            cov = None
            if genome_size:
                cov = 0
            for l in data:
                if l <= inc:
                    break
                cnt += 1
                bases += l
                if genome_size:
                    cov = bases / float(genome_size)
            return BigIncrement(inc,cnt,bases,cov)
        return _L
    
    return map(_LBig, length_increments)


def getBasicStats(lengths, genome_size = None):
    '''get stats from a list of lengths
    NOTE: lengths must be sorted in reverse
    '''
    
    num = len(lengths)
    total = sum(lengths)
    mean = total / float(num)
    stdev = sqrt(reduce(add,imap( lambda y: y*y,
                                  imap( lambda x : x-mean, lengths))) / float(num))
    cov = None
    if genome_size:
        cov = total / float(genome_size)
        
    minimum = lengths[-1]
    maximum = lengths[0]

    return BasicStats(num, minimum, maximum,
                      mean, stdev, total,cov)


def basicStatsToString(basic_stats):
    '''Basic stats to string'''
    
    s = "2 : n={n} [{min}, {max}] {mean:.2f} +/- {stdev:.2f} sum={sum}"
    fmtstr = s.format(**dict(basic_stats._asdict()))

    if basic_stats.cov:
        fmtstr += " cov={0:.2f}".format(basic_stats.cov)

    return fmtstr


def nstarsToString(nstars):
    '''List of nstars to make into a string'''
    s = "N{star}={length} N{star}cnt={count}"
    return "\n".join(map(lambda x: s.format(**dict(x._asdict())),
                         nstars))
    
    
def bigsToString(bigs):
    '''List of bigs to make into a string'''

    def bigformat(big):
        s = "#>{increment}={count} bases>{increment}={bases} {cov}"
        covstr = "cov={0:.2f}".format(big.coverage) if big.coverage else ""
        d = dict(big._asdict().items() + [('cov',covstr)])
        return s.format(**d)
    
    return "\n".join(map( bigformat, bigs))
                       
def extendedStatsToString(stats):
    ''' stats should be of type 'Stats' '''
    fmt_strs = []
    
    if stats.genome_size:
        fmt_strs += ["Assumed Genome Size: %d " % stats.genome_size]
    
    fmt_strs += map( lambda func, data : func(data),
                    [basicStatsToString, nstarsToString, bigsToString],
                    [stats.basic, stats.nstar, stats.bigs])
    
    #remove any empty ones
    fmt_strs = filter(bool, fmt_strs)

    return "\n\n".join(fmt_strs)
    





