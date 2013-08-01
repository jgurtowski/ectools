#!/bin/bash
# takes a unitig.layout and outputs read_id[tab]unitig_id

grep "^unitig\|^FRG" unitigs.layout | awk '{ if($1=="unitig"){print $1"\t"$2}else{ print $5}}' | awk '{ if($1 == "unitig"){printf "\n"$0" "}else{printf $1","}}' | awk '{split($3,a,","); for(i=1;i<length(a);i+=1){print a[i]"\t"$2}}'