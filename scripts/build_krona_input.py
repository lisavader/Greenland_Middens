import pandas as pd
import sys

def read_mapstat(file_path):
	mapstat_df = pd.read_csv(file_path,sep='\t',comment='##',engine='python')
	return(mapstat_df)			

def create_krona_input(mapstat_df):
	#subset relevant columns
	krona_df = mapstat_df.loc[:,('readCount','# refSequence')]
	#change formatting
	krona_df['# refSequence'] = krona_df['# refSequence'].str.replace('[^ ]* ','',1)
	krona_df['# refSequence'] = krona_df['# refSequence'].str.replace(';','\t')
	return(krona_df)


#read command line arguments
file_path=sys.argv[1]
sample=sys.argv[2]
output_file=sys.argv[3]

#read mapstat table
mapstat_df=read_mapstat(file_path)
#produce krona output
krona_df=create_krona_input(mapstat_df)
#write to tsv
krona_df.to_csv(output_file,sep='\t',header=False,index=False)
#remove quotes
with open(output_file,'r') as file:
	new_file=file.read().replace('"','')
with open(output_file,'w') as file:
	file.write(new_file)

