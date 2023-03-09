---
date: 2012-04-24 08:19:00+02:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- bridging
- high availability
title: STP loops strike again
url: /2012/04/stp-loops-strike-again.html
---
[Vasilis](http://www.linkedin.com/pub/vasilis-bouloukos/2/a66/b69) sent me an interesting campfire story. It started with a common mistake:

> An external partner of my company used an Ethernet cable and connected two switchport interfaces of one of our access switches .

Being a conscientious networking engineer, he had the usual safeguards in place \...
<!--more-->
> I have to mention that these access ports are configured with Root, BDPU guard as well as Portfast.

\... but he nonetheless experienced a total LAN meltdown:

> This had a severe effect (unavailability) to our LAN. L2 loops caused our L2 switches, Core Switches and Routers to reach 100% CPU!

Root cause analysis turned out a surprising fact:

> I thought that BPDU and Root guard were enough to protect the access ports of our LAN but found out it was not true.

Fortunately, the [Cisco documentation explaining the problem](http://www.cisco.com/en/US/tech/tk389/tk621/technologies_tech_note09186a0080136673.shtml) is quite explicit:

> It should be noted that short-living loops are not prevented by Root or BPDU Guards, if two portfast-enabled ports are connected directly or through the hub

**The problem?** Looped ports won't shut down until a BPDU packet is sent through one of them, and a single broadcast (for example, ARP packet) sent in that interval can cause a network meltdown.

**The solution?** Vasilis found a solution similar to those proposed in comments to my [*Preventing Bridging Loops Without STP*](https://blog.ipspace.net/2012/01/prevent-bridging-loops-without-bpdus.html) post: use **switchport port-security** and limit the number of MAC addresses accepted on the switch port.

Unfortunately, this solution works primarily in campus environments; you cannot use it in virtualized data centers with moving VMs as you can never predict how many VMs (and MAC addresses) will reside within a physical server.

**Better ideas?** Please share them in the comments!

**Short summary**: Bridging (also known as layer-2 switching) sucks (and some implementations suck more than others). We need to move to L3-based solutions.
