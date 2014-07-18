#!/usr/bin/env python

#################################################################################$$
# Copyright (c) 2011-2013, Pacific Biosciences of California, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted (subject to the limitations in the
# disclaimer below) provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials provided
#  with the distribution.
#
#  * Neither the name of Pacific Biosciences nor the names of its
#  contributors may be used to endorse or promote products derived
#  from this software without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE
# GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY PACIFIC
# BIOSCIENCES AND ITS CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PACIFIC BIOSCIENCES OR ITS
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#################################################################################$$


import os
import sys
import subprocess
import shlex
from pbcore.io import FastaIO

if not len(sys.argv) == 5:
    sys.exit("tig-sense.py reads.fa gkpstore tigstore workingdir\n")

sequence_file = sys.argv[1]
gkp_store = sys.argv[2]
tig_store = sys.argv[3]
work_tmp_dir = sys.argv[4]

frag_id_map = {}
fmap_args = "~/sources/wgs.svn/Linux-amd64/bin/gatekeeper -tabular -dumpfragments %s > frg_id.map" % gkp_store
print "running: %s" % fmap_args
os.system(fmap_args)
with open("frg_id.map") as fmap_out:
    for l in fmap_out:
        """SRR801638.26757_corrected2/1_3278       20498"""
        l = l.strip().split()
        if l[0] == "UID":
            continue
        frag_id_map[int(l[1])] = l[0]

seq_db = {}
seqF = FastaIO.FastaReader(sequence_file)
for r in seqF:
    seq_db[r.name] = r.sequence

            
args = "~/sources/wgs.svn/Linux-amd64/bin/tigStore -g %s -t %s 1 -D unitiglist > unitiglist" % (gkp_store, tig_store )
print "running : %s" % args
os.system(args)
out = open("unitiglist")
for l in out:
    l = l.strip().split()
    if len(l) == 0: continue
    if l[0] == "maID": continue
    unitig_id = int(l[0])

    read_file_name = "%s/t_reads_%07d.fa" % (work_tmp_dir, unitig_id)
    read_file = open(read_file_name, "w")

    tig_ref_file_name = "%s/t_ref_%07d.fa" % (work_tmp_dir, unitig_id)
    tig_ref_file = open(tig_ref_file_name, "w")

    frag_list_fn = "%s/frag_list_%d" % (work_tmp_dir, unitig_id)
    tigStore_args = "~/sources/wgs.svn/Linux-amd64/bin/tigStore -g %s -t %s 1 -d frags -u %d > tig_id.map" % (gkp_store, tig_store, unitig_id)
    frags = []
    max_coor = 0
    print "running: %s" % tigStore_args
    os.system(tigStore_args)
    with open("tig_id.map") as tig_id_map_fh:
        for frag in tig_id_map_fh:
            """FRG    1453 179419,182165"""
            frag = frag.strip()
            if len(frag) == 0:
                continue
            frag = frag.replace(",", " ")
            frag = frag.strip().split()
            frag_id = int(frag[1])
        

            frags.append( ( frag_id, int(frag[2]), int(frag[3]) ) )
            max_coor = max( int(frag[2]), int(frag[3]), max_coor ) 

    rMap = dict(zip("acgtACGTnN","tgcaTGCAnN"))
    seq_array = ["N"] * max_coor


    for frag_id, b, e in frags:
        #print frag_id, b, e
        rname = frag_id_map[frag_id]
        sequence = seq_db[rname]
        print >>read_file, ">"+rname
        print >>read_file, sequence

        if b < e:
            for p in range(b, e):
                if seq_array[p] == "N":
                    try:
                        seq_array[p] = sequence[p-b]
                    except:
                        pass

        if b > e:
            b, e = e, b
            rseq = "".join([rMap[c] for c in sequence[::-1]])
            for p in range(b, e):
                if seq_array[p] == "N":
                    try:
                        seq_array[p] = rseq[p-b]
                    except:
                        pass

    print >>tig_ref_file, ">unitig_%d" % unitig_id
    print >>tig_ref_file, "".join(seq_array)
    
    #print "q-sense.py r %s %s --output_dir %s --output tig_cns_%07dd --n_iter 3 --nproc 8 --min_cov 0 --max_n_reads %d" % (read_file_name,
    #                                                                                                  tig_ref_file_name,
    #                                                                                                  work_tmp_dir,
    #                                                                                                  unitig_id,
    #                                                                                                  len(frags)*2) 

    read_file.close()
    tig_ref_file.close()
    if len(frags) == 1:
        os.system("cp %s %s/tig_cns_%07d.fa" % (tig_ref_file_name, work_tmp_dir, unitig_id) )
    else:
        os.system("q-sense.py r %s %s --output_dir %s --output tig_cns_%07d --cname uti_cns_%07d --n_iter 3 --nproc 16 --min_cov 0 --max_n_reads %d" % (read_file_name, 
                                                                                     tig_ref_file_name, work_tmp_dir, unitig_id, unitig_id, len(frags)*2) )
    os.system("rm -f %s/t_* %s/*_input*" % (work_tmp_dir, work_tmp_dir))

out.close()
