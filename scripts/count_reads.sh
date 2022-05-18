
#from: https://bioinformatics.stackexchange.com/questions/935/fast-way-to-count-number-of-reads-and-number-of-bases-in-a-fastq-file

#wc -c also includes newline chars, we need to substract them to get the real base count
fix_base_count() {
    local counts=($(cat))
    echo "${counts[0]},$((${counts[1]} - ${counts[0]}))"
}

directory=$1
outfile=$2 

for file in $(ls $directory | grep 'singleton\|trim.fq'); do

counts=$(gzip -dc $directory/$file\
    | awk 'NR % 4 == 2' \
    | wc -cl \
    | fix_base_count)

echo $file,$counts >> $outfile

done

