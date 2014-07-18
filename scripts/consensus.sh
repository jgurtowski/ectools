#!/bin/bash

id=`printf "%03d" $SGE_TASK_ID`

S_OVL_ERROR_RATE=0.02
AS_CNS_ERROR_RATE=0.06
AS_CGW_ERROR_RATE=0.01
AS_OVERLAP_MIN_LEN=100
AS_READ_MIN_LEN=64
export AS_OVL_ERROR_RATE AS_CNS_ERROR_RATE AS_CGW_ERROR_RATE AS_OVERLAP_MIN_LEN AS_READ_MIN_LEN

~/sources/wgs.svn/Linux-amd64/bin/utgcns -g cns.gkpStore -t mod.tigstore.03 1 $id 

~/sources/wgs.svn/Linux-amd64/bin/utgcnsfix \
    -g cns.gkpStore \
    -t mod.tigStore.03 2 ${id} \
    -o cnsfix_${id}.fixes