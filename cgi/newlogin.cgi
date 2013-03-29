#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;
use Digest::SHA qw(sha1);

print "content-type: text/html\n\n";

sub sendEmail
 {
 	my ($to, $from, $subject, $message) = @_;
 	my $sendmail = '/usr/lib/sendmail';
 	open(MAIL, "|$sendmail -oi -t");
 		print MAIL "From: $from\n";
 		print MAIL "To: $to\n";
 		print MAIL "Subject: $subject\n\n";
 		print MAIL "$message\n";
 	close(MAIL);
 } 
 
my $cgi = CGI->new;
my $username = $cgi->param("username") || $ARGV[0];
my $password = $cgi->param("password") || $ARGV[1];
my $digest = sha1($password);

my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

## Test to see if the username already exists
my $sql = "SELECT * FROM Users WHERE username=?";
my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
my $c = $sth->execute($username);

## It's a unique username
if ($c == 0)
	{
		my @chars = ('0'..'9', 'A'..'Z');
		my $len = 8;
		my $authkey;
		while($len--){ $authkey .= $chars[rand @chars] };
		
		my $sth;
		$sql = "INSERT INTO Users VALUES (?, ?, ?, ?)";
		
		$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
		$c = $sth->execute( $username, $digest, "", $authkey);
		print "Success New";
		 sendEmail("$username", "implies\@reu.marshall.edu", 
			"Email authentication for IMPLIES", "$authkey");
	}
	
## Username has already been taken
else 
	{
		print "Duplicate"	
	}
	
