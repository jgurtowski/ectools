#!/bin/bash -x

#Make sure all of the Nucmer tools are in your path

set -e 

source ~/.bashrc

##SET THE FOLLOWING PARAMETERS

#path to correct script in pbtools repo
CORRECT_SCRIPT=/path/to/ectools/pb_correct.py

#pre filter delta file
PRE_DELTA_FILTER_SCRIPT=/path/to/ectools/pre_delta_filter.py

#smallest alignment allowed, filter out alignments smaller than this
MIN_ALIGNMENT_LEN=200

#Allow % from the ends of the fragments to be wiggle room 
#(for determining proper overlaps)
WIGGLE_PCT=0.05

#pct of read length for alignment to be considered contained
CONTAINED_PCT_ID=0.80

#path to high identity unitigs
UNITIG_FILE=/path/to/unitigs.fa

#Trim out regions with lower identity than
CLR_PCT_ID=0.96

#Minimum read length to output after splitting/trimming
MIN_READ_LEN=3000

###Done parameters

suffix=`printf "%04d" $SGE_TASK_ID`
FILE=p${suffix}

ORIGINAL_DIR=`pwd`

#Move to sge temp storage
if [[ $TMPDIR ]]
then
    cd $TMPDIR
fi

cp ${ORIGINAL_DIR}/${FILE} .

nucmer --maxmatch -l 11 -b 10000 -g 1000 -p ${FILE} ${FILE} ${UNITIG_FILE}

cp ${FILE}.delta ${ORIGINAL_DIR}

python ${PRE_DELTA_FILTER_SCRIPT} ${FILE}.delta ${WIGGLE_PCT} ${CONTAINED_PCT_ID} ${MIN_ALIGNMENT_LEN} ${FILE}.delta.pre

cp ${FILE}.delta.pre ${ORIGINAL_DIR}
cp ${FILE}.delta.pre.log ${ORIGINAL_DIR}

delta-filter -l $MIN_ALIGNMENT_LEN -i 70.0 -r ${FILE}.delta.pre > ${FILE}.delta.pre.r

cp ${FILE}.delta.pre.r ${ORIGINAL_DIR}

show-coords -l -H -r ${FILE}.delta.pre.r > ${FILE}.delta.pre.r.sc

cp ${FILE}.delta.pre.r.sc ${ORIGINAL_DIR}

show-snps -H -l -r ${FILE}.delta.pre.r > ${FILE}.snps

cp ${FILE}.snps ${ORIGINAL_DIR}

python ${CORRECT_SCRIPT} ${FILE} ${FILE}.snps ${FILE}.delta.pre.r.sc ${CLR_PCT_ID} ${MIN_READ_LEN} ${FILE}

cp ${FILE}.cor.fa ${ORIGINAL_DIR}
cp ${FILE}.cor.pileup ${ORIGINAL_DIR}

