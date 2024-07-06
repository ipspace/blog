---
anycast_tag: ecmp
date: 2020-10-22 07:36:00+00:00
series:
- anycast
tags:
- data center
- bridging
- IP routing
title: 'Weird: Wrong Subnet Mask Causing Unicast Flooding'
---
When I still [cared about CCIE certification](/2008/07/why-im-no-longer-active-ccie.html), I was always tripped up by the [weird scenario](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/71079-arp-cam-tableissues.html#broadcast) with (A) mismatched ARP and MAC timeouts and (B) default gateway outside of the forwarding path. When done just right you could get persistent unicast flooding, and I've met someone who reported average unicast flooding reaching ~1 Gbps in his data center fabric.

One would hope that we wouldn't experience similar problems in modern leaf-and-spine fabrics, but one of my readers managed to reproduce the problem _within a single subnet_ in FabricPath with anycast gateway on spine switches when someone misconfigured a subnet mask in one of the servers.
<!--more-->
Imagine the following FabricPath network (diagram taken from [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics) webinar):

{{<figure src="/2020/10/fabric-path-anycast.jpeg" caption="FabricPath Leaf-and-Spine Fabric">}}

Server A attached to leaf L1 has incorrect subnet mask 255.255.255.255, whereas server B attached to leaf L2 has correct subnet mask 255.255.255.0.

When A sends a packet to B, it does not send an ARP request for B, but uses default gateway (anycast gateway on spine switches) due to incorrect subnet mask. The spine switch receiving the packet (let's assume it's S1) routes it, and sends it back into the same subnet toward B. The routed packet has S1's source MAC address (SMAC), thus nobody but L1 and S1 see A's SMAC.

When B sends a packet to A, it does send an ARP request for A, and when the reply comes back (with A's SMAC) all switches know where A is... until the MAC table entry for A times out, and that's when the unicast flooding starts. L4 has no idea where A is (and it never sees any traffic from A, see above), and the only thing it can do is to flood unicast traffic toward A.

Got it? Now try to figure out:

* Would you observe the same behavior in non-EVPN VXLAN fabrics with anycast gateway configured on leaf switches?
* Would EVPN solve the problem?
* Bonus question (and I have no clue what the answer is): what would you see in an Avaya (now Extreme) SPB fabric?

It would be great to see a few answers in the comments, but do wait a day or two before posting them.

### More Information

You might find these webinars useful when trying to answer the above questions:

* [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)
* [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
* [Data Center Fabric Architectures - www.ipSpace.net](https://www.ipspace.net/Data_Center_Fabrics)

You might also want to read these blog posts to understand how anycast gateway on leaf switches works (the blog posts talk about Arista's VARP, but that's just terminology):

* [Optimal L3 Forwarding with VARP and Active/Active VRRP](/2013/05/optimal-l3-forwarding-with-varp-and.html)
* [VRRP, Anycasts, Fabrics and Optimal Forwarding](/2013/06/vrrp-anycasts-fabrics-and-optimal.html)
* [Arista EOS Virtual ARP (VARP) Behind the Scenes](/2013/06/arista-eos-virtual-arp-varp-behind.html)

