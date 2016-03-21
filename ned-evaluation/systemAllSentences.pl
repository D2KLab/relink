#!/usr/bin/perl -w

use XML::LibXML;

use strict;
use locale;
use encoding 'utf8';

my $input = $ARGV[0];
my $resource = $ARGV[1];
my $out = $ARGV[2];
my $outNum = $ARGV[3];


my $parser = XML::LibXML->new();

opendir(my $dh, $input) || die "can't opendir $input: $!";
my @docs = readdir($dh);
closedir $dh;

my $noNED = 0;
my $NED = 0;
my $NERC = 0;

my %tokens = ();

open(O,">$out") or die "can't open $out file\n";
foreach my $d (@docs){
    if ($d =~ /\.naf$/){
	my $doc    = $parser->parse_file("$input/$d"); 
	my @wfs = $doc->findnodes("/NAF/text/wf");
	my $sent = 0;
	my $pos = 0;
	my $max = 0;
	#print $sent;
	while ($pos <= $#wfs && $sent <= 6000){
	    my $wf = $wfs[$pos];
	    my $id = $wf->getAttribute("id");
	    my $token = $wf->textContent;
	    $sent = $wf->getAttribute("sent");
	    if ($sent <= 6000){
		$id =~ /(.*)/;
		$max = $1;
		$tokens{$max} = $token;
	    }
	    $pos++;
	}
	
	foreach my $entity ($doc->findnodes("/NAF/entities/entity")){

	    my $span;
	    my @targets = $entity->findnodes("references/span/target");
	    my @refs = $entity->findnodes("externalReferences/externalRef");
	    if ($#refs >= 0){
		my $pos = 0;
		my $tID = $targets[0]->getAttribute("id");
		$tID =~ /(.*)/;
		$tID = $1;
		if ($tID <= $max){
		    $NERC++;
		    my $mention;
		    while ($pos < $#targets){
			my $id = $targets[$pos]->getAttribute("id");
			$id =~ /(.*)/;
			$span .= $1 . "-";
			$mention .= $tokens{$1} . " ";
			$pos++;
		    }
		    my $h = $targets[$#targets]->getAttribute("id");
		    $h =~ /(.*)/;
		    $span .= $1;
		    $mention .= $tokens{$1};


		    my $ref = "";
		    my $maxconf = 0.0;
		    foreach my $cref (@refs){
			if ($cref->getAttribute("resource") eq $resource && ($cref->getAttribute("confidence")+0.0)>$maxconf){
				$maxconf=$cref->getAttribute("confidence");
				$ref=$cref->getAttribute("reference");
			}
		    }
	
		    if ($ref =~ /dbpedia/ || $ref =~ /wikipedia/){
			$ref =~ /.*\/(.*?)$/;
			$ref = $1;
			print O "$d\t$span\t$ref\t$mention\n";
			$NED++;
            } else{
                print O "$d\t$span\tNIL\t$mention\n";
                $noNED++;
            }

		}
	    }
	    else{
		my $pos = 0;
		my $tID = $targets[0]->getAttribute("id");
		$tID =~ /(.*)/;
		$tID = $1;
		if ($tID <= $max){
            my $mention;
            while ($pos < $#targets){
                my $id = $targets[$pos]->getAttribute("id");
                $id =~ /(.*)/;
                $span .= $1 . "-";
                $mention .= $tokens{$1} . " ";
                $pos++;
            }
            my $h = $targets[$#targets]->getAttribute("id");
            $h =~ /(.*)/;
            $span .= $1;
            $mention .= $tokens{$1};
            print O "$d\t$span\tNIL\t$mention\n";
		    $NERC++;
		    $noNED++;
		}		
	    }
	}
    }
}
close(O);

open(O,">$outNum") or die "can't open $outNum\n";
print O "NERC\t$NERC\n";
print O "NED\t$NED\n";
print O "No NED\t$noNED\n";
close(O);
