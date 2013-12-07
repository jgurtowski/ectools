#!/usr/bin/env python

##Simulates reads from genome

import sys

from collections import namedtuple
from seqio import fastaIterator
from itertools import dropwhile,count,repeat
import misc
import random

def insertion(pos, seq):
    return seq[:pos] + random.choice(["A","C","G","T"]) + seq[pos:]

def deletion(pos,seq):
    return seq[:pos] + seq[pos+1:]

def mismatch(pos,seq):
    return seq[:pos] + random.choice(["A","C","G","T"]) + seq[pos+1:]
            
#read.lens is just a file with a list of read lengths
if not len(sys.argv) == 5:
    print "pb_sim.py genome.fa read.lens error_rate out_prefix"
    sys.exit(1)


Chromosome = namedtuple("Chromosome", ["name","seq"])

gfh = open(sys.argv[1])
lfh = open(sys.argv[2])
erate = float(sys.argv[3])
rout = open(sys.argv[4]+".sim.fa", "w")


#read genome into mem
chromosomes = map(lambda r: Chromosome._make((str(r.name),str(r.seq))), fastaIterator(gfh))
chrom_lengths = map(lambda c: len(c.seq), chromosomes)
genome_length = sum(chrom_lengths)
chrom_lengths_ivtf = map(misc.accumulator(0), map(lambda x: float(x)/genome_length , chrom_lengths))

count = 0
for l in lfh:
    #length of read to simulate
    readlen = int(l.strip())
    
    while True:
        #choose a chromosome
        U_c = random.random()
        chr_idx = misc.first_idx(lambda x : x > U_c, chrom_lengths_ivtf)
        chromosome = chromosomes[chr_idx]
        chromosome_len = chrom_lengths[chr_idx]

        #choose a random position
        U_p = int(random.random() * chromosome_len)
    
        if (U_p + readlen) > (chromosome_len - 1):
            continue

        #decide reverse_complement or not
        f = random.choice([("f",lambda x: x), ("r",misc.reverse_complement)])
        
        sim_read = f[1](chromosome.seq[U_p:U_p + readlen])
        sim_read_name = ">"+chromosome.name+":"+str(U_p)+"-"+str(U_p+readlen)+":"+f[0]        
        
        ##add errors
        #how many errors? normal approx to binomial
        num_errors = abs(int(random.normalvariate(readlen*erate, readlen*erate*(1-erate))))
        for i in range(num_errors):
            position = int(random.random() * len(sim_read))
            f = random.choice([insertion,deletion,mismatch])
            sim_read = f(position,sim_read)

        sim_read_name += " orig_len=%d e_len=%d e_num=%d" % (readlen,len(sim_read),num_errors)
        
        rout.write("%s\n%s\n" % (sim_read_name,sim_read))
        break
    count += 1
    if count % 10000 == 0:
        sys.stderr.write("Simulated: %d\n" % count) 

gfh.close()    
lfh.close()
rout.close()
