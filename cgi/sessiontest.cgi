#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;

print "content-type: text/html\n\n";


my $cgi = CGI->new;
my $sessionID = $cgi->param("sessionID") || $ARGV[0];


my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

my $sql = "select * from Sessions WHERE sesID =?";
my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
my $c = $sth->execute($sessionID);

if ($c == 0){
	print "No session";
}
else{
	print "Session";
}
