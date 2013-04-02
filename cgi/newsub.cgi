#!/usr/bin/perl

use CGI;
use DBI;

print "content-type: text/plain\n\n";

$q=new CGI;

$ASCIIName = $q->param('ASCIIName') || $ARGV[0];
$LaTexName = $q->param('LaTexName') || $ARGV[2];
$Reference = $q->param('Reference') || $ARGV[3];
$FreeText = $q->param('FreeText')   || $ARGV[4];
$Overwrite = $q->param('Overwrite') || $ARGV[1] || 0;

my $date = `/bin/date`;
chomp $date;
open MYFILE, '>>', "/tmp/log.txt" or die $!;
print MYFILE "$date $ASCIIName\t $LaTexName\t $Reference\t $FreeText\n";
close MYFILE;

$dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

$sql = "select * from Subsystems where sub_Ascii = ?";  # because sub_Ascii is a unique key
$sh = $dbh->prepare($sql);
$c = $sh->execute($ASCIIName);
$sh->finish();

if ( $c == 0) {
  # insert
  $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";

  $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
  my $c = $sth->execute($ASCIIName, $LaTexName, $Reference, $FreeText);
  print "Added\n";
} 
elsif( $Overwrite > 0 )
{
		#print "Deleting \n";
	#print $Overwrite;
	#print $ASCIIName;
    #Delete the row
    $sql = "delete from Subsystems where sub_Ascii = ?";
    $sh = $dbh->prepare($sql);
    $cn = $sh->execute($ASCIIName);
    $sh->finish();
    print ("Deleted\n");
    
  if ($Overwrite == 1) 
  {
	      # read to update the row

	
    $sql = "INSERT INTO Subsystems VALUES(?, ?, ?, ?)";
    $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
    $sth->execute($ASCIIName, $LaTexName, $Reference, $FreeText) or die "Connection Error: $dbh->errstr";

    print "Updated\n";

  }
}
else
{
	print "Duplicate\n"
}


$dbh->disconnect();
