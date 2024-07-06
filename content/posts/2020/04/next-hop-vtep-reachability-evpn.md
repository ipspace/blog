---
date: 2020-04-14 07:02:00+00:00
dcbgp_tag: abstract
evpn_tag: details
series:
- bgp_nh
- dcbgp
series_title: Next-Hop and VTEP Reachability in EVPN Networks
tags:
- EVPN
- BGP
title: 'Response: Next-Hop and VTEP Reachability in EVPN Networks'
---
[Jeff Tantsura](https://www.linkedin.com/in/jeff-tantsura-bb229b2/) published a great response to my _[Can We Trust BGP Next Hops](/2020/04/can-we-trust-bgp-next-hops-part-1.html)_ blog post on LinkedIn, and I asked him for permission to save it in a more permanent form. Here it is (slightly edited)...
- - -
I'd like to bring back EVPN context. The discussion is more nuanced, the common non-arguable logic here - reachability != functionality.
<!--more-->
The fact that an end-point is reachable doesn't mean it is functional, and other way around, well, if it is functional but unreachable - it doesn't really matter. There are 2 ways to validate the functionality: locally to the device or through a path-trace that emulates encapsulation and semantics of the real traffic that is destined to the end-point (VTEP is the end-point for VxLAN encapsulated traffic).

### Local validation

For obvious reasons it doesn't make sense to withdraw the underlay route (VTEP) _[ even if the VTEP is not functional &mdash; IP ]_.

EVPN provides means to signal per EVI membership, namely throughout IMET (type 3) route. If local-to-the-device validation could detect dysfunctional/malfunctioning VTEP, withdrawing type 3 route could signal such condition. If the hosts behind the malfunctioning VTEP are single-homed, it doesn't matter that much since traffic is not going to reach them anyway.

When the hosts are multi-homed and EVPN ESI is in use, this is much more interesting case, since now the goal is to stop load-sharing/exclude a device with malfunctioning VTEP from being load-shared to.

As we know - ESI functionality is provided by type 1(per ES; per EVI) and type 4 (DF election) routes. Withdrawing type 1 per ES route (function called for a reason - mass withdraw) would achieve exactly that.

### Remote validation

We could also use path trace that is VxLAN aware. In NX-OS realm NG-OAM (draft-tissa-nvo3-oam-fm) could [validate VTEP functionality](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/92x/vxlan-92x/configuration/guide/b-cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-92x/b_Cisco_Nexus_9000_Series_NX-OS_VXLAN_Configuration_Guide_9x_chapter_0110.html) on the device and potentially notify sending device of the failure.
- - -
### Ivan's summary

As far as I'm aware no vendor implemented either option to check VTEP functionality in real time and adjust the forwarding behavior (NG-OAM **ping** and **traceroute** can be run as diagnostic commands).

{{<note info>}}I hope I'm wrong, in which case you probably know how to [reach me](https://www.ipspace.net/Contact#Tech).{{</note>}}

Also, running EVPN sessions between loopback (VTEP) addresses and expecting that presence of BGP sessions validates correct data-plane VTEP functionality is no more than wishful thinking.

In the end we're back to "_networks work reasonably well, stay calm, stop worrying (too much) and get a life._"

{{<next-in-series page="/posts/2020/04/can-we-trust-bgp-next-hops-part-2.html" />}}
