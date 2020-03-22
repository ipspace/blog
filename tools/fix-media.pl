#!/usr/bin/perl
use File::Basename;
use File::Slurp;
use URI::Encode qw(uri_encode uri_decode);
use Data::Dumper;
use YAML::XS;

our $count = 0;

sub urlize($) {
  my ($label) = @_;
  $label = uri_decode($label);
  $label =~ s/ /-/g;
  $label =~ s/['"]//g;
  return lc $label;
}

sub fix_media($) {
  my ($data) = @_;

  return unless $data->{media};
  return if $data->{media} =~ /.mp3/;
  delete $data->{media};
  $data->{tags} = [ map { $_ =~ /podcast/i ? () : $_ } @{$data->{tags}} ];
  return 1;
}

sub fix_data($$) {
  my ($fname,$callback) = @_;

  my $original = read_file($fname);
  my @parts = split /---\n/,$original;

  my $yaml = $parts[1];
  my $html = $parts[2];
  my $data = $result = YAML::XS::Load($yaml);

  return unless &$callback($data);

  $fixed = YAML::XS::Dump($data)."---\n".$html;

  if ($fixed ne $html) {
    print "Fixing $fname\n";
    write_file($fname,$fixed);
    $count++;
    if ($count > 5) {
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
      fix_data($fname,$callback);
    }
  }
}

traverse($ARGV[0],".html",\&fix_media);
print "Fixed $count files\n";
