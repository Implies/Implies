#!/usr/bin/perl

use CGI;
use DBI;
#use strict;
#use warnings;

print "content-type: text/html\n\n";

my $q=new CGI;
my $upper = $q->param('Left') || $ARGV[0];
my $lower = $q->param('Right') || $ARGV[1];
my $relation = $q->param('Relate') || $ARGV[2];
my $citation = $q->param('Citation') || $ARGV[3];
my $overwrite = $q->param('Overwrite') || $ARGV[4] || 0;



#print "$upper $lower $relation $citation $overwrite\n";
#my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/implies/.my.cnf", "", "", {'AutoCommit'=>0});
my $dbh = DBI->connect('DBI:mysql:Zoo', 'root', 'implies') or
die "Couldn't open database: + $DBI::errstr; stopped";

if ($overwrite == 0){
	my $sql = 'INSERT INTO Theorems (the_Left, the_Relate, the_Right, the_Citation) VALUES(?, ?, ?, ?)';
	$sh = $dbh->prepare($sql);
    $cn = $sh->execute($upper, $relation, $lower, $citation);
    $sh->finish();
}
elsif ($overwrite == 2){
	$sql = 'delete from Theorems where the_Left = ? and the_Right = ? and the_Relate = ?';
	$sh = $dbh->prepare($sql);
    $cn = $sh->execute($upper, $lower, $relation);
    $sh->finish();
}

$dbh->disconnect();
