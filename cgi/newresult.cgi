#!/usr/bin/perl

use CGI;
use DBI;
use strict;
use warnings;

print "content-type: text/html\n\n";

my $q=new CGI;
my $upper = $q->param('upper') || $ARGV[0];
my $lower = $q->param('lower') || $ARGV[1];
my $relation = $q->param('relation') || $ARGV[2];
my $citation = $q->param('citation') || $ARGV[3];

#if($relation eq "imply"){
#		$relation = "imply";
#	}
#else{
#		$relation = "notimply";
#	}

print "$upper $lower $relation $citation \n";
my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/mummertc/.my.cnf", "", "", {'AutoCommit'=>0});

my $sql = 'INSERT INTO Theorems VALUES(?, ?, ?, ?)';

my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
$sth->execute($upper, $lower, $relation, $citation) or die "Couldn't execute statement: $DBI::errstr; stopped";


my $count = $dbh->do ($sql);

print "$count \n";

$dbh->disconnect();
