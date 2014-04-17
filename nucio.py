import sys

from collections import namedtuple
from itertools import imap, izip, ifilter
from misc import trueFunc

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

M4Record = namedtuple('M4Record',
                      ["qname", "tname", "score", "pctsimilarity", "qstrand",
                       "qstart", "qend", "qseqlength", "tstrand", "tstart" ,"tend",
                       "tseqlength", "mapqv"])
M4RecordTypes = [str, str, float, float, int, int, int, int, int, int,int,int,int]


def lineRecordIterator(fh, nt, nt_types, filter_func=trueFunc, delim=None, cleaner_func=None):
    '''Create an iterator with given file handle (fh)
    as well as named tuple type (nt)
    and the column types (nt_types)

    filter_func filters lines before they are split, return True to keep the line
    cleaner_func takes a line and returns a list, default just splits on delim,
                 returned list must match the number of fields in the nt

    '''

    if cleaner_func == None:
        cleaner_func = lambda line : line.strip().split(delim) 
    
    filtered_lines = ifilter(filter_func, fh)
    split_clean_lines = imap(cleaner_func, filtered_lines)
    typed = imap(lambda splitline : typeify(splitline, nt_types), split_clean_lines)

    return imap(nt._make, typed)


def lineItemIterator(fh, filter_func=trueFunc):
    '''Takes a file handle and returns a list of the split line
    Will also take a filter function to filter out lines before they
    are split
    '''
    filtered = ifilter( filter_func, fh)
    return imap(str.split, filtered)

def getNucmerAlignmentIterator(fh):
    '''Get nucmer alignments from show-coords output
    (Deprecated legacy)
    '''
    return lineRecordIterator(fh, NucRecord, NucRecordTypes)


def fileIterator(filename, itemIterator, open_func=open):
    '''Handles the life cyle of a file,
       The itemIterator will be passed the 
       opened file handle
    '''
    with open_func(filename) as fh:
        for item in itemIterator(fh):
            yield item

def recordToString( record, delim="\t" ):
    '''Prints a generic named tuple combined by delim'''
    fields = record._fields
    return delim.join(imap(lambda x: str(getattr(record,x)), fields))

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


def deltaRecordHeaderToString(dr):
    a = map(lambda x : str(getattr(dr, x)), dr._fields[:-1])
    a[0] = ">"+a[0]
    return " ".join(a)

def deltaAlignmentHeaderToString(alignment):
    a = map(lambda x : str(getattr(alignment,x)), 
            alignment._fields[:-1])    
    return " ".join(a)

def deltaRecordToOriginalFormat(dr):

    final_str = deltaRecordHeaderToString(dr)
    
    for alignment in dr.alignments:
        final_str += "\n" + deltaAlignmentHeaderToString(alignment)
        p = "\n".join(map(str, alignment.positions))
        final_str += "\n"+p
        
    return final_str
    


class FileOrStream:
    '''Opens a File or a Stream from a String'''

    _streams = {"stdin": sys.stdin,
                 "stdout":sys.stdout,
                 "stderr":sys.stderr}

    def __init__(self, s, *args ):
        '''s is a string representation of what you 
        want to open, could be file or string'''

        self.s = s
        self.eargs = args
        self.isStream = False

    def __enter__(self):
        if self.s in FileOrStream._streams:
            self.isStream = True
            return FileOrStream._streams[self.s]
        self.fh = open(self.s, *self.eargs)
        return self.fh
    
    def __exit__(self, ttype ,value, traceback):
        if not self.isStream:
            self.fh.close()

    
def openerFromExtension(filename, default=None):
    '''Get an open function from a file's
    extension
    default is the default opener, None by default
    returns:
       (open_func, filename_with_extension_removed)
    '''
    arr = filename.split(".")
    
    if arr[-1] == "gz":
        import gzip
        return (gzip.open, ".".join(arr[:-1]))

    return (default, filename)
