#!/usr/bin/perl

use strict;
use DBI;

my $filename = "Zoo.xml";
my $xmldir = "/home/implies/public_html/html/";

open (OUTFILE, ">", $xmldir . $filename);

my $dbh = DBI->connect('DBI:mysql:Zoo', 'root', 'implies') or
die "Couldn't open database: + $DBI::errstr; stopped";

print OUTFILE "<?xml version=\"1.0\"?>\n";
print OUTFILE "<zoo>\n";

my $sql = "SELECT * FROM Subsystems";
my $sth = $dbh->prepare ($sql);
$sth->execute ();

print OUTFILE " <subsystems>\n";

while (my ($name, $latex, $freetext, $citation) = $sth->fetchrow_array ())
{
    print OUTFILE "   <subsystem>\n";
    print OUTFILE "    <name>" . $name . "</name>\n";
    print OUTFILE "    <latex>" . $latex  . "</latex>\n";
    print OUTFILE "    <freetext>" . $freetext . "</freetext>\n";
    print OUTFILE "    <citation>" . $citation . "</citation>\n";
    print OUTFILE "   </subsystem>\n";
}
    print OUTFILE "  </subsystems>\n";

my $sql = "SELECT * FROM Theorems";
my $sth = $dbh->prepare ($sql);
$sth->execute ();

    print OUTFILE "  <theorems>\n";

while (my ($left, $relate, $right, $citation) = $sth->fetchrow_array ())
{
    print OUTFILE "   <theorem>\n";
    print OUTFILE "    <left>" . $left . "</left>\n";
    print OUTFILE "    <relate>" . $relate  . "</relate>\n";
    print OUTFILE "    <right>" . $right . "</right>\n";
    print OUTFILE "    <citation>" . $citation . "</citation>\n";
    print OUTFILE "   </theorem>\n";
}
    print OUTFILE "  </theorems>\n";

my $sql = "SELECT * FROM Citations";
my $sth = $dbh->prepare ($sql);
$sth->execute ();

    print OUTFILE "  <bibliography>\n";

while (my ($key, $mrn, $freetext) = $sth->fetchrow_array ())
{
    print OUTFILE "   <citation>\n";
    print OUTFILE "    <key>" . $key . "</key>\n";
    print OUTFILE "    <mrn>" . $mrn  . "</mrn>\n";
    print OUTFILE "    <freetext>" . $freetext . "</freetext>\n";
    print OUTFILE "   </citation>\n";
}
    print OUTFILE "  </bibliography>\n";

$dbh->disconnect ();
print OUTFILE "</zoo>\n";
