import pandas as pd
import sys
import os

def read_res(file_path):
        res_df = pd.read_csv(file_path,sep='\t',engine='python')
        return(res_df)

def list_taxa(res_df):
	taxa_list=[]
	taxa_column = res_df['#Template'].str.replace('[^ ]* ','',1)
	for row in taxa_column:
		taxa_list.extend(row.split(';'))
	return(taxa_list)

def write_subset_table(subset,all_taxa,table_name):
	with open(output_dir+"/"+table_name,'w') as table:
		table.write("Taxon,Count\n")

	for item in subset:
		count=all_taxa.count(item)
		with open(output_dir+"/"+table_name,'a') as table:
			table.write(item+','+str(count)+'\n')

#get command line args
res_longread=sys.argv[1]
res_shortread=sys.argv[2]
output_dir=sys.argv[3]

os.makedirs(output_dir,exist_ok=True)

#extract taxa
taxa_longread=list_taxa(read_res(res_longread))
taxa_shortread=list_taxa(read_res(res_shortread))
taxa_all = taxa_longread + taxa_shortread

#find unique taxa and overlap
longread_unique = set(taxa_longread) - set(taxa_shortread)
shortread_unique = set(taxa_shortread) - set(taxa_longread)	
overlap = set(taxa_longread) & set(taxa_shortread)

#write tables
write_subset_table(longread_unique,taxa_longread,"longread_unique_taxa.csv")
write_subset_table(shortread_unique,taxa_shortread,"shortread_unique_taxa.csv")
write_subset_table(overlap,taxa_all,"overlapping_taxa.csv")
