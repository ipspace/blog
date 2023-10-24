---
title: "BGP Session Security: Be Very Skeptical"
date: 2023-10-02 07:09:00
tags: [ BGP, security ]
pre_scroll: True
---
A while ago I explained how [Generalized TTL Security Mechanism](https://blog.ipspace.net/2023/03/advantages-bgp-gtsm.html) could be used to prevent denial-of-service attacks on routers running EBGP. Considering the results published in *[Analyzing the Security of BGP Message Parsing](https://media.defcon.org/DEF%20CON%2031/DEF%20CON%2031%20presentations/Daniel%20dos%20Santos%20Simon%20Guiot%20-%20Route%20to%20bugs%20Analyzing%20the%20security%20of%20BGP%20message%20parsing.pdf)* presentation from DEFCON 31 I started wondering how well GTSM implementations work.

**TL&DR summary:**
<!--more-->
* The authors of the DEFCON 31 presentation fuzzed BGP OPEN messages.
* Most BGP routers (apart from Cisco IOS) accepted incoming TCP sessions on port 179 from IP addresses that were not configured as BGP neighbors.
* Some BGP implementations went as far as processing BGP OPEN messages before saying "*go away, I don't know you*." I would say that's equivalent to picking up a USB stick in the parking lot and checking its contents.

Considering the above results, can we trust that the vendors do the right thing and drop TCP packets with destination port 179 and too-low TTL *before* they reach the control plan or (worst case) the BGP daemon? I started wondering about that.

{{<note>}}Checking TTL after the TCP session has been established is useless from the DoS prevention perspective. The control-plane CPU cycles have already been wasted.{{</note>}}

Fortunately, it's pretty easy to check GTSM-related behavior of a particular BGP implementation:

* Start a lab with two BGP nodes
* Configure GTSM on one of them
* Reset the BGP session to make sure GTSM applies to the session setup process (or not)
* The session should be stuck in ACTIVE state. Being able to proceed beyond ACTIVE state indicates that the GTSM implementation is ~~broken~~ suboptimal.

I started the _[Protect EBGP Sessions](https://bgplab.github.io/bgplab/basic/6-protect/)_ lab exercise for a quick check of FRR behavior. The lab exercise pre-configures GTSM on Cumulus Linux[^CFR] and a standard EBGP neighbor on the user device (Arista cEOS in my case). This is what I got on Arista cEOS:

```
rtr#sh ip bgp sum
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  x1                       10.1.0.2 4 65100             15        22    0   95 00:00:36 OpenConfirm
  x2                       10.1.0.6 4 65101             10         8    0    0 00:00:34 Connect
```

The BGP session was in CONNECT state which means that:

* The TCP SYN packet was accepted by FRR even though its TTL was incorrect.
* FRR completed the TCP session establishment process
* BGP OPEN message with incorrect TTL was obviously dropped (the session was stuck in the CONNECT phase), but the TCP session was not torn down.

On the other side, FRR reported the BGP session being stuck in the OPENSENT state:

```
x1# sh ip bgp sum

IPv4 Unicast Summary:
BGP router identifier 10.0.0.10, local AS number 65100 vrf-id 0
BGP table version 2
RIB entries 3, using 600 bytes of memory
Peers 1, using 23 KiB of memory

Neighbor        V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt
10.1.0.1        4      65000         3        11        0    0    0 00:00:40     OpenSent        0

Total number of neighbors 1
```

FRR obviously:

* Completed TCP session setup even though the incoming TCP SYN packet had incorrect (too low) TTL
* Sent the BGP OPEN message but never processed the answer (thus the OpenSent state)

[^CFR]: Cumulus Linux uses FRR as its BGP routing daemon

I'm using Cumulus Linux 4.x for the external BGP speakers in the [BGP labs](https://bgplab.github.io/bgplab/), and it could be that the FRR team improved GTSM behavior in the recent versions of FRR, so I restarted the labs using FRR 9.0.1. I got the exact same behavior.

### Other Platforms

This blog post describes a proof-of-concept procedure you can use to test GTSM behavior on platforms you're interested in. I will not waste my time running those tests, but if you get interesting results please leave a comment.

### More Information

* I got the link to the DEFCON 31 presentation from the lovely SINOG 7.0 *The beautiful mess that is BGP presentation* by [Emile Aben](https://labs.ripe.net/author/emileaben/)
* Check out the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar if you want to know more about BGP security.
* For an overview of *what can go wrong with BGP* watch the *Internet Routing Security* part of *[Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC)* section of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)*.
* Want to get your hands dirty? Do the _[Protect EBGP Sessions](https://bgplab.github.io/bgplab/basic/6-protect/)_ lab exercise (part of [ipSpace.net BGP Configuration Labs](https://bgplab.github.io/bgplab/)).
