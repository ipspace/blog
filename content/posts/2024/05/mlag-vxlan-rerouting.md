---
title: "MLAG Deep Dive: LAG Member Failures in VXLAN Fabrics"
date: 2024-05-15 08:51:00+0200
mlag_tag: failure
series:
- mlag
series_title: LAG Member Failures in VXLAN Fabrics
tags:
- switching
---
In the [Dealing with LAG Member Failures](/2024/05/mlag-lag-member-rerouting/) blog post, we figured out how easy it is to deal with a LAG member failure in a traditional MLAG cluster. The failover could happen in hardware, and even if it's software-driven, it does not depend on the control plane.

Let's add a bit of complexity and [replace a traditional layer-2 fabric with a VXLAN fabric](/2022/09/mlag-deep-dive-vxlan-fabric/). The MLAG cluster members still use an MLAG peer link and an anycast VTEP IP address ([more details](/2022/09/mlag-deep-dive-vxlan-fabric/)).
<!--more-->
{{<figure src="/2022/09/MLAG-VXLAN-topology.jpg" caption="MLAG cluster connected to a VXLAN fabric">}}

The good news: nothing has changed. For example, when the S1-A link fails, S1 immediately starts forwarding the traffic toward A over the peer link, and S2 forwards those packets to the S2-A link. We still need control-plane adjustments to enable flooding, but the unicast traffic flow is uninterrupted.

Now let's [add EVPN to the mix](/2022/11/mlag-vxlan-evpn/) and assume that the MLAG cluster members advertise the MAC and IP addresses of the dual-connected nodes with the anycast IP address as the next hop, and the addresses of the orphan nodes with the switch-specific VTEP IP address as the next hop ([more details](/2022/11/mlag-vxlan-evpn/)).

MLAG members can still use the failover to the peer link, keeping the unicast traffic uninterrupted. They can even keep quiet about the change if they don't use unicast VTEP IP addresses in EVPN updates.

However, an optimized EVPN implementation that uses anycast VTEP for dual-connected nodes and unicast VTEP for orphan nodes has to tell the rest of the fabric to use an optimized forwarding path (send the traffic straight to the switch connected to the orphan node).

It's no big deal. The switch connected to the orphan node (S2 in our example) can fake a MAC move event and advertise A's MAC address with an increased sequence number and unicast next hop. The switch dealing with the link failure (S1 in our example) can revoke the original advertisement for MAC-A, and the failover is seamless; not a single unicast packet needs to be lost during EVPN convergence.

Not surprisingly, the situation is not as rosy if your vendor believes in EVPN-only multihoming.

{{<next-in-series page="/posts/2024/05/mlag-evpn-rerouting.html">}}In the next blog post in this series, we'll explore what happens when your vendor drank too much EVPN Kool-Aid {{</next-in-series>}}
