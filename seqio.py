
from collections import namedtuple


FastaRecord = namedtuple('FastaRecord', ['name','seq'])
FastqRecord = namedtuple('FastqRecord', ['name','seq','desc','qual'])


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

