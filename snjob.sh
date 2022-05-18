#!/bin/bash

IODIR=clusterIO
MAXJOBS=6000

mkdir -p $IODIR

module load tools ngs
module load anaconda3/4.4.0

snakemake --max-jobs-per-second 10 --local-cores 4 --stats snakerunstats.json --latency-wait 30 --cluster-config cluster_computerome.json --cluster "qsub -e $IODIR -o $IODIR -W group_list={cluster.proj} -A {cluster.proj} -l nodes=1:ppn={cluster.core},mem={cluster.vmem},walltime={cluster.time}" --jobs $MAXJOBS "$@"

