---
title: "Running Routing Protocols over Tunnels"
date: 2024-11-05 08:14:00+0100
tags: [ IP routing ]
---
James [got confused](https://blog.ipspace.net/2024/08/layer-3-only-evpn-behind-scenes/#2428) by a statement made by Hannes Gredler in his IS-IS book:

> Things behave really badly if the total IGP cost over the tunnel undermines the total topologies’ cost. What happens next is that the tunnel “wraps” around itself, ultimately causing a meltdown of the entire network.

Let's unpack that, starting with "Why would you need a tunnel?"
<!--more-->
The only reason to transport traffic across a tunnel[^LSP] is to prevent the intermediate nodes from inspecting the traffic and performing their own forwarding decision[^JS], typically due to one of the following scenarios:

[^LSP]: Or MPLS LSP, because I really don't want to go into the "is MPLS tunneling" discussion.

[^JS]: Ignoring the "increasing my job security," "just because I can," and "I need to practice for the CCIE lab exam on my production network" aspects.

1. We don't like the forwarding decision taken by the intermediate node (traffic engineering)
3. We have to encrypt the traffic.
2. The intermediate node knows nothing about the address space of the transported traffic (VPN)

In the first two scenarios, tunnel termination- and intermediate nodes use the same address space. Running a routing protocol *over a tunnel* could easily result in the tunnel itself being the best path for the remote tunnel endpoint, resulting in the (infinite) encapsulation recursion vividly described by Hannes (see also: [running OSPF over VXLAN](https://blog.ipspace.net/2022/10/use-vrf-for-vxlan-vlans/)).

MPLS/TE disables routing adjacencies over MPLS/TE "tunnels"[^1WAY] to avoid tunnel recursive routing. MPLS/TE tunnel is solely a data-plane construct; when a link-state routing protocol installs its routes into the RIB/FIB, it changes the outgoing interface in the FIB to a tunnel interface if the best path in the link-state shortest-path tree traverses the tunnel tail-end node[^HDNN].

[^1WAY]: MPLS/TE tunnels are one-way tunnels, so building routing adjacencies over them would be a bit hard, but I'm digressing. I vaguely remember seeing a use case for IGP routing adjacency over MPLS/TE tunnels a long while ago, but I can't remember what it was. Do leave a comment if you know more.

[^HDNN]: As one might expect, there are a half-dozen nerd knobs you can tweak to save your broken design or to make a CCIE lab more interesting.

You have to be extra careful with IPsec tunnel interfaces. You should announce the edge subnets over the tunnel (or the traffic wouldn't be pulled into the IPsec tunnel and encrypted) but not the tunnel endpoints (to avoid recursive routing). When you figure out an easy way to do that with a single OSPF or IS-IS instance, please let me know.

VPNs are a different beast. The VPN edge nodes (PE devices in MPLS/VPN or EVPN lingo) transport traffic from *customer address space*[^L2L3] using tunnels[^VT] built over the *provider address space*. They must use routing protocols[^SR] to exchange *customer prefixes* and *transport prefixes*. Traditional MPLS/VPN and EVPN achieve a clear separation between the two using BGP for customer prefixes and an IGP for transport prefixes. The GIFEE crowd wants to use EBGP everywhere, but even they usually use separate address families for the customer (L3VPN/EVPN) and transport (IPv4/IPv6) prefixes.

[^L2L3]: IPv4, IPv6, or Ethernet traffic

[^VT]: MPLS LSPs, VXLAN tunnels, GRE tunnels...

[^SR]: Or static routes, SDN controllers, or a crystal ball.

So far, so good. But what if you believe BGP is too complex to be used? If you're willing to be persuaded otherwise, I have a [few free labs to get you started](https://bgplabs.net/). Nope? That's too bad :( but it was worth a try.

However, you can use one more trick if you insist on running an IGP over a tunnel established between endpoints advertised with the same IGP: split the customer- and transport address spaces into two VRFs (one of them could be the global routing table). That will create two independent IGP instances, and as the tunnel endpoints are not in the customer VRF, you'll never get recursive routing over a tunnel.
