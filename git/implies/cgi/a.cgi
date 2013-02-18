#!/usr/bin/perl

use CGI;

my $cgi = CGI->new();

print "content-type: text/html\n\n";


my $x = $cgi->param('a') || $ARGV[0];

print "Hi $x$x\n";


