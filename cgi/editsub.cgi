#!/usr/bin/perl

use DBI; 
use CGI;
use strict; 
use warnings;
use JSON;

my $cgi = CGI->new();

print "content-type: text/html\n\n";

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";
my $sql = "SELECT * FROM Subsystems;";
my $sth = $dbh->prepare($sql);
$sth->execute() or die "Couldn't execute statement: $DBI::errstr; stopped";
$sth->finish();
my $data = [];
 
# Pull from Subsystem Table
while ( my ($field1, $field2, $field3, $field4,) = $sth->fetchrow_array() )
{
   push @$data, [$field1, $field2, $field3, $field4];
}

print to_json($data, {pretty => 1});   # print out the data structure in JSON
