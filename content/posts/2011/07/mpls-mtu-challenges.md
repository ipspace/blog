---
date: 2011-07-15 07:18:00+02:00
tags:
- MPLS
- workshop
- MPLS VPN
title: The MPLS MTU Challenges
url: /2011/07/mpls-mtu-challenges/
---
\@MCL_Nicolas sent me the [following tweet](http://twitter.com/MCL_Nicolas/status/86838923019558912):

> Finished \@packetpushers Podcast show 7 with \@ioshints \... I Want to learn more about Mpls+Mtu problem

You probably know I have to mention that a [great MPLS/VPN book](http://www.amazon.com/gp/product/1587050021/ref=as_li_tf_tl?ie=UTF8&tag=cisioshinandt-20&linkCode=as2&camp=217145&creative=399353&creativeASIN=1587050021) and [a fantastic webinar](http://www.ipspace.net/EntMPLS) describe numerous MPLS/VPN-related challenges and solutions (including MTU issues), but if MTU-related problems are the only thing standing between you and an awesome MPLS/VPN network, here are the details.
<!--more-->
The moment you configure **mpls ip** on an interface, several things happen in the background (assuming MPLS hasn't been configured on the router before and you haven't changed default settings):

-   LDP process is started and starts sending LDP hellos (UDP packets on port 646) on all MPLS-enabled interfaces;
-   Labels are assigned to all non-BGP IP prefixes in the CEF table and stored as *incoming labels* in Label Forwarding Information Base (LFIB). The outgoing action for all those labels is *untagged* (remove the top label, check the label stack is empty, and forward the IP packet).

When a router finds an LDP neighbor, it:

-   Establishes an LDP session (TCP session between loopback interfaces);
-   Exchanges all assigned labels with the LDP neighbor and stores labels sent by the neighbor in the Label Information Base (LIB);
-   Inserts *outgoing label* for every IP destination in LFIB where the LDP neighbor is the IP next hop.
-   Inserts MPLS label stack (with a single label advertised by the LDP neighbor) in the CEF table for every IP destination where the LDP neighbor is the IP next hop.

**Summary**: using the default settings in Cisco IOS, whenever two routers establish an LDP session, all IP packets forwarded between them become *labeled packets* with an MPLS label stack.

The default IP MTU on all router interfaces is 1500 bytes. The default MPLS MTU is the same, but as a single-label MPLS label stack takes 4 bytes, the MTU for labeled IP packets has to be reduced. The two routers can still exchange 1500-byte IP packets *as long as they are not labeled*. Labeled IP packets cannot be longer than 1496 bytes (remember: all forwarded packets are labeled if you use default settings).

Enabling MPLS between two routers does not affect the end hosts -- their MTU is still 1500 bytes and their packets will be fragmented by the ingress Label Switch Router (LSR) \... unless the hosts use MTU path discovery, in which case the now oversized packets will be dropped and ICMP messages will be sent back to the end hosts.

MTU path discovery usually works well in enterprise network, unless an overzealous security administrator decides to configure a firewall (or a router ACL) to drop all ICMP packets. A networking engineer misapplying best-practices documents and configuring **no ip unreachables** has the same effect. In both cases, path MTU discovery is broken and most of the application traffic crashes when you enable MPLS (VoIP might not be affected due to small packet sizes it uses).

#### More information

To learn more about MTU path discovery and related problems, read the [Never-Ending Story of IP Fragmentation](/kb/Internet/PMTUD/).

You'll find in-depth description of MPLS/VPN technology and enterprise network deployment hints in my [Enterprise MPLS/VPN Deployment](http://www.ipspace.net) webinar. For more VPN webinars, check my [VPN webinar roadmap](http://www.ipspace.net/Roadmap/VPN_webinars). You get access to all those webinars when you buy the [yearly subscription](http://www.ipspace.net/Subscription).
