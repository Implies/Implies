#!/usr/bin/perl
use Data::Dumper;

use strict; 
use DBI; 
use CGI;
use JSON;
use DBD::mysql;

#my $tmpdir = "dot/";
my $xmldir = "/home/implies/public_html/xml/";
#my $xmldir = "/home/ubuntu/public_html/html/dot/";
my $url = "http://reu.marshall.edu/~implies/dot/";
#my $url = "/localhost/ubuntu/dot/";
my $xmlext = ".xml";

my %tex = [];
my %data;# = {};
my $cgi = CGI->new();

print "content-type: text/html\n\n";

#my $upper = $cgi->param('upper') || $ARGV[0] || 'ACA';
#my $lower = $cgi->param('lower') || $ARGV[1] || 'WKL';
#my $filename = $upper. "_". $lower;


#my $filename = "$$";
open (OUTFILE, ">", $xmldir . $filename . $gvext) or die "777 Can't open: $xmldir$filename$xmlext  $!\n";   # FIXME
my $count = 0;
my $dbh = DBI->connect('DBI:mysql:Zoo', 'root', 'implies') or
die "Couldn't open database: + $DBI::errstr; stopped";
# my $sth = $dbh->prepare(<<End_SQL) or die "Couldn't prepare statement: + $DBI::errstr; stopped";


#my $response = {};
#$response->{'upper'} = $upper;
#$response->{'lower'} = $lower;

# define queries
my $query0 = "SELECT cd ..Subsystems.sub_Ascii, Subsystems.sub_Latex FROM Subsystems;";

# prepare first query
my $sth = $dbh->prepare($query0);

# Execute the query
$sth->execute() or die "Couldn't execute statement: $DBI::errstr; stopped";
#$sth->execute($upper, $upper, $lower, $lower) or die "Couldn't execute statement: $DBI::errstr; stopped";

# Pull from Subsystem Table
while ( my ($field1, $field2,) = $sth->fetchrow_array() )
{
  $field2 =~ s!\\!\\\\!g;
   $tex{$field1} = $field2;
}

# prepare next query
my $sth = $dbh->prepare($query1);

# execute query
$sth->execute($upper, $upper, $lower, $lower) or die "Couldn't execute statement: $DBI::errstr; stopped";

my $database = {};

# Pull from Theorem Table
my ($left, $right, $relate, $reason);
while ( my ($left,$right, $relate, $reason) = $sth->fetchrow_array() )
{    
  #print "$left $relate $right \n";

  if ( $relate eq 'imply' ) { 

    my $sys = get_system($database, $left);
    $sys->{'children'}->{$right} = 1;
    
    $sys = get_system($database, $right);
    $sys->{'parents'}->{$left} = 1;
  }

} 
my ($node, $parent, $child);

foreach $node ( keys %$database ) { 
  foreach $parent ( keys %{$database->{$node}->{'parents'}} ) { 
    foreach $child ( keys %{$database->{$parent}->{'children'}} ) { 

        #print "N: $node P: $parent C: $child\n";
   
       if ( exists $database->{$child}->{'children'}->{$node} ) { 
		#print ".. delete\n";

           delete $database->{$parent}->{'children'}->{$node};
           delete $database->{$node}->{'parents'}->{$parent};
       }
    }
  }
}


#print Dumper($database);

sub get_system { 
  my $database = shift;
  my $system = shift;

  if ( ! ( exists $database->{$system} ) ) { 
    $database->{$system} = {};
    $database->{$system}->{'name'} = $system;
    $database->{$system}->{'latexname'} = $tex{$system};
    $database->{$system}->{'parents'} = {};
    $database->{$system}->{'children'} = {};
  }

  return $database->{$system};
}

# Graphviz Header
print OUTFILE "digraph G" . "\n" . "{graph[ratio=.5]" . "\n"
			 . "\n" . "{node [shape=none, margin=0];" . "\n \n";

for $node ( values $database ) { 

  #print "N " . $node->{'name'} . " L " . $node->{'latexname'} . "\n";
	
  my $key;
  foreach $key (keys $node->{'children'})
  {
     print OUTFILE "\"" . $node->{'name'} . "\"" . " -> " . "\"" . "$key"  . "\"" . "[weight=0]" . ";" . "\n";
  }

  print OUTFILE "\"" . $node->{'name'} . "\"" 
		. ' [id ="' . $node->{'name'} . '" '
        . 'label="' . "\\\\" . "(" . $node->{'latexname'} . "\\\\" . ")" . '" ' 
        . ' href="javascript:void(click_node(' . "'" . $node->{'name'} . "'" . '))"];' . "\n";
}

# Close Graphviz Brace
print OUTFILE "}";
print OUTFILE "}";

# Compile
system("dot", "-Txdot", $xmldir . $filename . $xmlext, "-o", $xmldir . $filename . $xmlext);

# Disconnect from the database
$dbh->disconnect();

