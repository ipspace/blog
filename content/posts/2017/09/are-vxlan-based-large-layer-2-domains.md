---
date: 2017-09-21 08:56:00+02:00
dr_tag: fail_fix
high-availability_tag: dr
series:
- dr
tags:
- bridging
- VXLAN
- switching
- data center
- high availability
title: Are VXLAN-Based Large Layer-2 Domains Safer?
url: /2017/09/are-vxlan-based-large-layer-2-domains.html
---
One of my readers was wondering about the stability and scalability of large layer-2 domains implemented with VXLAN. He wrote:

> If common BUM traffic (e.g. ARP) is being handled/localized by the network (e.g. NSX or ACI), and if we are managing what traffic hosts can send with micro-segmentation style filtering blocking broadcast/multicast, are large layer-2 domains still a recipe for disaster?

There are three major (fundamental) problems with large L2 domains:
<!--more-->
-   [non-deterministic forwarding](http://blog.ipspace.net/2010/07/bridging-and-routing-is-there.html) (flood-when-unknown)
-   no data plane loop detection mechanism
-   summarization boundary spanning multiple sites.

First two are caused by the Ethernet forwarding semantics and could be solved with enough effort and clever tricks, but then you\'d effectively replace bridging with routing based on MAC addresses (effectively [reinventing CLNS](http://blog.ipspace.net/2015/10/was-clnp-really-broken.html) and using MAC addresses as globally-unique network-layer addresses). That would also break the IEEE 802.1/801.3 forwarding semantics, so why bother.

{{<note info>}}This is exactly what the original TRILL proposal tried to do before it got bogged down with "*we have to support flooding and VLANs and...*" garbage.{{</note>}}

It\'s better to stop pretending that we [live in the age of long coax cable](http://blog.ipspace.net/2015/04/what-is-layer-2-and-why-do-we-need-it.html) and start doing proper longest-prefix IPv4/IPv6 routing with L2 domain being limited to where it belongs: adjacent L3 nodes.

The third fundamental problem is a killer. We\'re designing our networks based on long tradition of subnet-based forwarding: one VLAN = one subnet = one IP summarization entity. If a summarization entity becomes partitioned (fancy language for *falls apart*), all bets are off, you're dealing with interesting forwarding blackholes, and quite often you lose all sites involved in the debacle not just one of them.

The claims that you can solve the problem with redundant connectivity just prove that some people don't understand statistics, and that [RFC 1925](https://tools.ietf.org/html/rfc1925) Rule 4 is still relevant. As anyone who has enough operational experience knows, it\'s not the matter of IF but [WHEN the brown substance hits the rotating blades](http://blog.ipspace.net/2012/10/if-something-can-fail-it-will.html).

Having stretched layer-2 domains is very similar to deploying OSPF inter-area summarization with ABRs being far apart - yet again, I\'m guessing there are people out there with hands-on experience of how wonderful that idea is.

One could solve the summarization problem by inserting host routes into the wider network, and it might eventually work (see also: Mobile ARP, EVPN, LISP...) but definitely not across stateful network services (see also: [stretched firewall clusters](http://blog.ipspace.net/2015/11/stretched-firewalls-across-layer-3-dci.html)) and toward the Internet. Oh, and by now you probably realized we're about to [reinvent CLNS using IP addresses](http://blog.ipspace.net/2015/05/reinventing-clns-with-l3-only-forwarding.html) instead of MAC addresses.

Alternatively, one could realize that it doesn\'t make sense to try to find the solution to world peace in the networking layer (while keeping in mind that that\'s exactly what the engineers working for networking vendors are paid to do and promote) and spend his time [working with business owners](http://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) to figure out how to [get out of the mess](http://blog.ipspace.net/2013/09/layer-2-extension-otv-use-cases.html) we allowed the networking and virtualization vendors to entice us into.
