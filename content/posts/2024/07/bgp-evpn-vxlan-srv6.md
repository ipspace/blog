---
title: "BGP, EVPN, VXLAN, or SRv6?"
date: 2024-07-25 07:55:00+0200
tags: [ BGP, EVPN, VXLAN, segment routing ]
evpn_tag: intro
series_weight: 460
---
Daniel Dib [asked an interesting question](https://www.linkedin.com/feed/update/urn:li:activity:7221449552220823552?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7221449552220823552%2C7221746944149180416%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287221746944149180416%2Curn%3Ali%3Aactivity%3A7221449552220823552%29) on LinkedIn when considering an RT5-only EVPN design:

> I’m curious what EVPN provides if all you need is L3. For example, you could run pure L3 BGP fabric if you don’t need VRFs or a limited amount of them. If many VRFs are needed, there is MPLS/VPN, SR-MPLS, and SRv6.

I received a similar question numerous times in my previous life as a consultant. It's usually caused by vendor marketing polluting PowerPoint slide decks with acronyms without explaining the fundamentals[^HF]. Let's fix that.
<!--more-->
[^HF]: To be fair, it's not their job to explain the fundamentals to enable a customer to make an informed decision. Their job is to sell their boxes; a confused customer is always an excellent mark.

IP networks use hop-by-hop destination-only forwarding using a single forwarding table. If that's what you need, step away from the acronyms; all you have to decide is what routing protocol to use. We [had that discussion a gazillion times in the past](https://blog.ipspace.net/series/dcbgp/), and the only sane recommendation is, "_It usually doesn't matter[^SR]; use whatever is familiar._"

[^SR]: If your network is extensive enough so that it matters, and you can't decide what to use, stop reading blog posts and hire someone with a cluebat.

### Traffic Diversions

Next, you might want to divert some traffic (still within a single routing domain) onto a path that might be considered suboptimal. You might want to do some traffic engineering or push traffic around a failure before everyone involved realizes the network topology has changed ([more details](/series/fast-failover/)).

In that case, you must hide the traffic from the intermediate nodes into a tunnel or a virtual circuit -- you need a data-plane packet-hiding technology. MPLS (data-plane encapsulation) is the most commonly used one; vendors trying to sell new ASICs are preaching the beauties of SRv6, and I don't think I've seen VXLAN used in this scenario (primarily because it does not allow you to do loose source routing).

You obviously need a control plane to support the traffic-hiding shenanigans[^SDNC]. A decade ago, we used RSVP to build MPLS-TE tunnels. Today, I'd recommend using an SR-aware IGP, and I'm sure someone could make it work with BGP-LU.

To recap, this is what I would do in 2024:

* Select an IGP that works with Segment Routing (the MPLS variant)
* Enable MPLS and SR-MPLS in your network
* Provision traffic engineering paths on head-end routers or through a controller
* Configure TI-LFA to support fast rerouting around failures.

[^SDNC]: You could also prove RFC 1925 Rule 6 and offload the problem to an SDN controller.

### Multiple Forwarding Domains

Now for the fun part: you want multiple independent forwarding domains running on top of a shared infrastructure. The marketing term for that is Virtual Private Networks (VPN), and they could use MAC addresses (L2VPN) or IP addresses (L3VPN) to make forwarding decisions.

You could involve all network devices in making those forwarding decisions:

* The ingress device would mark a packet with a VPN identifier
* The intermediate devices would look at the VPN identifier and select the desired forwarding table
* The egress device would remove the VPN identifier from the packet and forward the packet to the final destination.

Did you notice I described VLANs and VLAN-based VRF-lite? Sometimes, they are all you need to get the job done.

OK, now let's assume you've seen as many VLAN-based fabric meltdowns as I did[^WTO] and want something better. Yet again, we need two components:

[^WTO]: Or was told about as part of my consulting work ;

* A data plane component that will hide the VPN traffic from the intermediate nodes. The usual candidates are MPLS, VXLAN, GRE,  SRv6, or even PBB (802.1ah) or LISP (data plane encapsulation).
* A control plane component that will distribute the VPN endpoint information from egress to ingress nodes. You could choose between L3VPN (RFC 4364, aka MPLS/VPN), EVPN, LISP, or even SPB (802.1aq) if you want a standard solution.

You can't willy-nilly combine data-plane encapsulations with control plane protocols:

* L3VPN usually works with MPLS encapsulation. Some vendors automatically add GRE tunnels as needed.
* SPB (802.1aq) works with PBB (802.1ah) encapsulation. Yet again, there are proprietary implementations involving GRE tunnels.
* SRv6 is just a data-plane encapsulation and needs a control plane. [RFC 9252](https://www.rfc-editor.org/rfc/rfc9252.html) defines two control planes you can use[^MPS]: EVPN is the usual answer, but you could [also use L3VPN](https://www.rfc-editor.org/rfc/rfc9252.html#name-bgp-based-l3-service-over-s) (RFC 4364)[^OGNT].
* EVPN is the clear winner. EVPN implementations use MPLS, VXLAN, PBB, or SRv6 data-plane encapsulations.

I'm positive there are a half-dozen RFCs out there describing other combinations. Please leave pointers in the comments.

[^MPS]: Unless you believe in the magic powers of SDN controllers.

[^OGNT]: Who would have thought such an ancient technology could be used to control the shiny new stuff?

### Layer-3-Only VPNs

It took us a long time, but we finally reached the question we started with: What can you use to implement layer-3-only VPNs?

**L3VPN (RFC 4364)** is the obvious answer but usually requires MPLS encapsulation (unless your vendor implemented layer-3 VPNs with SRv6 using RFC 4364 control plane). That's not a big deal; most modern ASICs support MPLS in one way or another, and SR-MPLS makes MPLS fabrics as simple as possible. The real problem is that L3VPN is not cool enough for the vendor marketing departments (hey, everyone has been doing that for 25 years). They might want to use it to power their SRv6 implementations, but then they might keep mum about it and pretend that SRv6 magic gets the job done.

**EVPN** is another (more popular) answer, but there's just a tiny gotcha: it was designed to be a layer-2 VPN solution. Making it into a layer-3 VPN is possible but requires significant deviations from vendor defaults (= tweaking nerd knobs) (see [Jeff Doyle and Jeff Tantsura discussing it](https://www.youtube.com/clip/Ugkx6DMOvh6Hv6nJSyH-fjUEGKtEs2_I4D5T) for more details).

The beauty of EVPN is that you can use it with whatever your vendor is pushing you into: it always worked with MPLS, it works beautifully with VXLAN, and most vendors preaching the benefits of SRv6 can use it as the VPN control plane on top of it.
