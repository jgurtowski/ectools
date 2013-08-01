#!/usr/bin/env python

import sys

from io import *

from Bio import SeqIO

from operator import itemgetter
from itertools import groupby, repeat, izip_longest, imap, count, chain
from collections import namedtuple
from cov import getMarkedRanges
from misc import create_enum
import copy


if not len(sys.argv) == 7:
    print "pb_correct.py in.fa in.snps in.showcoords clr_id(float) min_read_length out_prefix"
    sys.exit(1)

CLR_ID_CUTOFF = float(sys.argv[4])
MIN_READ_LENGTH = int(sys.argv[5])

PileupEntry = namedtuple("PileupEntry", ["index","base","snps","utg","clr"])
CovStat = {"COVERED":"COVERED", "UNCOVERED":"UNCOVERED", "JOINED":"JOINED"}

class CoverageRange:
    def __init__(self, b, e, pid, covstat):
        self.begin = b
        self.end = e
        self.pctid = pid
        self.covstat = covstat

    def __repr__(self):
        return "CoverageRange(%d,%d,%f,%s)" % (self.begin,self.end,
                                               self.pctid, self.covstat)
    def __eq__(self,other):
        return (self.begin == other.begin and self.end == other.end
                and self.pctid == other.pctid and self.covstat == other.covstat)


#correction logic
def correct_base(pentry):
    '''Takes a pileup entry and returns corrected base(s)
       With any warnings
       ('bases','warnings','clr_range')
    '''
    #filter snps 
    filt_snps = filter(lambda s: s.qname == pentry.utg, 
                       [] if pentry.snps == None else pentry.snps)

    #nothing
    if len(filt_snps) == 0:
        return (pentry.base, None, pentry.clr) 

    ssnp = filt_snps[0]    
    if len(filt_snps) > 1:
        #better all be insertions
        if all(map(lambda p: p.sbase == '.', filt_snps)):
            return (pentry.base+"".join(map(lambda f: f.qbase,filt_snps)), None, pentry.clr)
        else:
            #not everything is an insertion, add the insertions and
            #return warning
            return (pentry.base+
                    "".join(map(lambda f: f.qbase if f.sbase == "." else "",filt_snps)), 
                    "Multiple SNPs, Not all were Insertions", pentry.clr)
    elif ssnp.sbase == '.': #single insertion
        return (pentry.base+ssnp.qbase, None,pentry.clr)
    elif ssnp.qbase == '.': #Deletion
        return ("", None if ssnp.sbase == pentry.base else "Mismatched Bases", pentry.clr)
    else: #Mismatch
        return (ssnp.qbase, None if ssnp.sbase == pentry.base else "Mismatched Bases", pentry.clr)

def range_size(arange):
    return arange.end - arange.begin
    
def get_contiguous_ranges(ranges):
    '''Gets Contiguous Ranges from a list of CoverageRanges
       Returns a new list of CoverageRanges updated with contiguous
       ranges and their weighted pct_id
    '''
    if len(ranges) == 0:
        return []
    out = [copy.deepcopy(ranges[0])]
    for i in range(1,len(ranges)):
        if ranges[i].begin - ranges[i-1].end  == 1:
            sp = range_size(out[-1])
            sc = range_size(ranges[i])
            out[-1].pctid = ((sp * out[-1].pctid) + 
                             (sc * ranges[i].pctid)) / (sp+sc)
            out[-1].end = ranges[i].end
            out[-1].covstat = CovStat["JOINED"]
        else:
            out.append(copy.deepcopy(ranges[i]))
    return out


rfh = open(sys.argv[1])
sfh = open(sys.argv[2])
afh = open(sys.argv[3])

pout = open(sys.argv[6] +".cor.pileup", "w")
corout = open(sys.argv[6] +".cor.fa", "w")

alignment_it = lineRecordIterator(afh, NucRecord, NucRecordTypes)
snp_it = lineRecordIterator(sfh, NucSNPRecord, NucSNPRecordTypes)


reads = dict(map(lambda r : (str(r.name), str(r.seq)), SeqIO.parse(rfh, "fasta")))
alignments = dict(map(lambda (n,a): (n,list(a)), 
                      groupby(alignment_it, lambda x: x.sname)))

for pbname, snp_entries in groupby(snp_it, lambda x: x.sname):
    warnings = []
    pblen = len(reads[pbname])

    ##create ranges of accepted alignments
    accept_alignment_ranges = [None] * pblen
    #alignments[pbname].sort(key=lambda a: (a.send-a.sstart) * pow(a.pctid/100.0,2))
    alignments[pbname].sort(key=lambda a: (a.send-a.sstart))
    for alignment in alignments[pbname]:
        for p in range(alignment.sstart-1,alignment.send):
            accept_alignment_ranges[p] = alignment.qname

    ##
    ##find clr ranges
    ##

    #find ranges
    covered_ranges = map(lambda (s,e): CoverageRange(s,e,1.0,CovStat["COVERED"]),
                         getMarkedRanges(map(lambda c: 1 if not c == None else 0 , accept_alignment_ranges)))
    uncovered_ranges = map(lambda (s,e): CoverageRange(s,e,0.7,CovStat["UNCOVERED"]),
                           getMarkedRanges(map(lambda c: 1 if c == None else 0 , accept_alignment_ranges)))
    #remove uncorrected ends
    uncovered_ranges = filter(lambda x: not (x.begin == 0 or x.end == pblen-1),uncovered_ranges)
    
    joined_ranges = sorted(covered_ranges + uncovered_ranges, key=lambda x: x.begin)

    #find the clr ranges
    while True:
        clr_ranges = get_contiguous_ranges(joined_ranges)
        if( all(map(lambda y: y.pctid > CLR_ID_CUTOFF,clr_ranges))):
            break
        for cr in clr_ranges:
            #skip clr ranges that are ok
            if cr.pctid > CLR_ID_CUTOFF:
                continue
            
            #get uncorrected subranges for larger clr range
            subranges = filter(lambda x: x.covstat == CovStat["UNCOVERED"]
                               and  x.begin >= cr.begin and x.end <= cr.end , joined_ranges)
            del joined_ranges[joined_ranges.index(max(subranges, key=lambda y: y.end - y.begin))]

    clr_ranges = filter(lambda c: range_size(c) > MIN_READ_LENGTH, clr_ranges)
    #mark clr ranges in array
    clr_range_array = [None] * pblen
    for clr_range in clr_ranges:
        for p in range(clr_range.begin, clr_range.end+1):
            clr_range_array[p] = str("%d_%d" % (clr_range.begin,clr_range.end))

    #build a list of snps
    merged_snps = [None] * pblen
    for pos, snps in groupby(snp_entries, lambda y: y.spos):
        merged_snps[pos-1] = list(snps)
    
    #build the pileup
    pileup = map(PileupEntry._make,
                 izip(count(), 
                      reads[pbname], 
                      merged_snps, 
                      accept_alignment_ranges,
                      clr_range_array))
    
    #correct the bases
    corrected_data = map(correct_base, pileup)
    
    #how to print the snps (str format)
    snp_str = lambda f : "None" if f == None else "%d,%s,%s,%s" % (f.spos,f.sbase,f.qbase,f.qname)
    #build pileup string for debugging
    pileup_str_list = map(lambda x: "\t".join([
                str(x.index), x.base, str(x.utg),
                "|".join(
                    map(snp_str, [None] if x.snps == None else x.snps))]),pileup)
    
    #add warnings to pileup
    pileup_str_list = map(lambda z : "\t".join(map(str,z)),
                          izip(pileup_str_list, 
                               imap(itemgetter(1), corrected_data),
                               imap(itemgetter(0), corrected_data)
                               ))

    pbname_corrected_base = pbname + "_corrected2"

    for clr_name, clr_group in groupby(corrected_data, itemgetter(2)):
        #skip non clear ranges
        if clr_name == None:
            continue
        pbname_corrected = pbname_corrected_base + "/" + clr_name
        corout.write( ">%s\n%s\n" % (pbname_corrected,"".join(imap(itemgetter(0), clr_group))))        
    
    pout.write( ">%s\n%s\n" % (pbname_corrected_base,"\n".join(pileup_str_list)))

rfh.close()
sfh.close()
afh.close()
corout.close()
pout.close()



