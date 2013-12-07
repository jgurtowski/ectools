import sys

sys.path.append('..')

from seqio import fastaIterator, fastqIterator, seqIterator

for i in ["bad.fa","corrupt.fa","good.fa"]:
    with open(i) as fh:
        try:
            for record in fastaIterator(fh):
                print record.name
                print record.seq
        except Exception as e:
            print e

for i in ["bad.fq","corrupt.fq","good.fq"]:
    with open(i) as fh:
        try:
            for record in fastqIterator(fh):
                print record.name
                print record.seq
                print record.desc
                print record.qual
        except Exception as e:
            print e



