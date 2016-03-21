#!/usr/bin/perl -w 

use strict;
use locale;
use encoding 'utf8';


sub is_part($$){
    my ($key,$hashRef) = @_;
    my %hash = %{$hashRef};

    foreach my $k (keys %hash){
	if ($k =~ /(^|\-)$key($|\-)/){
	    return 1;
	}
	elsif ($key =~ /(^|\-)$k($|\-)/){
	    return 1;
	}
    }
    return 0;
}

sub get_to_compare($$){
    my ($key,$hashRef) = @_;
    my %hash = %{$hashRef};

    my @output;

    foreach my $k (keys %hash){
	if ($k =~ /(^|\-)$key($|\-)/){
	    $output[$#output+1] = $k;
	    #return $k;
	}
	elsif ($key =~ /(^|\-)$k($|\-)/){
	    $output[$#output+1] = $k;
	    #return $k;
	}
    }
    return @output;
}


my $gold = $ARGV[0];
my $sys = $ARGV[1];
my $out = $ARGV[2];

open(F,$gold) or die "can't open $gold\n";
my @goldInfo = <F>;
close(F);

my %goldEnt = ();
foreach my $gLine (@goldInfo){
    chomp($gLine);
    my @info = split(/\t/,$gLine);
    $goldEnt{$info[0]}{$info[1]} = $info[2];
}

open(F,$sys) or die "can open $sys\n";
my @sysInfo = <F>;
close(F);

my $TP = 0;
my $fuzzyTP = 0;
open(O,">$out") or die "can't open $out\n";
foreach my $sLine (@sysInfo){
    chomp($sLine);
    my @info = split(/\t/,$sLine);
    my $d = $info[0];
    my $span = $info[1];
    my $ned = $info[2];
    if (!$goldEnt{$d}){
#	print $d . "\n";
    }
    if ($goldEnt{$d}{$span}){
	if ($goldEnt{$d}{$span} eq $ned){
	    $TP++;
	}
	else{
#	    print $goldEnt{$d}{$span} . "\t" .  $ned . "\n";
	}
    }
    if (is_part($span,\%{$goldEnt{$d}})){
	my @goldKeys = get_to_compare($span,\%{$goldEnt{$d}});
	if ($#goldKeys > 1){
	    foreach my $a (@goldKeys){
#		print $d . "\t" . $span . "\t" . $a . "\t" . $ned . "\t" . $goldEnt{$d}{$a} . "\n";
	    }
	}
	foreach my $goldKey (@goldKeys){
	    if ($goldEnt{$d}{$goldKey} eq $ned){
		$fuzzyTP++;
		print O "1\t" . $goldEnt{$d}{$goldKey} . "\t" .  $ned . "\t" . $d . "\t" . $goldKey . "\t" . $span . "\n";
	    }
	    else{
#		print $goldEnt{$d}{$goldKey} . "\t" .  $ned . "\n";
		print O "0\t" . $goldEnt{$d}{$goldKey} . "\t" .  $ned . "\t" . $d . "\t" . $goldKey . "\t" . $span . "\n";
	    }
	}
    }

}

my $sys_all = $#sysInfo + 1;
my $gold_all = $#goldInfo + 1;

print "SYSTEM\t" . $sys_all . "\n";
print "GOLD\t" . $gold_all . "\n";
print "TP\t" . $TP . "\n";
print "FUZZY\t" . $fuzzyTP . "\n";

print O "SYSTEM\t" . $sys_all . "\n";
print O "GOLD\t" . $gold_all . "\n";
print O "FUZZY\t" . $fuzzyTP . "\n";


my $precision = $TP / $sys_all;
my $recall = $TP / $gold_all;
my $fscore = 2 * ($precision*$recall/($precision+$recall));

print 100*$precision . "\t" . 100*$recall . "\t" . 100*$fscore . "\n";

$precision = $fuzzyTP  / $sys_all;
$recall = $fuzzyTP  / $gold_all;
$fscore = 2 * ($precision*$recall/($precision+$recall));
print 100*$precision . "\t" . 100*$recall . "\t" . 100*$fscore . "\n";
print O 100*$precision . "\t" . 100*$recall . "\t" . 100*$fscore . "\n";
close(O);
