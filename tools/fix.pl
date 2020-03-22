#!/usr/bin/perl
use File::Basename;
use File::Slurp;
use URI::Encode qw(uri_encode uri_decode);

our $count = 0;

sub urlize($) {
  my ($label) = @_;
  $label = uri_decode($label);
  $label =~ s/ /-/g;
  $label =~ s/['"]//g;
  return lc $label;
}

sub fix_links($) {
  my ($fname) = @_;

  my $html  = read_file($fname);
  my $fixed = $html;

  $fixed =~ s#http://blog.ioshints.info#https://blog.ipspace.net#gi;
  $fixed =~ s#http://ioshints.blogspot.com#https://blog.ipspace.net#gi;
  $fixed =~ s#https://blog.ipspace.net/2006/01/contact-me.html#https://www.ipspace.net/Contact#gi;
  $fixed =~ s#/search/label/([^'"]+)#"/tag/".urlize($1).".html"#gie;
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

sub traverse($$$) {
  my ($dir,$pattern,$callback) = @_;

  for my $fname (<$dir/*>) {
    my $basename = basename($fname);
    if (-d $fname) {
      traverse($fname,$pattern,$callback);
    } elsif ($basename =~ /$pattern/) {
      &$callback($fname);
    }
  }
}

traverse($ARGV[0],".html",\&fix_links);
print "Fixed $count files\n";
