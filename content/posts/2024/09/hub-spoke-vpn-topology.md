---
title: "Hub-and-Spoke VPN Topology"
date: 2024-09-16 08:24:00+0200
tags: [ MPLS VPN, EVPN, design ]
series: hub_spoke_vpn
evpn_tag: vpn_topo
---
Hub-and-spoke topology is by far the most complex topology I've ever encountered in the MPLS/VPN (and now EVPN) world. It's used when you want to push all the traffic between sites attached to a VPN (spokes) through a central site (hub), for example, when using a central firewall.

{{<figure src="/2024/09/hub-spoke-firewall.png">}}

You get the following diagram when you model the traffic flow requirements with VRFs. The forward traffic uses light yellow arrows, and the return traffic uses dark orange ones.
<!--more-->
{{<figure src="/2024/09/hub-spoke-traffic-flow.png">}}

**Notes:**

* In a generic scenario, you need an *ingress* and an *egress* firewall interface for routing purposes. Please note that these are not *inside* and *outside* interfaces, as all traffic enters through the *ingress* interface and leaves through the *egress* interface.
* From the firewall perspective, you could use a one-arm design where all the traffic enters and exists the firewall through the same interface. Getting that to work on the adjacent routers (a router is hiding behind every VRF box) requires interesting tricks like Policy-Based Routing. I might cover them in another blog post.
* Trying to get stateful firewall traffic inspection to work in scenarios where all traffic (including the return traffic) enters through one interface and exists through another interface is an interesting exercise in futility.
* Each spoke site has to be connected to a different VRF. Two sites connected to the same VRF could communicate directly.

**TL&DR:** Just because you could does not mean that you should. You've been warned.

Still here? Let's move to the next bit of the puzzle: routing. The traffic in a network always flows in the opposite direction of the route propagation[^LER1], which means that the route propagation in our design should go:

* From the spoke VRFs to egress VRF
* Through the firewall into the ingress VRF[^FWDR]
* Finally, from the ingress VRF into the spoke VRFs.

The dark orange arrows in the following diagram are routing protocol updates; the light yellow ones are route leaks between VRFs[^OOM].

[^LER1]: If you wonder why that's the case, please stop reading and watch the [networking fundamentals](https://my.ipspace.net/bin/list?id=Net101) videos first.

[^FWDR]: We'll assume that the firewall is also a decent router that can be used as the CE router running OSPF or BGP.

[^OOM]: We could do route leaking on a single PE device or in an MPLS/VPN or EVPN network.

{{<figure src="/2024/09/hub-spoke-routing.png">}}

{{<note>}}We want to have any-to-any communication between the spokes, which means that routing updates *from all spokes* should follow the same path. If that doesn't make your head explode, let's move on.{{</note>}}

The final piece of the puzzle: the routing protocols. We're assuming that the route leaking between VRFs uses some unspecified mechanism (usually involving BGP) and that the leaked routes get redistributed into the PE-CE routing protocol.

* RIP would work just fine.
* OSPFv2/OSPFv3 would have no problem *as long as* the OSPF instances running in the *Hub Ingress* and the *Hub Egress* VRFs use different OSPF router IDs[^NYNC].
* BGP would work, but as the AS number of the router behind the *Hub Ingress* VRF is probably the same as the AS number of the router behind the *Hub Egress* VRF, you'd have to bypass the BGP AS-path loop prevention logic. You could, for example, use *AS override* on the firewall.

{{<figure src="/2024/09/hub-spoke-as-override.png">}}

[^NYNC]: Now you know why you can configure OSPF router ID of individual VRF instances on most network devices.

<span></span>{{<next-in-series page="/posts/2024/09/hub-spoke-single-pe.html">}}
Now that we've covered the theory, it's time to get our hands dirty. In the next blog post, we'll try to keep things as simple as possible and implement the hub-and-spoke VPN on a single PE router.
{{</next-in-series>}}
