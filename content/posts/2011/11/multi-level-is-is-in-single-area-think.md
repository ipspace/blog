---
date: 2011-11-23 06:53:00+01:00
tags:
- IS-IS
title: Multi-Level IS-IS in a Single Area? Think Again!
url: /2011/11/multi-level-is-is-in-single-area-think/
lastmod: 2020-12-26 07:03:00
---
Many service providers choosing IS-IS as their IGP use it within a single area (or at least run all routers as L1L2 routers). Multi-level IS-IS design is a royal pain, more so in MPLS environments where every PE-router needs a distinct route for every BGP next hop (but of course there's a nerd knob to disable L1 default route in IS-IS). Moreover, MPLS TE is reasonably simple only within a single level (L1 or L2).

I'm positive at least some service providers do something as stupid as I usually did -- deploy IS-IS with default settings using a configuration similar to this one:
<!--more-->
{{<cc>}}Typical IS-IS configuration{{</cc>}}
``` {.code}
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
 ip router isis
!
interface Serial1/0
 description Link to P router
 ip address 10.0.7.9 255.255.255.252
 ip router isis
 mpls ip
!
interface Serial1/4
 description Backup link to RR
 ip address 10.0.7.53 255.255.255.252
 ip router isis
 mpls ip
!
router isis
 net 49.0000.0000.cccc.0001.00
 metric-style wide transition
 log-adjacency-changes
```

The above router configuration and the printouts included in this post were generated on a simple 4-router service provider network I'm using for lab configurations in the [Building IPv6 Service Provider Core](http://www.ipspace.net/IPv6SPCore) webinar (IPv6 has been removed to simplify the printouts).

{{<figure src="/2011/11/s1600-Topology.png" caption="Lab topology">}}

After the IS-IS adjacencies are established, the **show isis neighbors** command displays the expected results: all adjacencies are L1L2 adjacencies.

``` {.code}
PE-A#show isis neighbors

Tag null:
System Id      Type Interface   IP Address      State Holdtime Circuit Id
RR             L1L2 Se1/4       10.0.7.54       UP    27       00
P              L1L2 Se1/0       10.0.7.10       UP    25       00
```

The IS-IS database looks OK: every router originates an L1 LSP and an L2 LSP (there are also LSPs for Ethernet segments, for example P.02-00)

{{<cc>}}IS-IS database on PE-A{{</cc>}}
``` {.code}
PE-A#show isis database

Tag null:
IS-IS Level-1 Link State Database:
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime      ATT/P/OL
PE-A.00-00          * 0x000001C2   0x730E        1081              0/0/0
PE-B.00-00            0x000001C1   0x9A01        369               0/0/0
RR.00-00              0x000001C3   0xCE94        1087              0/0/0
P.00-00               0x000001C3   0xE49B        1046              0/0/0
P.02-00               0x000001BD   0xD0D8        1023              0/0/0
IS-IS Level-2 Link State Database:
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime      ATT/P/OL
PE-A.00-00          * 0x000001C5   0xE601        1081              0/0/0
PE-B.00-00            0x000001C1   0x9674        1083              0/0/0
RR.00-00              0x000001C5   0xA9F9        1090              0/0/0
P.00-00               0x000001C3   0xAF39        1085              0/0/0
P.02-00               0x000001C0   0xE24C        1174              0/0/0
```

A detailed look in any L2 LSP reveals the horror behind the scenes: every single IP prefix known to IS-IS is advertised in every L2 LSP (there are four loopback addresses advertised by PE-A, even though it only has one).

{{<cc>}}L2 LSP originated by PE-A{{</cc>}}
``` {.code}
PE-A#show isis database L2 PE-A.00-00 detail

Tag null:

IS-IS Level-2 LSP PE-A.00-00
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime      ATT/P/OL
PE-A.00-00          * 0x000001C5   0xE601        944               0/0/0
  Area Address: 49.0000
  NLPID:        0xCC
  Hostname: PE-A
  IP Address:   10.0.1.1
  Metric: 50         IS-Extended RR.00
  Metric: 10         IS-Extended P.00
  Metric: 10         IP 10.0.1.1/32
  Metric: 30         IP 10.0.1.2/32
  Metric: 30         IP 10.0.1.5/32
  Metric: 20         IP 10.0.1.6/32
  Metric: 20         IP 10.0.2.0/24
  Metric: 10         IP 10.0.7.8/30
  Metric: 20         IP 10.0.7.16/30
  Metric: 50         IP 10.0.7.52/30
```

The explanation of this seemingly absurd behavior is very simple: every L1L2 router leaks intra-area L1 routes into L2 topology. If the L1 and L2 topology overlap (which should not be the case), you get every single L1 prefix in every single L2 LSP. It's obviously not a good idea to cram a round peg (IP routing) into a square hole (CLNS routing protocol with totally different addressing hierarchy).

Apart from consuming way too much memory, this behavior generates a few other side effects:

-   Every time there's a topology change, every router in your network runs SPF twice; once for L1 and once for L2. It also changes its L2 LSP based on the results;
-   All the changed L2 LSPs are flooded across the network;
-   Changed L2 LSPs trigger partial L2 SPF in every router \... and if you're trigger-happy and have reduced SPF timers, you might get more than one partial SPF run due to late arrival of some changes.

Obviously it makes no sense to run IS-IS in L1L2 mode if you have only a single IS-IS area. I would prefer L2-only mode; if you run IS-IS only in level-1, you might get an inadvertent default route caused by a misconfigured L1L2 router.

To change the router type to L2-only takes a single command in Cisco IOS: **is-type level-2-only**. According to my today's understanding of Junos, it might be a bit more complex to do the same thing there (feedback welcome).

After the configuration change, the L2 LSP originated by PE-A contains just the local IP prefixes:

{{<cc>}}L2 LSP originated by PE-A running in L2-only mode{{</cc>}}
``` {.code}
PE-A#show isis data PE-A.00-00 detail

Tag null:

IS-IS Level-2 LSP PE-A.00-00
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime      ATT/P/OL
PE-A.00-00          * 0x000001C8   0xFE7C        1184              0/0/0
  Area Address: 49.0000
  NLPID:        0xCC
  Hostname: PE-A
  IP Address:   10.0.1.1
  Metric: 50         IS-Extended RR.00
  Metric: 10         IS-Extended P.00
  Metric: 10         IP 10.0.1.1/32
  Metric: 10         IP 10.0.7.8/30
  Metric: 50         IP 10.0.7.52/30
```

**Summary**: Unless you have very good reasons to do otherwise, run IS-IS in a single area and configure all routers as L2-only routers (and remember: [using recipes without understanding them can hurt your network](http://networkingnerd.net/2010/10/16/now-put-that-thing-back-where-it-came-from-or-so-help-me/)).
