
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
