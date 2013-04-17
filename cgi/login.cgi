#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;
use Digest::SHA qw(sha1_hex);
use POSIX qw/strftime/;
print "content-type: text/html\n\n";

my $cgi = CGI->new;
my $username = $cgi->param("username") || $ARGV[0];
my $password = $cgi->param("password") || $ARGV[1];
my $date = strftime("%Y-%m-%d", localtime);
my $sesID = sha1_hex($username.$password);

## connect to the database
my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

my $sql = "SELECT password FROM Users WHERE username=?";
my $sth = $dbh->prepare($sql)
  or die $dbh->errstr;
my $c = $sth->execute($username);

## if there is a match for the username
if ($c != 0)
	{

		my $digest = sha1_hex($password);
		my $sql = "SELECT * FROM Users WHERE username=? AND password=?";
		
		$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
		my $test = $sth->execute($username, $digest);
		
		## pair did not exist
		if($test == 0)
		{
			print "Incorrect";
		}
		## successful login
		else
		{
			$sql = "DELETE FROM Sessions WHERE username=?";
			$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
			$test = $sth->execute($username);
			$sql = "INSERT INTO Sessions VALUES (?,?,?)";
			$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
			$test = $sth->execute($username, $date, $sesID);
			print "$sesID";
		}

	}
	
## If the user doesn't exist
else 
	{
		print "Incorrect"	
	}
