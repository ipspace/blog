#!/usr/bin/perl
use File::Basename;
use File::Slurp;
use URI::Encode qw(uri_encode uri_decode);
use Data::Dumper;
use YAML::XS;
use Getopt::Long;

our $count = 0;

sub urlize($) {
  my ($label) = @_;
  $label = uri_decode($label);
  $label =~ s/ /-/g;
  $label =~ s/['"]//g;
  return lc $label;
}

sub fix_tags($) {
  my ($data) = @_;

  return unless $data->{tags};
  my $taglist = $data->{tags};
  my $taglen  = scalar @$taglist;
  my $cnt = 0;

  my $old_tags = join "|",sort @$taglist;

  my $t_remove = $tags->{remove};
  my $t_list   = $tags->{tags};

  for (my $i = 0; $i < $taglen; $i++) {
    for (my $j = 0; $j < scalar @$t_remove; $j++) {
      if (lc @$taglist[$i] eq lc @$t_remove[$j]) {
        @$taglist[$i] = undef;
        $cnt++
      }
    }
    for (my $j = 0; $j < scalar @$t_list; $j++) {
      my $value = @$taglist[$i];
      my $match = @$t_list[$j];
      if (index(lc $value,lc $match) == 0 && length($value) <= length($match) + 1) {
        @$taglist[$i] = @$t_list[$j];
        $cnt++;
      }
    }
  }
  $data->{tags} = [ grep { $_} @$taglist ];
  my $new_tags = join "|",sort @{$data->{tags}};

  return $old_tags ne $new_tags;
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
#    print $yaml."\n\n".$fixed; exit;
    write_file($fname,$fixed);
    $count++;
    if ($count > 2000) {
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

our ($opt_tags,$opt_dir,$tags);

GetOptions('tags=s' => \$opt_tags,'posts=s' => \$opt_posts);

$tags = YAML::XS::LoadFile($opt_tags);
traverse($opt_posts,".html",\&fix_tags);
print "Fixed $count files\n";
