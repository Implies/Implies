#!/usr/bin/perl
use CGI;
use DBI;
use strict;
use warnings;
use Digest::SHA qw(sha1_hex);
use Email::MIME;
use Email::Sender::Simple qw(sendmail);

print "content-type: text/html\n\n";

sub sendEmail
 {
	my ($to, $from, $subject, $message) = @_;
	$message = Email::MIME->create(
	header_str => [
		From    => $from,
		To      => $to,
		Subject => $subject,
	  ],
	  attributes => {
		encoding => 'quoted-printable',
		charset  => 'ISO-8859-1',
	  },
	  body_str => $message,
	);

	# send the message
	use Email::Sender::Simple qw(sendmail);
	sendmail($message);
 } 
 
my $cgi = CGI->new;
my $email = $cgi->param("email") || $ARGV[0];
my $username = $cgi->param("username") || $ARGV[1];
my $password = $cgi->param("password") || $ARGV[2];
my $digest = sha1_hex($password);

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";

## Test to see if the username already exists
my $sql = "SELECT * FROM Users WHERE username=?";
my $sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
my $c = $sth->execute($username);
$sth->finish();
## It's a unique username
if ($c == 0)
	{
		my @chars = ('0'..'9', 'A'..'Z');
		my $len = 8;
		my $authkey;
		while($len--){ $authkey .= $chars[rand @chars] };
		
		my $sth;
		$sql = "INSERT INTO Users VALUES (?, ?, ?, ?, ?)";
		
		$sth = $dbh->prepare($sql) or die "Can't prepare $sql: $dbh->errstrn";
		$c = $sth->execute( $username, $digest, "", $authkey, $email);
		$sth->finish();
		print "Success New";
		# sendEmail("$username", "implies\@reu.marshall.edu", 
		#	"Email authentication for IMPLIES", "Your authentication code for IMPLIES:"."$authkey");
	}
	
## Username has already been taken
else 
	{
		print "Duplicate"	
	}
	
$dbh->disconnect();
