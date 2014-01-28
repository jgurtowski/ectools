#!/bin/bash

#symlink unitigs.layout
#symlink ovlStore
#cp gkpStore to gkpStore.modified

GENOME_SIZE=12000000
FRAGS_PER_PARTITION=10
ERROR_RATE=0.02

for i in {01..09}
do
    cat unitigs.layout | awk '{if($1=="FRG"){$1=$2=$3=$4=""; print $0}else if($1=="unitig"){print}}' |sed "s/^\s*//" | uniq  > unitigs.layout.${i}.clean

    cat unitigs.layout.${i}.clean | awk '{print $1}' | sed "s/unitig/>/g" | tr '\n' ' ' | tr '>' '\n' | awk 'NF < 3' | tr ' ' '\n' | awk 'NF >0' | awk '{ print "frg iid "$1" isdeleted t" }' > bad.${i}

    #python ~/workspace/ectools/filter.py <(/bluearc/data/schatz/mschatz/devel/bin/tig_length.pl unitigs.layout | awk '$2 < 100000' | awk '{ print $1}') <(less unitigs.layout.${i}.clean  | sed "s/unitig />/g" | awk '{print $1}' | tr '\n' ' ' | tr '>' '\n' | awk 'NF > 0') | awk '{ for(i=2;i<=NF;i++){print $i}}' | awk '{print "frg iid "$1" isdeleted t" }' > bad.${i}

    /bluearc/home/schatz/gurtowsk/sources/wgs.svn/Linux-amd64/bin/gatekeeper --edit bad.${i} gkpStore.modified &> mod.log.${i}

    /bluearc/home/schatz/gurtowsk/sources/wgs.svn.utgdevel/Linux-amd64/bin/unitigger  -I ovlStore  -F gkpStore.modified -T mod.tigstore.${i}  -B $FRAGS_PER_PARTITION  -e $ERROR_RATE  -k  -d 1 -x 5 -z 10 -j 5 -U 1  -o utg.${i}  &> log.${i}

    /bluearc/home/schatz/gurtowsk/sources/wgs.svn/Linux-amd64/bin/tigStore -g gkpStore.modified -t mod.tigstore.${i} 1 -d layout -U  > unitigs.layout.${i}

    /bluearc/data/schatz/mschatz/devel/bin/tig_length.pl unitigs.layout.${i} | sort -n -r -k2,2 > unitigs.layout.${i}.lens

    stats -f 2 -n50 $GENOME_SIZE unitigs.layout.${i}.lens  | tee unitigs.layout.${i}.stats
    
    unlink unitigs.layout
    
    ln -s unitigs.layout.${i} unitigs.layout

done