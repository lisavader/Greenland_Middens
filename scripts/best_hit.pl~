#!/usr/bin/env perl
my $command="$0 ";
my $i=0;
while (defined($ARGV[$i])){
  $command .= "$ARGV[$i] ";
  $i++;
}
use Getopt::Std;
use Cwd;
use strict;
# Default parameters
my $fh_log = *STDERR;
my $fh_out = *STDOUT;
my $fh_inp = *STDIN;
my $verbose=0;
my $postName='bestHit';
my $sampleName;
my $searchDir;
my %fragmentCount=();
#
# Process command line
#
getopts('hi:o:vl:d:')||Usage();
#
# Usage
#
if (defined($Getopt::Std::opt_h)||defined($Getopt::Std::opt_h)){
  # Print help message
  Usage();
}

sub Usage {
  print ("Usage: $0 [-h] [-i name] [-d directory] [-o name] \n");
  print ("Description:\n");
  print ("$0 - find best hit from bam files. Requirements: samtools\n");
  print ("\n");
  print ("Options:\n");
  print ("  -h  : display this message\n");
  print ("  -i  : sample name ex. DTU_2021_1010236_1_MG_Mid_ID_A1_26A_Midden_S0_L001\n");
  print ("  -d  : full path dirctory where to search for bam files where 'sample name' is included in bam file name\n");
  print ("  -o  : output fragment count file [STDOUT]\n");
  print ("  -l  : logfile [STDERR]\n");
  print ("  -v  : Verbose [off]\n");
  print ("\n");
 exit;
} # Usage

#
# input sample file name 
#
if (defined($Getopt::Std::opt_i)){
    $sampleName=$Getopt::Std::opt_i;
}
else{
    die ("option -h has not been defined: $!");
}

#
# post output name
#
if (defined($Getopt::Std::opt_o)){
    open($fh_out,">", $Getopt::Std::opt_o);
}

if (defined($Getopt::Std::opt_l)){
    open($fh_log,">",$Getopt::Std::opt_l);
}
if (defined($Getopt::Std::opt_v)){
    $verbose=1;
}
if (defined($Getopt::Std::opt_d)){
    $searchDir=$Getopt::Std::opt_d;
}
else{
    die ("option -d has not been defined: $!");
}
###############################################################################
# Main
#
###############################################################################
my $datestring = localtime();
my $thisDir=cwd();
if ($verbose){
    print $fh_log "## Local date and time $datestring - Start program\n";
    print $fh_log "# $command\n";
    print $fh_log "# working dir: $thisDir\n\n";
}

#
# Find files
#
my @files=`find $searchDir -name \"$sampleName*.mapTo.bam\"`;
chomp(@files);
my $missing=0;
if (@files){
    foreach my $file (@files){
#	print $fh_log "# Found file: $file\n" if ($verbose); 
	my $bestHit = $file;
	$bestHit =~ s/\.mapTo\./\.bestHit\./g;
	if (! -e $bestHit){
#	    print $fh_log "# file not found - setting missing=1: $bestHit\n" if ($verbose);
	    $missing=1;
	}
    }

    #
    # if missing==1 then redo all bestHit files
    #
    my %rec=();
    my $fh_bamIn;
    my $fh_bamOut;

    if ($missing){
	print $fh_log "At least one bestHit file was missing - I remake all bestHit files\n" if ($verbose);
	my $partition=$0;
	foreach my $file (@files){
	    $partition++;
	    my $cmd="samtools view $file -f2 |";
	    print $fh_log "# partition=$partition\n# Doing: $cmd\n" if ($verbose);
	    open($fh_bamIn,"$cmd");
	    while (defined($_=<$fh_bamIn>)){
		my @w=split(/\t/);
		my $read = $w[0];
		my $as = substr($w[13],5);
		
		my $mate = <$fh_bamIn>;
		my @w_mate = split(/\s+/,$mate);
		$as += substr($w_mate[13],5);
		if (! exists ($rec{$read}{sumAS})){
		    $rec{$read}{sumAS}=$as;
		    $rec{$read}{partition}=$partition;
		}
		else{
		    if ($as > $rec{$read}{sumAS}){
			$rec{$read}{sumAS}=$as;
			$rec{$read}{partition}=$partition;
		    }
		}
	    }
	    close($fh_bamIn);
	}
    
	
	$partition=0;
	foreach my $file (@files){
	    $partition++;
	    my $bestHit = $file;
	    $bestHit =~ s/\.mapTo\./\.bestHit\./g;
	    print $fh_log "# Making file: $bestHit\n";
	    open($fh_bamIn,"samtools view -h -f2 $file |");
	    open($fh_bamOut,"| samtools view -h -Sb - -o $bestHit ");
	    my $headerLine=1;
	    
	    while (defined($_=<$fh_bamIn>)){
		if (( (m/^\@SQ/) || (m/^\@PG/) || (m/^\@HD/)) && ($headerLine)){
		    print $fh_bamOut "$_";
		    next;
		}
		else{
		    $headerLine=0;
		}
		my @w=split(/\s+/);
		my $read = $w[0];
		my $acc = $w[2];
		my $mate = <$fh_bamIn>;
		
		if ($rec{$read}{partition}==$partition){
		    $fragmentCount{$acc}++;
		    print $fh_bamOut "$_";
		    print $fh_bamOut "$mate";
		}
	    }
	    close($fh_bamIn);
	    close($fh_bamOut);
	}
    }
    else{
	print $fh_log "All bestHit files are already made\n" if ($verbose);
    }
}

foreach my $id (sort {$fragmentCount{$b} <=> $fragmentCount{$a}} keys %fragmentCount){
    print $fh_out "$id\t$fragmentCount{$id}\n";
}
#
# End program
#
$datestring = localtime();
print $fh_log "## Local date and time $datestring - End program\n" if ($verbose);
