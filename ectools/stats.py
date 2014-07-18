
from itertools import imap
from collections import namedtuple
from operator import add, attrgetter, lt
from functools import partial
from math import sqrt, ceil
from string import ljust
from strutil import strAppend

BasicStats = namedtuple('BasicStats', ["n","min","max",
                                  "mean","stdev",
                                  "sum","cov"])

NStarType = namedtuple('NStar', ['star','count',
                                 'length'])

BigIncrement = namedtuple('BigIncrement', ['increment',
                                           'count',
                                           'bases',
                                           'coverage'])

SpanCov = namedtuple('SpanCov', ['increment',
                                 'count',
                                 'bases',
                                 'coverage'])

HistBin = namedtuple('HistBin', ['bin',
                                 'count'])

##types in this tuple are above
ExtendedStats = namedtuple('ExtendedStats', ['basic',
                                             'nstar',
                                             'bigs',
                                             'hist',
                                             'spancovs',
                                             'genome_size'])
def SpanningCoverage(increments,genome_size =None):
    '''Calculates the coverage of reads
    that can cover an increment'''
    
    def _SC(inc):
        def _N(lens):
            cnt = 0
            bases_greater = 0
            for l in lens:
                if l > inc:
                    bases_greater += l-inc
                    cnt += 1
            cov = bases_greater / float(genome_size) if genome_size else None
            return SpanCov(inc, cnt, bases_greater, cov)
        return _N
    return map(_SC, increments)

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


def Hist(increments, bin_size):
    
    def _Hist(inc):
        def _H(lens):
            cond = lambda x: x >= inc and x < inc+bin_size
            return HistBin(inc,len(filter(cond, lens)))
        return _H
    
    return map(_Hist, increments)



    


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
    
    s = "n={n} [{min}, {max}] {mean:.2f} +/- {stdev:.2f} sum={sum}"
    fmtstr = s.format(**dict(basic_stats._asdict()))

    if basic_stats.cov:
        fmtstr += " cov={0:.2f}".format(basic_stats.cov)

    return fmtstr


def nstarsToString(nstars):
    '''List of nstars to make into a string'''
    s = "N{star}={length} N{star}cnt={count}"
    return "\n".join(map(lambda x: s.format(**dict(x._asdict())),
                         nstars))
    
def spancovsToString(spancovs):
    
    def spancovformat(spancov):
        s = "#>{increment}={count} extra_bases>{increment}={bases} {cov}"
        covstr = "cov={0:.2f}".format(spancov.coverage) if spancov.coverage else ""
        d = dict(spancov._asdict().items() + [('cov',covstr)])
        return s.format(**d)

    covs = map(spancovformat, spancovs)
    return "Spanning Coverage:\n" + "\n".join(covs) if bool(covs) else ""

def bigsToString(bigs):
    '''List of bigs to make into a string'''

    def bigformat(big):
        s = "#>{increment}={count} bases>{increment}={bases} {cov}"
        covstr = "cov={0:.2f}".format(big.coverage) if big.coverage else ""
        d = dict(big._asdict().items() + [('cov',covstr)])
        return s.format(**d)
    
    return "\n".join(map( bigformat, bigs))


def histToVertString(bins):
    '''List of 'HistBin's'''
    if not bool(bins):
        return ""

    N_COLS = 80
    mcount = max(bins, key=attrgetter("count")).count
    mcslen = len(str(mcount))
    mbslen = len(str(max(bins, key=attrgetter("bin")).bin))
    
    def format(bin):
        stars = "*" * int(ceil((bin.count / float(mcount)) * N_COLS))
        binstr = ljust(str(bin.bin), mbslen)
        cntstr = ljust(str(bin.count), mcslen)
        return " : ".join([binstr,cntstr,stars])

    return "\n".join(map(format,bins))

                       
def extendedStatsToString(stats):
    ''' stats should be of type 'Stats' '''
    fmt_strs = []
    
    if stats.genome_size:
        fmt_strs += ["Assumed Genome Size: %d " % stats.genome_size]
    
    fmt_strs += map( lambda func, data : func(data),
                    [basicStatsToString, nstarsToString, histToVertString, bigsToString, spancovsToString],
                    [stats.basic, stats.nstar, stats.hist, stats.bigs, stats.spancovs])
    
    #remove any empty ones
    fmt_strs = filter(bool, fmt_strs)

    return "\n\n".join(fmt_strs)
    





