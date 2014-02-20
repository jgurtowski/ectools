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

##Filter the delta file for proper overlaps before doing LIS in delta-filter
#
#Depending on the quality of the data, you may want to ensure
#that only proper overlapping alignments are used for correction.
#If the initial short read assembly is very good (ex. 100kb contig N50)
#you probably want to ensure proper overlaps.
#If the initial assembly is not very contiguous, requiring
#proper overlaps may hinder correction.
PRE_DELTA_FILTER=true;

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

nucmer --maxmatch -l 11 -b 3000 -g 1000 -p ${FILE} ${FILE} ${UNITIG_FILE}

cp ${FILE}.delta ${ORIGINAL_DIR}

FILTERED_DELTA=${FILE}.delta
if [[ "$PRE_DELTA_FILTER" == true ]]
then
    FILTERED_DELTA=${FILE}.delta.pre
    python ${PRE_DELTA_FILTER_SCRIPT} ${FILE}.delta ${WIGGLE_PCT} ${CONTAINED_PCT_ID} ${MIN_ALIGNMENT_LEN} ${FILTERED_DELTA}
    cp ${FILTERED_DELTA} ${ORIGINAL_DIR}
    cp ${FILTERED_DELTA}.log ${ORIGINAL_DIR}
fi

delta-filter -l $MIN_ALIGNMENT_LEN -i 70.0 -r ${FILTERED_DELTA} > ${FILTERED_DELTA}.r

cp ${FILTERED_DELTA}.r ${ORIGINAL_DIR}

show-coords -l -H -r ${FILTERED_DELTA}.r > ${FILTERED_DELTA}.r.sc

cp ${FILTERED_DELTA}.r.sc ${ORIGINAL_DIR}

show-snps -H -l -r ${FILTERED_DELTA}.r > ${FILTERED_DELTA}.snps

cp ${FILTERED_DELTA}.snps ${ORIGINAL_DIR}

python ${CORRECT_SCRIPT} ${FILE} ${FILTERED_DELTA}.snps ${FILTERED_DELTA}.r.sc ${CLR_PCT_ID} ${MIN_READ_LEN} ${FILE}

cp ${FILE}.cor.fa ${ORIGINAL_DIR}
cp ${FILE}.cor.pileup ${ORIGINAL_DIR}

