#!/bin/bash

module load tools ngs
module load pigz/2.3.4

cd /home/projects/cge/data/projects/1214/

for sample in metaspades/DTU* hybrid_metaspades/DTU* hybrid_metaspades_contigs/DTU*; do
cd $sample
rm -r K27 K47 K67 K87 K107 K127 tmp misc
rm before_rr.fasta first_pe_contigs.fasta
#compress with pigz, an alternative to gzip that allows multithreading (default = max avail threads)
pigz *fasta *fastg *gfa *paths
echo "Cleaned up $sample!"
cd ../..
done

echo "Finished."
