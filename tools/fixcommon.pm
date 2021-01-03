#!/usr/bin/perl
use File::Basename;
use File::Slurp;
use URI::Encode qw(uri_encode uri_decode);

sub urlize($) {
  my ($label) = @_;
  $label = uri_decode($label);
  $label =~ s/ /-/g;
  $label =~ s/['"]//g;
  return lc $label;
}

sub traverse_raw($$$) {
  my ($dir,$pattern,$callback) = @_;

  for my $fname (<$dir/*>) {
    my $basename = basename($fname);
    if (-d $fname) {
      traverse_raw($fname,$pattern,$callback);
    } elsif ($basename =~ /$pattern/) {
      &$callback($fname);
    }
  }
}

1;
