---
title: "ICMP Redirects Considered Harmful"
date: 2022-02-22 07:28:00
tags: [ IP routing, data center, design ]
---
One of my readers sent me an intriguing challenge based on the following design:

* He has a data center with two core switches (C1 and C2) and two Cisco Nexus edge switches (E1 and E2).
* He's using static default routing from core to edge switches with HSRP on the edge switches.
* E1 is the active HSRP gateway connected to the primary WAN link.

The following picture shows the simplified network diagram:
<!--more-->
{{<figure src="/2022/02/icmp-redirect-physical.png" caption="Physical connectivity">}}

All four devices are in the same VLAN, resulting in the following logical connectivity:

{{<figure src="/2022/02/icmp-redirect-layer-3.png" caption="Layer-3 connectivity">}}

He wanted to test the backup WAN link, shut down the primary link without changing the active HSRP gateway, and discovered that the core switches are no longer reachable from the outside world. Changing the HSRP gateway solved the problem. Adding another transit link between E1 and E2, and running a routing protocol on that link instead of on the current VLAN also fixed it.

I had no clue what might have gone wrong, even though the root cause was so obvious in hindsight: **ICMP redirects**.

C1 and C2 had no idea about the changed routing landscape. When they continued sending the outgoing packets toward E1, E1 sent them ICMP redirects, desperately trying to tell them to send the traffic to E2 instead. There were just a few tiny little problems:

* Linecard hardware cannot send ICMP redirects. All packets that generate a redirect (packets sent out through the same interface) must be forwarded to the main CPU.
* Control Plane Protection -- protecting the main CPU -- dropped most of those packets.
* IP routers (aka layer-3 switches) ignore ICMP redirects anyway.

Disabling ICMP redirects on the Nexus switches with **no ip redirects** magically solved the problem.

Considering the impact of this SNAFU, one has to wonder about the Nexus OS default settings:

* ICMP redirects are rarely useful
* Ignoring ICMP redirects on hosts is often considered a "security best practice" -- they are almost as good as [IPv6 Router Advertisements](https://blog.ipspace.net/2011/11/ipv6-security-getting-bored-bru-airport.html) if you want to snatch someone's traffic.
* Sending ICMP redirects is a performance killer.

And still, a modern network operating system has an obsolete 40-year-old technology enabled by default (still true on Nexus OS 9.3.8). Mindboggling.

On a tangential note, the current design suffers from traffic trombones: S1 and S2 send outgoing traffic to E1, which forwards it to E2 when the primary WAN link is down. That particular glitch would be easy to fix with anycast gateway or active-active VRRP. The proof is left as an exercise for the reader.
