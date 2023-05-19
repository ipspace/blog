#!/usr/bin/env perl
#

use strict;

my $text = "";
my $outfile = $ARGV[0];

# Slurp HTML text
while (<>) {
	$text .= $_;
}

#print($text);
my $title = "";
my $html = "";
print("$outfile\n");
if ($text =~ m#<TITLE>(.*)</TITLE>#) {
  $title = $1;
}
if ($text =~ m#<TABLE.*WIDTH=.*<TD>(.*)</TD>#sm) {
  $html = $1;
} elsif ($text =~ m#<!--msnavigation--><td.*?>(.*?)<!--msnavigation-->#sm) {
  $html = $1;
}

if ($html) {
  $html =~ s#<span.*?>(.*?)</span>#$1#msg;
}

if ($title && $html) {
  open(FH, '>', $outfile) or die $!;
  print FH "---\ntitle: $title\nhidden: True\nminimal_sidebar: True\n---$html\n";
  close FH;
  print("Created $outfile\n");
} else {
  print("Cannot extract title or HTML\n")
}
