---
date: 2008-09-29 06:45:00.001000+02:00
tags:
- MPLS
- command line interface
title: Enhance the Traceroute Output
url: /2008/09/enhance-traceroute-output/
---
After working with MPLS Traffic Engineering lab for a few days and interpreting IP addresses from various **traceroute** outputs, I finally had enough and wrote a simple Perl script (below) that parses router configurations and produces **ip host** configuration commands for every interface IP address it encounters. When you paste the **ip host** commands into the configuration of the edge router from which you do the tests, the meaningless numbers finally make sense.
<!--more-->
Compare the "traditional" output produced with MPLS-enabled **traceroute**...

{{<cc>}}Traceroute displaying MPLS labels and IP addresses{{</cc>}}
``` {.code}
PE-A#traceroute PE-C

Type escape sequence to abort.
Tracing the route to PE-C (10.0.1.5)

  1 10.0.7.6 [MPLS: Label 1017 Exp 0] 16 msec 136 msec 52 msec
  2 10.0.7.26 [MPLS: Label 3018 Exp 0] 8 msec 20 msec 8 msec
  3 10.0.7.30 [MPLS: Label 4018 Exp 0] 16 msec 20 msec 56 msec
  4 10.0.7.33 [MPLS: Label 2017 Exp 0] 20 msec 44 msec 20 msec
  5 10.0.7.17 24 msec *  24 msec
```

... with this one:

{{<cc>}}Traceroute displaying MPLS labels and hostnames + interfaces{{</cc>}}
``` {.code}
PE-A#traceroute PE-C

Type escape sequence to abort.
Tracing the route to PE-C (10.0.1.5)

  1 Serial1-0.C1 (10.0.7.6) [MPLS: Label 1017 Exp 0] 56 msec
  2 Serial1-2.C3 (10.0.7.26) [MPLS: Label 3018 Exp 0] 12 msec
  3 Serial1-1.C4 (10.0.7.30) [MPLS: Label 4018 Exp 0] 48 msec
  4 Serial1-2.C2 (10.0.7.33) [MPLS: Label 2017 Exp 0] 52 msec
  5 Serial1-0.PE-C (10.0.7.17) 16 msec *  64 msec
```

### Perl script

```
#!/usr/bin/perl

use strict;
use Getopt::Long;

our ($host,$domain,$FQDN,$loop,$ifname,$inIfMode);
our ($opt_dbg);

GetOptions("debug" => \$opt_dbg);

while (<>) {
  if (/^hostname\s+(.*)/) { 
    $host = $1; 
    print STDERR "processing router $host\n" if $opt_dbg; 
    $FQDN = $host; $loop = 0; 
  }
  if (/^ip\s+domain-name\s+(.*)/) { 
    $domain = $1; 
    print STDERR "router $host in domain $domain" if $opt_dbg; 
    $FQDN = "$host.$domain"; }
  if (/^interface\s+(.*)/) { 
    $ifname = $1; $ifname =~ s/[:\/.]/-/gi; $ifname = "$ifname.";
    print "interface $ifname\n" if $opt_dbg; 
    if ($ifname =~ /loopback/i) { $ifname = "" unless $loop++; }
    $inIfMode = 1 ;
  } elsif (/^[a-z]/i) { $inIfMode = 0; }
    elsif (/^\s+ip address ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)/i && $inIfMode) { 
      print "ip host $ifname$FQDN $1\n"; 
  }
}