#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;

print "content-type: text/html\n\n";

my $cgi = CGI->new;
my $sesID = $cgi->param("sessionID") || $ARGV[0];

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";

my $sql = sprintf "select * from Sessions where sesID = %s;", 
    $dbh->quote($sesID);
my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
my $c = $sth->execute();
$sth->finish();

if($c != 0) {
    print "Session";
}
else{
	print "No session";
}
