---
date: 2015-03-05 08:12:00+01:00
dr_tag: fail_fix
high-availability_tag: dr
series:
- dr
tags:
- data center
- fabric
- WAN
- ACI
- high availability
title: Cisco ACI – a Stretched Fabric That Actually Works
url: /2015/03/cisco-aci-stretched-fabric-that.html
---
In mid-February a blog post on Cisco's web site [announced stretched ACI fabric](http://blogs.cisco.com/datacenter/new-cisco-apic-software-allows-stretched-aci-fabric-across-long-distances) (bonus points for not using [marketing grammar](https://blog.ipspace.net/2014/05/marketing-grammar.html) but talking about a [shipping product](http://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/release/notes/aci_nxos_rn_1103.html#46677)). Will it work better than [other PowerPoint-based fabrics](http://blog.ipspace.net/2011/09/long-distance-irf-fabric-works-best-in.html)? You bet!

### What's the Big Deal?

Cisco's ACI fabric uses distributed (per-switch) control plane with APIC controllers providing fabric configuration and management functionality. In that respect, the ACI fabric is no different from any other routed network, and we know that those work well in distributed environments.
<!--more-->
### But What about Stretched Subnets?

Even though you can use Cisco ACI to implement [stretched subnets](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html) (and there was the mandatory mention of [VM mobility](http://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html) in Cisco's documentation), the fabric uses VXLAN-over-IP as the transport protocol, making the underlying transport network rock-solid. You cannot get a L2 forwarding loop in a pure L3 network.

Stretched subnets are [as great idea as they ever were](https://blog.ipspace.net/2013/09/sooner-or-later-someone-will-pay-for.html) (there's nothing you can do to fix a broken concept), but ACI's handling of stretched subnets is better than almost anything else out there (including OTV).

ACI uses ARP proxies and anycast gateways on leaf switches, and something equivalent to VRF-based host routing to forward traffic toward IP endpoints. The traffic transported across the fabric is thus mostly unicast IP traffic (admittedly encapsulated in VXLAN envelopes), and we know that IP-based networks got pretty good at handling unicast IP traffic.

### But There's Split Brain Problem

True -- and Cisco was quick to admit the problem exists (many vendors try to pretend you don't have a problem because the [redundant links between sites can never fail](https://blog.ipspace.net/2012/10/if-something-can-fail-it-will.html)) and documented the split fabric scenario in their [design guidelines](http://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/b_kb-aci-stretched-fabric.html):

-   Controller cluster is split, and the minority part of the cluster goes into read-only mode;
-   The fabric continues to forward traffic based on already-established policy rules;
-   Leaf switches can detect new endpoints (assuming they're covered with existing policy rules) and report them to the spine switches -- both isolated fabrics thus continue to operate normally even under edge or core topology changes.

### More Information

Start with Cisco ACI videos from [NFD8](http://techfieldday.com/appearance/cisco-presents-at-networking-field-day-8/) and [NFD9](http://techfieldday.com/appearance/cisco-presents-at-networking-field-day-9/), then watch the [Multi-Pod and Multi-Site Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) part of the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar, and the [Cisco ACI Deep Dive](https://www.ipspace.net/Cisco_ACI_Deep_Dive) webinar.

**Disclosure**: Cisco Systems was indirectly covering some of the costs of my attendance at the Network Field Day 9 event. 