#!/usr/bin/perl

use CGI;
use DBI;

$q=new CGI;

$Left = $q->param('Left');
$Right = $q->param('Right');
$Relate = $q->param('Relate');
$Citation = $q->param('Citation');

my $dbh=DBI->connect("DBI:mysql:database=Zoo;mysql_read_default_file=/home/mummertc/.my.cnf", "", "", {'AutoCommit'=>0});

sub populate{
	$sql = "SELECT sub_Ascii FROM Subsystems; ";
		
	$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
	$sth->execute();
}
sub result{
	$sql = "IF EXISTS(SELECT * FROM References WHERE ref_Citation=?) BEGIN
	INSERT INTO Theorems(the_Left, the_Right, the_Relate, the_Citation)
	VALUES(?, ?, ?, ?) ON DUPLICATE KEY UPDATE
	END;";
	$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
	$sth->execute($Citation, $Left, $Right, $Relate, $Citation);
}
print "content-type: text/html\n\n";
