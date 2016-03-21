#!/usr/bin/perl -w

use XML::LibXML;

use strict;
use locale;
use encoding 'utf8';

my $gold = $ARGV[0];
my $out = $ARGV[1];

my $parser = XML::LibXML->new("1.0", "UTF-8");

opendir(my $dh, $gold) || die "can't opendir $gold: $!";
my @docs = readdir($dh);
closedir $dh;

open(O,">$out") or die "can't open $out file\n";
my $nils = 0;
my $dnum = 0;
my $links=0;
my $entities=0;
my $tokens=0;
foreach my $d (@docs){
    if ($d =~ /\.naf$/ or $d =~ /\.xml$/){
        $dnum++;
	my $doc    = $parser->parse_file("$gold/$d");    
	my @wfs = $doc->findnodes("/NAF/text/wf");
	my $sent = 0;
	my $pos = 0;
	my $max = 0;
	while ($pos <= $#wfs && $sent <= 6){
	    my $wf = $wfs[$pos];
	    $sent = $wf->getAttribute("sent");
	    if ($sent <= 6){
		$max = $wf->getAttribute("id");
	    }	    
	    $pos++;
	}
        $tokens+=$pos;
	foreach my $entity ($doc->findnodes("/NAF/entities/entity")){
	    my $span;
	    my @targets = $entity->findnodes("references/span/target");
	    my $pos = 0;
	    if ($targets[0]->getAttribute("id") <= $max){
		while ($pos < $#targets){
		    my $id = $targets[$pos]->getAttribute("id");
		    $span .= $id . "-";
		    $pos++;
		}
		$span .= $targets[$#targets]->getAttribute("id");
        $entities++;

		my @refs = $entity->findnodes("externalReferences/externalRef");
		if ($#refs >= 0){
		    my $ref = $refs[0]->getAttribute("reference");
		    
            if (defined $ref && !($ref eq "") && ($ref =~ /wikipedia/ || $ref =~ /dbpedia/)){
			$ref =~ /.*\/(.*?)$/;
			$ref = $1;
			print O "$d\t$span\t$ref\n";
                $links++;
            } else {
                print O "$d\t$span\tNIL\n";
                $nils++;
            }
        } else {
            print O "$d\t$span\tNIL\n";
            $nils++;
        }
	    }
	}
    }
}
print $dnum;
print "\n";
print $entities;
print "\n";
print $nils;
print "\n";
print $links;
print "\n";
print $tokens;
print "\n";
print "\n";
close(O);
