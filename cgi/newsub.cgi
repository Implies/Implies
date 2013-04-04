#!/usr/bin/perl

use CGI;
use DBI;
use strict;

print "content-type: text/plain\n\n";

my $q=new CGI;

my $ASCIIName = $q->param('ASCIIName') || $ARGV[0];
my $LaTexName = $q->param('LaTexName') || $ARGV[2] || 0;
my $Reference = $q->param('Reference') || $ARGV[3] || 0;
my $FreeText = $q->param('FreeText')   || $ARGV[4] || 0;
my $Overwrite = $q->param('Overwrite') || $ARGV[1] || 0;

my $date = `/bin/date`;
chomp $date;
open MYFILE, '>>', "/tmp/log.txt" or die $!;
print MYFILE "$date $ASCIIName\t $LaTexName\t $Reference\t $FreeText\n";
close MYFILE;

my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

my $sql = "select * from Subsystems where sub_Ascii = ?";  # because sub_Ascii is a unique key
my $sh = $dbh->prepare($sql);
my $c = $sh->execute($ASCIIName);
$sh->finish();

if ( $c == 0) {
  # insert
  $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";

  $sh = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
  $sh->execute($ASCIIName, $LaTexName, $Reference, $FreeText);
  print "Added\n";
} 
elsif( $Overwrite > 0 )
{
    $sql = "delete from Subsystems where sub_Ascii = ?";
    $sh = $dbh->prepare($sql);
    $sh->execute($ASCIIName);
    $sh->finish();
    print ("Deleted\n");
    
  if ($Overwrite == 1) 
  {
    $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";
    $sh = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
    $sh->execute($ASCIIName, $LaTexName, $Reference, $FreeText) or die "Connection Error: $dbh->errstr";
    print "Updated\n";

  }
}
else
{
	print "Duplicate\n"
}


$dbh->disconnect();
