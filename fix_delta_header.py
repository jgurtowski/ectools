#!/usr/bin/env python

import sys
import os


###
#Assume ref is now in the cwd
###


if not len(sys.argv) == 2:
    print "fix_delta_header.py file.delta"
    sys.exit(1)

cwd = os.getcwd()


fname = sys.argv[1]
ftmp = sys.argv[1]+".copy_tmp_new"

print "%s" % fname

with open(fname) as dfile:
    with open(ftmp,"w") as tmp:
        ref,query = dfile.readline().split()
        new_ref = os.path.join(cwd,os.path.basename(ref))
        tmp.write(" ".join([new_ref, query]) +"\n")
        for line in dfile:
            tmp.write(line)
        
os.rename(ftmp, fname)
