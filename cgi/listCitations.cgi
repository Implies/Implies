#!/usr/bin/perl

use CGI;
use DBI;
use JSON;
use strict;
use Data::Dumper;

print "content-type: text/plain\n\n";
my $q=new CGI;
my $search = $q->param('search') || $ARGV[0] || "";
my $sql = "select ref_Citation, ref_MRNumber, ref_FreeText from Citations";
if ( 0 <  length $search  ) {
  $sql .= " where ref_FreeText like ?";
}

my $dbh=DBI->connect("DBI:mysql:database=Zoo;" 
             . "mysql_read_default_file=/home/implies/.my.cnf", 
               "", "", {'AutoCommit'=>0}),
   or die "Can't connect: $!\n";

my $sth = $dbh->prepare($sql);


my $count;
if ( 0 < length $search ) {
  $count = $sth->execute('%' . $search . '%');
  $sth->finish();
} else {
  $count = $sth->execute();
  $sth->finish();
}


my $data = {};

if ( $count eq '0E0' ) {
  $count = 0;
}
$data->{'count'} = $count;
$data->{'results'} = [];

my $r;
while ( $r = $sth->fetchrow_arrayref() ) {
  push @{$data->{'results'}}, [$r->[0], $r->[1], $r->[2]];
}


print to_json($data, {'pretty'=>1});
$dbh->disconnect();
