#!/bin/bash

id=`printf "%03d" $SGE_TASK_ID`

/bluearc/home/schatz/gurtowsk/sources/wgs.svn/Linux-amd64/bin/utgcns -g cns.gkpStore -t mod.tigstore.03 1 $id -V 
