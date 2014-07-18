
from collections import namedtuple


FastaRecord = namedtuple('FastaRecord', ['name','seq'])
FastqRecord = namedtuple('FastqRecord', ['name','seq','desc','qual'])


def seqlen(record):
    '''Gets the sequence length for a seqio record'''
    return len(record.seq)

def fastaIterator(fh):

    l = fh.readline()
    if(not l or not l.startswith(">")):
        raise Exception("No \">\" at start of Fasta File")
    name = l.strip()[1:]
    seq = ""
    while True:
        l = fh.readline()
        if not l or l.startswith(">"):
            yield FastaRecord(name,seq)
            if not l:
                break
            name = l.strip()[1:]
            seq = ""
        else:
            seq += l.strip()
    

def recordToString(record):
    f = fastqRecordToString if hasattr(record,"desc") else fastaRecordToString
    return f(record)


def fastaRecordToString(record):
    return "\n".join([">"+record.name,record.seq])


def fastqIterator(fh):
    l = fh.readline()
    if(not l or not l.startswith("@")):
        raise Exception("No \"@\" at start of Fastq File")
    name = l.strip()[1:]
    while True:
        nxt = [fh.readline() for _ in range(3)]
        if( not all(nxt)):
            raise Exception("Fastq is corrupted")
        yield FastqRecord(name, nxt[0].strip(), nxt[1][1:].strip(), nxt[2].strip())
        l = fh.readline()
        if not l:
            break
        name = l.strip()[1:]


def fastqRecordToString(record):
    return "\n".join(["@"+record.name, record.seq, "+"+record.desc, record.qual])


def iteratorFromExtension(filename):
    '''
    Get a sequence file iterator 
    Based on the file's extension
    '''
    ext = filename.split(".")[-1]
    if ext in ["fasta", "fa"]:
        return fastaIterator
    elif ext in ["fastq", "fq", "txt"]:
        return fastqIterator
    raise Exception, "Unknown file extension %s for file %s" % (ext,filename)




    



