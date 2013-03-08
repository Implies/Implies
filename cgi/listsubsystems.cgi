#!/usr/bin/perl

use strict; 
use DBI; 
use CGI;
use DBD::mysql;
use JSON;

my $cgi = CGI->new();

print "content-type: text/html\n\n";

#my $x = $cgi->param('a') || $ARGV[0];

my $dbh = DBI->connect('DBI:mysql:Zoo', 'root', 'implies') or
die "Couldn't open database: + $DBI::errstr; stopped";
# my $sth = $dbh->prepare(<<End_SQL) or die "Couldn't prepare statement: + $DBI::errstr; stopped";

my $query0 = "SELECT Subsystems.sub_Ascii, Subsystems.sub_Latex, Subsystems.sub_FreeText FROM Subsystems";

# prepare first query
my $sth = $dbh->prepare($query0);

# Execute the query
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

print to_json($data, {pretty => 1});   # print out the data structure in JSON
