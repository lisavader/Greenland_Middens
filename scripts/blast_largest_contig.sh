module load tools ngs perl
module load ncbi-blast/2.12.0+

cd /home/projects/cge/data/projects/1214/metaflye
for sample in $(ls); do
	cd $sample
	for i in $(seq -w 00 54); do
		blastn -query largest_contig.fasta -db /home/databases/metagenomics/db/nt_20220208/nt.$i -outfmt "6 std staxid" -perc_identity 95 -num_threads 4 >> largest_contig_blast.out
	done
	cd ..
done

