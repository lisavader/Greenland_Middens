import sys
import subprocess
import re
import argparse

#code for running samtools (subprocess) adapted from: https://github.com/pysam-developers/pysam/issues/207

parser = argparse.ArgumentParser()

#POSITIONAL ARGS:
parser.add_argument("input",type=str,help="alignment file (.sam/.bam/.cram) in bowtie standard format")
parser.add_argument("output",type=str,help="specify output file")

#OPTIONAL ARGS:
parser.add_argument("-c","--coverage",type=float,default=0.8,help="set minimum coverage (default=0.8)")
parser.add_argument("-i","--identity",type=float,default=0.9,help="set minimum identity (default=0.9)")
parser.add_argument("-m","--matches",type=int,default=70,help="set minimum alignment length in bp (default=70)")

args = parser.parse_args()

input=args.input
output=args.output

minCV=args.coverage	#min coverage
minID=args.identity 	#min identity
minM=args.matches	#min nr. of matches + mismatches

def get_CV(samline):
	#extract cigar
	cigar=samline.split("\t")[5]

	#sum all digits that are followed by M
	M=sum(map(int,re.findall(r"(\d+)M",cigar)))		
	# Read Length
	read_length=len(samline.split("\t")[9])
	
	# Calculate coverage
	CV=M/read_length

	return(CV)

def get_ID(samline):
	#extract cigar
	cigar=samline.split("\t")[5]
	
	# Find number of true matches (TM)
	#extract M (matches + mismatches)
	M=sum(map(int,re.findall(r"(\d+)M",cigar)))
	#extract XM (mismatches)
	XM=int(re.findall(r"XM:i:(\d+)",samline)[0])
	#calculate true matches
	TM=M-XM
	
	# Find alignment length
	#cigar: sum all digits followed by M, I or D
	ALN=sum(map(int,re.findall(r"(\d+)[MID]",cigar)))

	# Calculate identity
	ID=TM/ALN

	return(ID)

def get_M(samline):
	#extract cigar
	cigar=samline.split("\t")[5]

	#sum all digits that are followed by M
	M=sum(map(int,re.findall(r"(\d+)M",cigar)))

	return(M)

with open(output, 'w') as outstream:
	samview = subprocess.Popen(['samtools', 'view', '-h', input],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
	bamview = subprocess.Popen(['samtools', 'view', '-Sb'],stdin=subprocess.PIPE,stdout=outstream,stderr=subprocess.DEVNULL)
	bamstream = bamview.stdin

	##Loop over all lines, and write out when they meet the requirements (% coverage, % identity and nr. of M)	

	#set integer denoting whether we are in read 1 or 2 of the pair
	i=1

	for line in samview.stdout:		
			dline=line.decode(sys.stdout.encoding)	
			if dline.startswith('@'):
				bamstream.write(line)
			else:	
				#check 1st line of the pair
				if i==1:
					#calculate metrics
					CV_1=get_CV(dline)
					ID_1=get_ID(dline)
					M_1=get_M(dline)
					#store line
					line_1=line
					#next line is 2nd of the pair
					i=2

				#check 2nd line of the pair
				elif i==2:
					#calculate metrics
					CV_2=get_CV(dline)
					ID_2=get_ID(dline)
					M_2=get_M(dline)
					#store line
					line_2=line
					#next line is 1st of the pair
					i=1
		
					#write lines only if both reads meet the requirements
					if CV_1 >= minCV and CV_2 >= minCV and ID_1 >= minID and ID_2 >= minID and M_1 >= minM and M_2 >= minM :
						bamstream.write(line_1)
						bamstream.write(line_2)

