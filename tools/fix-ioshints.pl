#!/usr/bin/perl
BEGIN {
  use File::Basename;
  push @INC,dirname(__FILE__);
}

use File::Slurp;
use URI::Encode qw(uri_encode uri_decode);
use fixcommon;

our $count = 0;

sub fix_ioshints($) {
  my ($fname) = @_;

  my $html  = read_file($fname);
  my $fixed = $html;

  $fixed =~ s#http://www.ioshints.info#https://www.ipspace.net#gi;
  $fixed =~ s#Subscription_to_ioshints_webinars#Subscription#gi;
  $fixed =~ s#/about/send.php#/Contact#gi;
#  $fixed =~ s#/search/label/#/tag#gi;
  if ($fixed ne $html) {
    print "Fixing $fname\n";
    write_file($fname,$fixed);
    $count++;
    if ($count > 50) {
      print "Enough...\n"; exit;
    }
  }
}

traverse_raw($ARGV[0] || ".",".html",\&fix_ioshints);
print "Fixed $count files\n";
