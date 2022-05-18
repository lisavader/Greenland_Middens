
file=$1

contig_name=$(zcat $file | bioawk -c fastx '{print length($seq),$name}' | sort -n | tail -n1 | cut -f2)
zcat $file | bioawk -v query=$contig_name -c fastx '($name==query){print $seq}' > largest_contig.fasta
