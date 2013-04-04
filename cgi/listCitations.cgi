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

my $dbh=DBI->connect('dbi:mysql:Zoo','root','implies');

my $sh = $dbh->prepare($sql);


my $count;
if ( 0 < length $search ) {
  $count = $sh->execute('%' . $search . '%');
} else {
  $count = $sh->execute();
}


my $data = {};

if ( $count eq '0E0' ) {
  $count = 0;
}
$data->{'count'} = $count;
$data->{'results'} = [];

my $r;
while ( $r = $sh->fetchrow_arrayref() ) {
  push @{$data->{'results'}}, [$r->[0], $r->[1], $r->[2]];
}


print to_json($data, {'pretty'=>1});
$dbh->disconnect();
