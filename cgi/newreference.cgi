#!/usr/bin/perl

use CGI;
use DBI;
use Data::Dumper;
use strict;

print "content-type: text/plain\n\n";

my $q=new CGI;

my $Key = $q->param('KeyName') || $ARGV[0];
my $MRNumber = $q->param('MRNumber') || $ARGV[1];
my $FreeText = $q->param('FreeText') || $ARGV[2];

my $date = `/bin/date`;
chomp $date;
open MYFILE, '>>', "/tmp/log.txt" or die $!;
print MYFILE "$date $Key\t $MRNumber\t $FreeText\n";
close MYFILE;

my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/mummertc/.my.cnf", "", "", {'AutoCommit'=>0});

my $sql = "select * from Citations where ref_Citation = ?"; #ref_Citation is the primary key
my $sh = $dbh->prepare($sql);


my $c = $sh->execute($Key);


$sh->finish();

if ($c == 0)
	{
my $sth;
		$sql = "INSERT INTO Citations VALUES (?, ?, ?)";
		
		$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
		my $c = $sth->execute($Key, $MRNumber, $FreeText);
		print "Success\n";
	}
else 
	{
		print "Duplicate\n"	
	}


$dbh->disconnect();

