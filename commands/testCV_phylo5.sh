module load tools ngs python36 samtools/1.14; cd /home/projects/cge/data/projects/1214/bowtie/DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001; python ../../scripts/filter_best_hits.py DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001.PhyloNorway_5.bestHit.bam 0.5; python ../../scripts/filter_best_hits.py DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001.PhyloNorway_5.bestHit.bam 0.6; python ../../scripts/filter_best_hits.py DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001.PhyloNorway_5.bestHit.bam 0.7; python ../../scripts/filter_best_hits.py DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001.PhyloNorway_5.bestHit.bam 0.8; python ../../scripts/filter_best_hits.py DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001.PhyloNorway_5.bestHit.bam 0.9; for file in $(ls DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001.PhyloNorway_5*filtered*); do python ../../scripts/list_organisms.py $file genus; done
