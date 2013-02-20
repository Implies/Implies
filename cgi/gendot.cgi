#!/usr/bin/perl

use strict; 
use DBI; 
use CGI;
use JSON;
use DBD::mysql;


my $tmpdir = "dot/";
my $dotdir = "/home/implies/public_html/dot/";
#my $dotdir = "/home/ubuntu/public_html/html/dot/";
my $url = "http://reu.marshall.edu/~implies/dot/";
#my $url = "/localhost/ubuntu/dot/";
my $gvext = ".gv";
my $dotext = ".dot";


my $cgi = CGI->new();

print "content-type: text/html\n\n";


my $filename = "$$";
open (OUTFILE, ">", $dotdir . $filename . $gvext) or die "777 Can't open: $dotdir$filename$gvext  $!\n";   # FIXME
my $count = 0;
my $dbh = DBI->connect('DBI:mysql:Zoo', 'root', 'implies') or
die "Couldn't open database: + $DBI::errstr; stopped";
# my $sth = $dbh->prepare(<<End_SQL) or die "Couldn't prepare statement: + $DBI::errstr; stopped";


my $upper = $cgi->param('upper') || $ARGV[0] || 'ACA';
my $lower = $cgi->param('lower') || $ARGV[1] || 'WKL';

my $response = {};
$response->{'upper'} = $upper;
$response->{'lower'} = $lower;

# define queries
my $query0 = "SELECT Subsystems.sub_Ascii, Subsystems.sub_Latex FROM Subsystems;";

my $query1 = "select t0.exp_Left, t0.exp_Right, t0.exp_Relate
  from Expandedtheorems as t0
  join Expandedtheorems as ul
    on ul.exp_Left = ?
       and ul.exp_Right = t0.exp_Left
       and ul.exp_Relate = 'imply'
  join Expandedtheorems as ur
    on ur.exp_Left = ?
       and ur.exp_Right = t0.exp_Right
       and ur.exp_Relate = 'imply'
  join Expandedtheorems as ll
    on ll.exp_Right = ?
       and ll.exp_Left = t0.exp_Left
       and ll.exp_Relate = 'imply'
  join Expandedtheorems as lr
    on lr.exp_Right = ?
       and lr.exp_Left = t0.exp_Right
       and lr.exp_Relate = 'imply'
  where t0.exp_Left != t0.exp_Right ";


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
  $field2 =~ s!\\!\\\\!g;

     print OUTFILE "\"$field1\" [id =\"$field1\" label=\"\\\\($field2\\\\\)\" " 
                 . " href=\"javascript:void(click_node(\'$field1\'))\"];\n";    
     #$count++;
}

# prepare next query
$sth = $dbh->prepare($query1);

# execute query
$sth->execute($upper, $upper, $lower, $lower) or die "Couldn't execute statement: $DBI::errstr; stopped";

# Pull from Theorem Table
my ($left, $right, $relate);
while ( my ($left,$right, $relate,) = $sth->fetchrow_array() )
{    
  if ( $relate eq 'imply' ) { 
     print OUTFILE "\"$left\" -> \"$right\";\n";
     $count++;
  }
}

# Close Graphviz Brace
print OUTFILE "}";

# Compile
system("dot", "-Txdot", $dotdir . $filename . $gvext, "-o", $dotdir . $filename . $dotext);


# Disconnect from the database
$dbh->disconnect();

$response->{'dotfileurl'} = $tmpdir . $filename . $dotext;


print to_json($response, {pretty => 1}); 
