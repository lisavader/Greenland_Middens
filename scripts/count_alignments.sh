module load tools ngs samtools/1.14

count_aln(){
	for file in $(ls $1); do
		local count
		local tot_count
		count=$(samtools view -c $file)
		tot_count=$((tot_count+count))
	done
	echo $tot_count
}

cd /home/projects/cge/data/projects/1214
mkdir -p alncount
#echo "sample,mapTo,bestHit,filtered" > alncount/aln_midden.csv

for sample in $(ls bowtie/ | awk -F "[_]" '{if ($3>=1010168 && $3<=1010178) print $0}'); do
	path="bowtie/"$sample"/"
	mapTo=$(count_aln "${path}*.mapTo.bam")
	bestHit=$(count_aln "${path}*.bestHit.bam")
	filtered=$(count_aln "${path}*.filtered.bam")
	echo $sample,$mapTo,$bestHit,$filtered >> alncount/aln_midden.csv
done
