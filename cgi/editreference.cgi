#!/usr/bin/perl

use CGI;
use DBI;
use Data::Dumper;
#use strict;

print "content-type: text/plain\n\n";

my $q=new CGI;

$Key       = $q->param('KeyName')   || $ARGV[0];
$MRNumber  = $q->param('MRNumber')  || $ARGV[2] || 0;
$FreeText  = $q->param('FreeText')  || $ARGV[3] || 0;
$Overwrite = $q->param('Overwrite') || $ARGV[1] || 0;

print $Key . "\n";
print $Overwrite . "\n";

my $date = `/bin/date`;
chomp $date;
open MYFILE, '>>', "/tmp/log.txt" or die $!;
print MYFILE "$date $ASCIIName\t $LaTexName\t $Reference\t $FreeText\n";
close MYFILE;

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";

$sql = "select * from Citations where ref_Citation = ?";
$sh = $dbh->prepare($sql);

$c = $sh->execute($Key);

#exit;

$sh->finish();

#print "here\n";

if ($c == 0)
{
	$sql = "INSERT INTO Citations VALUES(?, ?, ?)";		
	$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
	$c = $sth->execute($Key, $MRNumber, $FreeText);
	print "Success\n";
}
elsif( $Overwrite > 0)
{
    $sql = "DELETE FROM Citations WHERE ref_Citation = ?";
    print $sql . "\n";
    $sh = $dbh->prepare($sql);
    $cn = $sh->execute($Key);
    $sh->finish();
    
  if ( $Overwrite == 1 )
  {
	print "Adding\n";
    $sql = "INSERT INTO Citations VALUES(?, ?, ?)";		
	$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
    $sth->execute($Key, $MRNumber, $FreeText) or die "Connection Error: $dbh->errstr";

    print "Success\n";
   }
   
   if ($cn > 0)
   {
	   print "Deleted\n";
   }
}

$dbh->disconnect();
