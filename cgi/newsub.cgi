#!/usr/bin/perl

use CGI;
use DBI;

print "content-type: text/plain\n\n";

$q=new CGI;

$ASCIIName = $q->param('ASCIIName') || $ARGV[0] || undef;
$Overwrite = $q->param('Overwrite') || $ARGV[1] || 0;
$LaTexName = $q->param('LaTexName') || $ARGV[2] || undef;
$Reference = $q->param('Reference') || $ARGV[3] || undef;
$FreeText  = $q->param('FreeText')  || $ARGV[4] || undef;

my $date = `/bin/date`;
chomp $date;
open MYFILE, '>>', "/tmp/log.txt" or die $!;
print MYFILE "$date $ASCIIName\t $LaTexName\t $Reference\t $FreeText\n";
close MYFILE;

my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/implies/.my.cnf", "", "", {'AutoCommit'=>0})
or die "Can't connect: $!\n";

$sql = "select * from Subsystems where sub_Ascii = ?"; # because sub_Ascii is a unique key
$sh = $dbh->prepare($sql);
$c = $sh->execute($ASCIIName);
$sh->finish();

if ( $c == 0) {
 # insert
  $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";
  $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
  $sth->execute($ASCIIName, $LaTexName, $Reference, $FreeText) or die "Connection Error: $dbh->errstr";

  print "Success\n";
} else
{
    #Delete the row
    $sql = "DELETE FROM Subsystems WHERE sub_Ascii = ?";
    $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
    $sth->execute($ASCIIName) or die "Connection Error: $dbh->errstr";

  if ( 1 == $Overwrite )
  {
    # readd to update the row
    #$sql = "DELETE FROM Subsystems WHERE sub_Ascii = ?";
    #$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
    #$sth->execute($ASCIIName) or die "Connection Error: $dbh->errstr";

    $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";
    $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
    $sth->execute($ASCIIName, $LaTexName, $Reference, $FreeText) or die "Connection Error: $dbh->errstr";

    print "Success\n";
   }
}

  #} else {
    # it's a duplicate, send error
    #print "Duplicate\n";
  #}



$dbh->disconnect();
