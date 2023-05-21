---
title: "Segment Routing Segment IDs and MPLS Labels"
date: 2021-05-04 07:09:00
tags: [ MPLS, segment routing ]
---
In one of my [introductory Segment Routing videos](https://my.ipspace.net/bin/get/MPLS101/SR3%20-%20MPLS%20Label%20Distribution%20in%20Segment%20Routing.mp4), I made claims along the lines of "*Segment Routing totally simplifies the MPLS control plane, replacing LDP and local labels allocated to various prefixes with globally managed labels advertised in IGP*"

It took two years for someone to realize the ~~stupidity~~ over-simplification of what I described. Matjaž Strauss sent me this kind summary of my errors:

> You're effectively claiming that SRGB has to be the same across all devices in the network. That's not true; routers advertise SIDs and must configure label swap operations in case SRGBs don't match.

Wait, what? What is SRGB and why could it be different across devices in the same network? Also, trust IETF to take a simple idea and complicate it to support vendor whims.
<!--more-->
Once you spend more than a few seconds thinking about this challenge, you're bound to figure out that:

* Segment Identifiers are statically configured (by an SDN controller, an automation script, or a CLI jockey), and must thus use a reserved label range (aka *Segment Routing Global Block* -- SRGB) where there's no chance of having an overlap with other users of dynamically-allocated MPLS labels (LDP, RSVP-TE, BGP, MPLS/VPN, EVPN...).
* Expecting multiple vendors to agree on the start and the size of that reserved range is somewhat idealistic. I'm positive the business units within a single vendor cannot agree on what to do (not to mention that some of them think SRv6 is the way to go, and others think LISP is the answer to all questions, but I'm digressing).

The only solution to this conundrum is to:

* give up, huddle up in a quiet corner with a cozy Segment Blanket, and try to figure a way out;
* change the *let's use the same labels everywhere* idea into *at least let's use the same index into reserved label range everywhere* (aka *Segment ID*);
* add *advertise reserved label range* to every mechanism you're using to propagate segment IDs;
* Add plenty of label glue on every hop of the way to map local labels into labels expected by the downstream LSR. At least the entries in the MPLS FIB aren't totally random anymore (assuming you chose a sane start of SRGB).

A picture is worth a thousand words they say. A working lab is even better, so here it is:

{{<figure src="/2021/05/SR-Simple.png" caption="Simple SR-MPLS/IS-IS Lab">}}

IS-IS and SR-MPLS are configured on two Cisco IOS XE devices (E1, C1) and two Arista EOS devices (E2, C2). IOS XE default SRGB starts at 16.000, vEOS default SRGB starts with 900.000. 

The SRGB range is advertised as a TLV in IS-IS:

```
IS-IS Level-2 Link State Database:
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime/Rcvd      ATT/P/OL
c1.00-00              0x0000002A   0xA7B1                1056/1199      0/0/0
  Area Address: 49.0001
  NLPID:        0xCC 0x8E
  Topology:     IPv4 (0x0)
                IPv6 (0x2)
  Router CAP:   10.0.0.1, D:0, S:0
    Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
      Segment Routing Algorithms: SPF, Strict-SPF
  Hostname: c1
```

Cisco IOS XE has a nice **show** command that displays SRGB for all LSPs in IS-IS topology database:

```
e1#show isis segment-routing global-block
Tag Gandalf:

IS-IS Level-2 Segment-routing Global Blocks:

System ID             SRGB Base  SRGB Range SID Index  Strict-SID SR-Cap Strict
c1                    16000      8000       1          None       Y       N
c2                    900000     65536      2          None       Y       N
e1                  * 16000      8000       3          None       Y       N
e2                    900000     65536      4          None       Y       N
```

Cisco IOS XE can also display all advertised Segment IDs and their mapping into IPv4 prefixes[^1]:

```
e1#show isis segment-routing connected-sid
Tag Gandalf:

IS-IS Level-2 connected prefix-sids:
Host                   Prefix               SID Index    Range        Flags
e1                   * 10.0.0.3/32          3            1
c1                     10.0.0.1/32          1            1
e2                     10.0.0.4/32          4            1
c2                     10.0.0.2/32          2            1
```

Arista EOS is even better: it can show IPv4 and IPv6 SID mappings (had to remove two columns from the printout, as they wouldn't fit into the default format of this blog):

```
e2#sh isis segment-routing prefix-segments ipv4

System ID: 0000.0000.0004                       Instance: 'Gandalf'
SR supported Data-plane: MPLS                   SR Router ID: 10.0.0.4

Node: 4      Proxy-Node: 0      Prefix: 0       Total Segments: 4

Flag Descriptions: R: Re-advertised, N: Node Segment, P: no-PHP
                   E: Explicit-NULL, V: Value, L: Local
Segment status codes: * - Self originated Prefix, L1 - level 1, L2 - level 2
  Prefix                      SID Type       Flags                   System ID       
  ------------------------- ----- ---------- ----------------------- ---------------
  10.0.0.1/32                   1 Node       R:0 N:1 P:1 E:1 V:0 L:0 0000.0000.0001
  10.0.0.2/32                   2 Node       R:0 N:1 P:0 E:0 V:0 L:0 0000.0000.0002
  10.0.0.3/32                   3 Node       R:0 N:1 P:1 E:1 V:0 L:0 0000.0000.0003
* 10.0.0.4/32                   4 Node       R:0 N:1 P:0 E:0 V:0 L:0 0000.0000.0004
e2#sh isis segment-routing prefix-segments ipv6

System ID: 0000.0000.0004                       Instance: 'Gandalf'
SR supported Data-plane: MPLS                   SR Router ID: 10.0.0.4

Node: 1      Proxy-Node: 0      Prefix: 0       Total Segments: 1

Flag Descriptions: R: Re-advertised, N: Node Segment, P: no-PHP
                   E: Explicit-NULL, V: Value, L: Local
Segment status codes: * - Self originated Prefix, L1 - level 1, L2 - level 2
  Prefix                      SID Type       Flags                   System ID
  ------------------------- ----- ---------- ----------------------- ---------------
* 2001:db8:cafe:4::1/128      104 Node       R:0 N:1 P:0 E:0 V:0 L:0 0000.0000.0004
```

OK, so everyone agrees that one should use SID 4 to get to 10.0.0.4, but IOS XE thinks the way to get there is to use label 16004, while EOS thinks 900004 is the right label to use. What could E1 do, having an IOS XE and an EOS downstream neighbor? It must run an algorithm along these lines for every IP prefix with a SID:

* Find all downstream neighbors for the prefix (remember, we're doing ECMP between C1 and C2);
* For every neighbor, look into IS-IS topology database to find neighbor's SRGB;
* Map local MPLS label (local SRGB + SID) into downstream MPLS label (remote SRGB + SID).

Here are the expected results from E1 MPLS FIB. Problem solved.

```
e1#show mpls forwarding-table 10.0.0.4 detail
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label      Label      or Tunnel Id     Switched      interface
16004      16004      10.0.0.4/32      0             Gi2        10.0.0.1
	MAC/Encaps=14/18, MRU=1500, Label Stack{16004}
	525400E150A052540031C74D8847 03E84000
	No output feature configured
    Per-destination load-sharing, slots: 0 2 4 6 8 10 12 14
           900004     10.0.0.4/32      0             Gi3        10.0.0.2
	MAC/Encaps=14/18, MRU=1500, Label Stack{900004}
	084FA9A8356452540043122F8847 DBBA4000
	No output feature configured
    Per-destination load-sharing, slots: 1 3 5 7 9 11 13 15
```

You can also see the downstream labels in IPv4 routing table:

```
e1#show ip route 10.0.0.4
Routing entry for 10.0.0.4/32
  Known via "isis", distance 115, metric 30, type level-2
  Redistributing via isis Gandalf
  Last update from 10.0.0.2 on GigabitEthernet3, 08:29:58 ago
 SR Incoming Label: 16004
  Routing Descriptor Blocks:
    10.0.0.2, from 10.0.0.4, 08:29:58 ago, via GigabitEthernet3
      Route metric is 30, traffic share count is 1
      MPLS label: 900004
      MPLS Flags: NSF
  * 10.0.0.1, from 10.0.0.4, 08:29:58 ago, via GigabitEthernet2
      Route metric is 30, traffic share count is 1
      MPLS label: 16004
      MPLS Flags: NSF
```

... and in the CEF table:

```
e1#show ip cef 10.0.0.4 detail
10.0.0.4/32, epoch 2, per-destination sharing
  sr local label info: global/16004 [0x1B]
  nexthop 10.0.0.1 GigabitEthernet2 label 16004-(local:16004)
  nexthop 10.0.0.2 GigabitEthernet3 label 900004-(local:16004)
```

### Reproducibility Is Essential

Want to try it out? You'll find the [lab setup](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-sid) and [device configurations](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-sid/config) on Github. I used *libvirt* Vagrant provider, if you happen to have VirtualBox boxes, or containerlab-compatible containers, [install netlab](https://netlab.tools/install/), change the provider in the topology file to **virtualbox** and rerun the [lab topology creation script](https://netlab.tools/netlab/create/).

[^1]: You can assign a segment ID to an IPv6 prefix in Arista EOS, but not in Cisco IOS XE. Last time I looked at my calendar, it said 2021, and Cisco supposedly supported IPv6 everywhere [for at least a decade](https://blog.ipspace.net/2010/11/ipv6-in-data-center-after-year-cisco-is.html). Yeah, sure...

### Revision History

2021-07-12
: Updated the *netsim-tools* documentation links.

