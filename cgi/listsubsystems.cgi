#!/usr/bin/perl

use strict; 
use DBI; 
use CGI;
use DBD::mysql;
use JSON;

my $cgi = CGI->new();

print "content-type: text/html\n\n";

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";
   
#my $query = "SELECT t2.sub_Ascii, t2.sub_Latex, t2.sub_FreeText "
#		    . "FROM Subsystems AS t0 "
#            . "JOIN Theorems AS t1 ON t1.the_Left = t0.sub_Ascii "
#            . "JOIN Subsystems AS t2 ON t1.the_Right = t2.sub_Ascii;";

my $query = "SELECT * FROM Subsystems;";

# prepare first query
my $sth = $dbh->prepare($query);

$sth->execute() or die "Couldn't execute statement: $DBI::errstr; stopped";


my $names = {};   # hash reference
my $tex = {};
my $cite = {};
my $data = [];
 
# Pull from Subsystem Table
while ( my ($field1, $field2, $field3) = $sth->fetchrow_array() )
{
   push @$data, [$field1, $field2, $field3];
}

$sth->finish();

print to_json($data, {pretty => 1});   # print out the data structure in JSON
$dbh->disconnect();
