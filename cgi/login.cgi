#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;
use Digest::SHA qw(sha1);
print "content-type: text/html\n\n";

my $cgi = CGI->new;
my $username = $cgi->param("username") || $ARGV[0];
my $password = $cgi->param("password") || $ARGV[1];
my $sesID = sha1($username.$password);
print $sesID;
## connect to the database
my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

my $sql = "SELECT password FROM Users WHERE username=?";
my $sth = $dbh->prepare($sql)
  or die $dbh->errstr;
my $c = $sth->execute($username);

## if there is a match for the username
if ($c != 0)
	{

		my $digest = sha1($password);
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
			$sql = "INSET INTO Sessions values(?,?,?,?)";
			print "Success";
		}

	}
	
## If the user doesn't exist
else 
	{
		print "Incorrect"	
	}
