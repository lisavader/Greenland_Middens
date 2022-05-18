cd /home/projects/cge/data/projects/1214/bowtie/DTU_2021_1010055_1_MG_Nuuk_ID69_S1_StV23C_0_5_inf1_S0_L001 
module load tools ngs python36 samtools/1.14

<<HHH
for file in $(ls *bestHit*); do
	for c in 5 6 7 8 9; do
		output=$(echo $file | sed "s/bestHit/filtered${c}90/")
		echo $file $output
		python ../../scripts/filter_best_hits.py -c 0.$c -i 0.9 $file $output
 		#output=$(echo $file | sed "s/bestHit/filtered${c}95/")
		#python ../../scripts/filter_best_hits.py -c 0.$c -i 0.95 $file $output 
	done
done
HHH

for selection in filtered590 filtered690 filtered790 filtered890 filtered990 filtered595 filtered695 filtered795 filtered895 filtered995 bestHit
do
	#python ../../scripts/list_organisms.py -s $selection species DTU_2021_1010055_1_MG_Nuuk_ID69_S1_StV23C_0_5_inf1_S0_L001.PhyloNorway.${selection}.speciesCount 
	#python ../../scripts/list_organisms.py -s $selection genus DTU_2021_1010055_1_MG_Nuuk_ID69_S1_StV23C_0_5_inf1_S0_L001.PhyloNorway.${selection}.genusCount 
	#python ../../scripts/list_organisms.py -s $selection family DTU_2021_1010055_1_MG_Nuuk_ID69_S1_StV23C_0_5_inf1_S0_L001.PhyloNorway.${selection}.familyCount 
	python ../../scripts/list_organisms.py -s $selection order DTU_2021_1010055_1_MG_Nuuk_ID69_S1_StV23C_0_5_inf1_S0_L001.PhyloNorway.${selection}.orderCount
done
