import sys

from collections import namedtuple
from itertools import imap, izip


NucRecord = namedtuple('NucRecord',
                       ["sstart","send","b3","qstart","qend",
                        "b6", "salen","qalen","b9","pctid",
                        "b11","slen","qlen","b14","sname","qname"])

NucRecordTypes = [int, int, str, int,int,str,int,int,str,float,str,
                  int,int,str,str,str]

NucSNPRecord = namedtuple('NucSNPRecord',
                          ["spos", "sbase", "qbase", "qpos",
                           "b5", "buf", "dist", "b8", "r", "q", "b9",
                           "frm1", "frm2", "b12", "r1", "r2", "sname", "qname"])
NucSNPRecordTypes = [int, str, str, int, str, int, int, str, int, int,
                     str, int, int, str, int, int, str, str]

DeltaAlignment = namedtuple('DeltaAlignment',
                            ["sstart","send","qstart","qend","errors", 
                             "simerrors", "stopcodons", "positions"])
DeltaAlignmentTypes = [int, int, int, int ,int ,int ,int, list]

DeltaRecord = namedtuple('DeltaRecord',
                         ["sname", "qname", "slen", "qlen", "alignments"])
DeltaRecordTypes = [str, str, int, int, list]

def lineRecordIterator(fh, nt, nt_types):
    '''Create an iterator with given file handle (fh)
    as well as named tuple type (nt)
    and the column types (nt_types)'''
    return imap(lambda x: nt._make(
            imap(lambda (t,e): t(e) ,izip(nt_types, x.strip().split()))
            ),fh)


def getNucmerAlignmentIterator(fh):
    '''Get nucmer alignments from show-coords output
    (Deprecated legacy)
    '''
    return lineRecordIterator(fh, NucRecord, NucRecordTypes)

def nucRecordToString(nuc_record):
    fields = nuc_record._fields
    return "\t".join(
        imap( lambda x : str(getattr(nuc_record, x)), fields))


def typeify(mylist, mytypes):
    return map( lambda (t,e): t(e), izip(mytypes, mylist))

def prepareDeltaRecord(buf):
    if not buf or not buf[0].startswith(">"):
        return None

    l = len(buf)
    rec = DeltaRecord._make(typeify([buf[0][1:], buf[1],buf[2],buf[3],[]],
                DeltaRecordTypes))
    i = 4
    while( l - i >= 7 ):
        almnt = DeltaAlignment._make(typeify(buf[i:i+7]+[[]],
                                             DeltaAlignmentTypes))
        i = i+7
        while True:
            almnt.positions.append(int(buf[i]))
            i += 1
            if almnt.positions[-1] == 0:
                break
        rec.alignments.append(almnt)
    return rec

def getDeltaAlignmentIterator(fh):

    itembuf = []    
    while True:
        line = fh.readline()
        if line.startswith(">") or not line:
            record = prepareDeltaRecord(itembuf)
            if not None == record:
                yield record
            itembuf = []
            if not line:
                break
        for i in line.strip().split():
            itembuf.append(i)

def deltaRecordToOriginalFormat(dr):
    final_str = None

    a = map(lambda x : str(getattr(dr, x)), dr._fields[:-1])
    a[0] = ">"+a[0]
    final_str = " ".join(a)
    for alignment in dr.alignments:
        a = map(lambda x : str(getattr(alignment,x)), 
                alignment._fields[:-1])
        final_str += "\n" + " ".join(a)
        p = "\n".join(map(str, alignment.positions))
        final_str += "\n"+p
        
    return final_str
    
