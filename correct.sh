#!/bin/bash -x

#Make sure all of the Nucmer tools are in your path

set -e 

source ~/.bashrc

##SET THE FOLLOWING PARAMETERS

#path to correct script in pbtools repo
CORRECT_SCRIPT=/path/to/pb_correct.py

#path to high identity unitigs
UNITIG_FILE=/path/to/org.utg.fasta

#Trim out regions with lower identity than
CLR_PCT_ID=0.97

#Minimum read length to output after splitting/trimming
MIN_READ_LEN=1000

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

nucmer --maxmatch -l 11 -b 2000 -g 2000 -p ${FILE} ${FILE} ${UNITIG_FILE}

cp ${FILE}.delta ${ORIGINAL_DIR}

delta-filter -i 70.0 -r ${FILE}.delta > ${FILE}.delta.r

cp ${FILE}.delta.r ${ORIGINAL_DIR}

show-coords -l -H -r ${FILE}.delta.r > ${FILE}.delta.r.sc

cp ${FILE}.delta.r.sc ${ORIGINAL_DIR}

show-snps -H -l -r ${FILE}.delta.r > ${FILE}.snps

cp ${FILE}.snps ${ORIGINAL_DIR}

python ${CORRECT_SCRIPT} ${FILE} ${FILE}.snps ${FILE}.delta.r.sc ${CLR_PCT_ID} ${MIN_READ_LEN} ${FILE}

cp ${FILE}.cor.fa ${ORIGINAL_DIR}
cp ${FILE}.cor.pileup ${ORIGINAL_DIR}

