import sys
import os
import mysql.connector
import subprocess
import glob
import argparse
import csv

parser = argparse.ArgumentParser()

parser.add_argument("tax_level",type=str,help="choose the taxonomic level (species,genus,family,order,class,phylum,kingdom,superkingdom,all)")
parser.add_argument("output",type=str,help="specify output file")
parser.add_argument("-d","--directory",type=str,default=".",help="provide directory, where .bam files are stored (default = current)")
parser.add_argument("-s","--select",type=str,default="",help="string the filename has to contain")
parser.add_argument("-c","--config",type=str,default=os.path.expanduser("~/.my.cnf"),help="specify path to mysql config file")
args = parser.parse_args()

connection = mysql.connector.connect(option_files=args.config,database="taxonomy")
cursor= connection.cursor()

search_string=args.directory+"/*"+args.select+"*"
if not ".bam" in search_string:
	search_string=search_string+".bam"

input_files=glob.glob(search_string)

user_tax_level=args.tax_level
outfile=args.output

def id_to_name(id,tax_level):
	query="select "+tax_level+"_name from tax where id = \'"+id+"\'"
	cursor.execute(query)
	try:	
		result=cursor.fetchone()[0]
	#if the id is not present in the database, pass id as result
	except TypeError:
		#print(id+" not found!")
		result=id
	#sometime the id is present, but there is no information on the specified taxonomic level.
	#output the id if requesting only one taxon, output '-' if requesting all taxa
	if result == None:
		#print(id+": no "+tax_level+" data")
		if user_tax_level == "all":
			result="-"
		else:
			result=id
	return(result)

#make dictonary to store all counts
counter = {}

for file in input_files:
	samview = subprocess.Popen(['samtools', 'view', file],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
	
	#boolean specifying whether we are looking at read 1 or not
	read1=True

	for line in samview.stdout:
		#only write the organism name, when we're in the 1st read of a pair (otherwise names become duplicated)
		if read1 == True:
			#decode line
			dline=line.decode(sys.stdout.encoding)
			#retrieve the accession id (from nt or PhyloNorway database)
			id=dline.split("\t")[2]
			#find the species / genus (or other taxonomic level) the organism belongs to
			if user_tax_level == 'all':
				name=id_to_name(id,"species")
				for tax_level in "genus","family","order","class","phylum","kingdom","superkingdom":
					#get the name for each subsequent taxonomic level
					taxname=id_to_name(id,tax_level)
					#add them all together into the full name
					name=name+","+taxname
			else:
				name=id_to_name(id,user_tax_level)
			#increment the count in the dictionary
			counter[name] = counter.get(name,0) + 1

		#convert boolean to False, if True. Convert to True, if False.
		read1 = not read1	

#create header
if user_tax_level == "all":
	header="count,species,genus,family,order,class,phylum,kingdom,superkingdom\n"
else:
	header="count,"+user_tax_level+"\n"

#write dictionary as csv file
with open (outfile,'w') as output:
	output.write(header)
	for name in counter:
		line=str(counter[name])+","+name+"\n"
		output.write(line)

cursor.close()
connection.close()	
