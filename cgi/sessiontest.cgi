#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;

print "content-type: text/html\n\n";


my $cgi = CGI->new;
my $sesID = $cgi->param("sessionID") || $ARGV[0] || "Õf1ífk0*˜dçÂØwðta;âb ";

my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

my $sql = sprintf "select * from Sessions where sesID = %s;", 
    $dbh->quote($sesID);
my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
my $c = $sth->execute();
if($c != 0) {
    print "Session";
}
else{
	print "No session";
}
