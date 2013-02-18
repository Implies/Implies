#!/usr/bin/perl

use strict; 
use DBI; 
use CGI;
use DBD::mysql;


my $length = @ARGV;

my $cgi = CGI->new();

#print "$length";

print "content-type: text/html\n\n";

#my $x = $cgi->param('a') || $ARGV[0];

my $filename = "default.gv";
open (OUTFILE, ">", $filename);
my $count = 0;
my $dbh = DBI->connect('DBI:mysql:Zoo', 'root', 'implies') or
die "Couldn't open database: + $DBI::errstr; stopped";
# my $sth = $dbh->prepare(<<End_SQL) or die "Couldn't prepare statement: + $DBI::errstr; stopped";


my $sub0 = $ARGV[0];
my $sub1 = $ARGV[1];

print $sub0;
print $sub1;


# define queries
my $query0 = "SELECT Subsystems.sub_Ascii, Subsystems.sub_Latex FROM Subsystems;";
#my $query1 = "SELECT Theorems.the_Left, Theorems.the_Right FROM Theorems;";

#my $query2 = "SELECT T0.the_Left AS Top, T1.the_Right AS 1st, T2.the_Right AS 2nd, T3.the_Right AS Bottom
#FROM Theorems AS T0 JOIN Theorems AS T1 JOIN Theorems AS T2 JOIN Theorems AS T3
#WHERE T0.the_Left = '$sub0' && T0.the_Right = T1.the_Left && T1.the_Right = T2.the_Left && T2.the_Right = T3.the_Left && T3.the_Right LIKE '%';";

my $query1 = "SELECT T0.Exp_Left, T0.Exp_Right, T1.Exp_Right FROM Expandedtheorems AS T0 JOIN Expandedtheorems AS T1 ON T0.exp_Right = T1.exp_Left AND T0.exp_Left = 'ACA';";

#my $md5String = "";

# Graphviz Header
print OUTFILE "digraph G {\n node [shape=none, margin=0];\n \n";

# prepare first query

my $sth = $dbh->prepare($query0);

# Execute the query
$sth->execute() or die "Couldn't execute statement: $DBI::errstr; stopped";

# Pull from Subsystem Table
while ( my ($field1, $field2,) = $sth->fetchrow_array() )
{
     print OUTFILE "\"$field1\" [id =\"$field1\" label=\"\$\\\\mathsf{$field1}_0\$\" href=\"javascript:void(click_node(\'\$\\\\mathsf{$field2}_0\$\'))\"];\n";    
     #$count++;
}

# prepare next query
$sth = $dbh->prepare($query1);

# execute query
$sth->execute() or die "Couldn't execute statement: $DBI::errstr; stopped";

# Pull from Theorem Table
while ( my ($field3, $field4,) = $sth->fetchrow_array() )
{    
     print OUTFILE "\"$field3\" -> \"$field4\";\n";
     $count++;
}

# Close Graphviz Brace
print OUTFILE "}";

# Compile
system("dot -Txdot default.gv -o /home/ubuntu/public_html/demo/default.dot");


# Disconnect from the database
$dbh->disconnect();
