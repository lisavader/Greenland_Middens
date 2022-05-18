#!/bin/bash

module load ngs tools
module load pigz/2.3.4

cd /home/projects/cge/data/projects/1214/metaflye

for sample in DTU*; do
cd $sample
rm -r 00-assembly 10-consensus 20-repeat 30-contigger 40-polishing
#compress with pigz, an alternative to gzip that allows multithreading (default = max avail threads)
pigz *fasta *gfa *gv
echo "Cleaned up $sample!"
cd ..
done

echo "Finished."

