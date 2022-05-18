
cd /home/projects/cge/data/projects/1214/bowtie
echo "Loading modules..."
module load tools ngs python36 samtools/1.14

for sample in $(ls | grep mid | grep 'DTU_2021_1010078\|DTU_2021_1010158\|DTU_2021_1010159\|DTU_2021_1010162\|DTU_2021_1010171\|DTU_2021_1010172'); do
	for file in $(ls $sample/*bestHit.bam); do
		base=${file%.bam}
		output=${base}.filtered.bam
		echo "Executing command: python ../scripts/filter_best_hits.py $file $output"
		python ../scripts/filter_best_hits.py $file $output
	done
done


