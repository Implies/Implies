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
##$Citation = $q->param('Citation');

if($relation eq "Implies"){
		$relation = "imply";
	}
else{
		$relation = "notimply";
	}

my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/mummertc/.my.cnf", "", "", {'AutoCommit'=>0});

my $sql = "INSERT INTO Theorems(?, ?, ?) ON DUPLICATE KEY UPDATE;";
my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
$sth->execute($upper, $lower, $relation);

if ($sth)
{
	print "Success";
}

