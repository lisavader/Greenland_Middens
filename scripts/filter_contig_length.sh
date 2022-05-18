#!/bin/bash

module load tools ngs
module load bioawk/1.0

file=$1
cutoff=$2

name=${file%.fasta*}

bioawk -c fastx -v n=${cutoff} '(length($seq)>n){print ">" $name ORS $seq}' $file > ${name}'_filtered_'${cutoff}'bp.fasta.gz'

