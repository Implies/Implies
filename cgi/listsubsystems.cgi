#!/usr/bin/perl

use strict; 
use DBI; 
use CGI;
use DBD::mysql;
use JSON;

my $cgi = CGI->new();

print "content-type: text/html\n\n";

my $x = $cgi->param('a') || $ARGV[0];
my $y = $cgi->param('b') || $ARGV[1];

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";
my $query;
if($x)
{
   if($y)
   {
      $query = "SELECT t2.sub_Ascii, t2.sub_Latex, t2.sub_FreeText FROM Subsystems AS t0 
                JOIN Theorems AS t1 ON t1.the_Left = t0.sub_Ascii 
                JOIN Subsystems AS t2 ON t1.the_Right = t2.sub_Ascii WHERE t0.sub_Ascii = ?";
   }
   else
   {
      $query = "SELECT Subsystems.sub_Ascii, Subsystems.sub_Latex, Subsystems.sub_FreeText FROM Subsystems
                WHERE Subsystems.sub_Ascii = ?";
   }
   

   #$query = "SELECT Subsystems.sub_Ascii, Subsystems.sub_Latex, Subsystems.sub_FreeText FROM 
   #	     WHERE Subsystems.sub_Ascii = ?";
}
else
{
   $query = "SELECT Subsystems.sub_Ascii, Subsystems.sub_Latex, Subsystems.sub_FreeText FROM Subsystems";
}


# prepare first query
my $sth = $dbh->prepare($query);

# Execute the query
if($x)
{ 
   $sth->execute(@ARGV[0]) or die "Couldn't execute statement: $DBI::errstr; stopped";
   $sth->finish();
}
else
{
   $sth->execute() or die "Couldn't execute statement: $DBI::errstr; stopped";
   $sth->finish();
}

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
