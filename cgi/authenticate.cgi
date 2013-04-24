#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;


print "content-type: text/html\n\n";

my $cgi = CGI->new;


my $username = $cgi->param("username") || $ARGV[0];
my $authkey = $cgi->param("authkey") || $ARGV[1];
my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";

my $sql = "select * from Users where username = ?
		AND authkey = ?"; 

my $sth = $dbh->prepare($sql);
my $c = $sth->execute($username, $authkey);
$sth->finish();

if($c != 0){
	$sql = "UPDATE Users
			SET status = '1'
			where username = ?
			and authkey = ?";
	$sth = $dbh->prepare($sql) or die $dbh->errstr;
	$c = $sth->execute($username, $authkey);
	$sth->finish();
	
	if($c != 0){
		print "Success";
	}
	else{
		print "Incorrect";
	}
}

else
{
	print "Incorrect";
}
$dbh->disconnect();

