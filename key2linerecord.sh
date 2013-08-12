#!/bin/bash

awk '{ for(i=2;i<=NF;i++){print $i"\t"$1}}'