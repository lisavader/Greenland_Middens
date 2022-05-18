import pandas as pd
import sys
import glob
import os

def read_res(file_path):
        res_df = pd.read_csv(file_path,sep='\t',engine='python')
        return(res_df)

def list_hits(res_df):
        hit_list=[]
        hit_column = res_df['#Template'].str.replace('[^ ]* ','',1)
        for row in hit_column:
                hit_list.append(row)
        return(hit_list)

def merge_samples(sample_dir,query):
	matching_samples = glob.glob(sample_dir+"/"+"*"+query+"*.res")
	total_hits=[]
	for sample in matching_samples:
		hit_list = list_hits(read_res(sample))
		total_hits.extend(hit_list)
	return(total_hits)

def count_hits(list):
	count_df = pd.DataFrame()
	for item in list:
		count=list.count(item)
		count_df = count_df.append({ "Count": count, "Hit": item},ignore_index=True)
	return(count_df)

def write_krona_input(count_df,output_file):
	#change fomatting
	count_df['Hit'] = count_df['Hit'].str.replace(';','\t')
	#write to tsv
	count_df.to_csv(output_file,sep='\t',header=False,index=False)
	#remove quotes
	with open(output_file,'r') as file:
        	new_file=file.read().replace('"','')
	with open(output_file,'w') as file:
        	file.write(new_file)

#get command line args
sample_dir = sys.argv[1]
query = sys.argv[2]
output_file = sys.argv[3]

#build output dir
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir,exist_ok=True)

#save hit counts of the queried samples
all_counts = count_hits(merge_samples(sample_dir,query))
write_krona_input(all_counts,output_file)
