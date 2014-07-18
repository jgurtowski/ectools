less all_2.schtats  | grep "#>" | grep "cov" | awk '{print $1"\t"$3}' | awk '{split($1,a,"="); split($2,b,"="); split(a[1],c,">"); print c[2]"\t"a[2]"\t"b[2]}' > cov.dat
