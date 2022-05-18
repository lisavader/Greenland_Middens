
module load tools ngs
module load datamash/1.4

cd /home/projects/cge/data/projects/1214/

directory=trimReads

counts_file="readcount/"$directory"_readcount.csv"
stats_file="readcount/"$directory"_readcount_stats.csv"

#the first time, store header info in name,count,bp
name="sample"
count="count"
bp="bp"

echo ",median,min,max" > $stats_file

#1. Write read counts per sample
for file in $(ls $directory/*.trim.fq.gz $directory/*.singletons.fq.gz $directory/*SE.fq.gz); do	
	new_name=${file%.*}
	#remove unwanted parts
	new_name=$(echo $new_name | sed "s/$directory\///")
	new_name=$(echo $new_name | sed 's/_R[1-2].*//')

	#count nr. of reads and bases
	new_count=$(zcat $file | awk 'NR%4==2' | wc -l)
	new_bp=$(zcat $file | awk 'NR%4==2' | wc -c)

	#if name is same as before, add counts together
	if [[ $new_name = $name ]]; then
		count=$(expr $count + $new_count)
		bp=$(expr $bp + $new_bp)

	#otherwise, write old info to file and update count
	else
		echo $name,$count,$bp >> $counts_file
		echo $name,$count,$bp
		count=$new_count
		bp=$new_bp
	fi
	
	name=$new_name
	
done

#write last line
echo $name,$count,$bp >> $counts_file
echo $name,$count,$bp

#2. Write stats (median,min,max) with datamash
count_stats=$(datamash median 2 min 2 max 2 -t, --header-in < $counts_file)
bp_stats=$(datamash median 3 min 3 max 3 -t, --header-in < $counts_file)
echo "count",$count_stats >> $stats_file
echo "bp",$bp_stats >> $stats_file
	
