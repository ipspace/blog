---
title: "Troubleshooting Multi-Pod EVPN: Overview"
date: 2025-10-09 08:27:00+0200
tags: [ EVPN ]
evpn_tag: tshoot
---
An engineer reading my multi-pod EVPN article asked an interesting question:

> How do you handle troubleshooting when VTEPs cannot reach each other across pods?

The ancient Romans already knew the rough answer: divide and conquer.

In this particular case, the "divide" part starts with a simple realization: VXLAN/EVPN is just another application running on top of IP.
<!--more-->
Before starting a detailed troubleshooting session, it's worth doing a simple test: can you ping remote VTEPs from the IP address of the local VTEP *using the packet size required to transport the VXLAN-encapsulated Ethernet packets*?

If the answer is *no*, you have an underlay problem. If the answer is *yes*, you probably have an overlay problem.

{{<note info>}}
You might also be dealing with a firewall that passes ICMP but blocks UDP traffic. You can try to detect that with UDP-based pings. They're pretty rare on network device operating systems (unless they run on top of Linux), but readily available on Linux, for example, *netcat*.

However, it would be pretty hard to check the *actual VXLAN UDP port* when VXLAN is configured, unless your device supports VXLAN ping.
{{</note>}}

Troubleshooting a VXLAN underlay problem is pure IP connectivity troubleshooting; I'm positive your AI friend will give you plenty of ideas 😉; some might even be useful 😜.

Once you ~~hope~~ know the underlay works as expected, it's time to troubleshoot the EVPN/VXLAN part. It's time for another bifurcation:

* Is the ingress PE-device receiving the expected EVPN routes from the egress PE-device? For example, does it get the type-3 routes to set up the ingress replication? Does it get the type-2 routes for the remote MAC address?
* Are the contents of the EVPN routes correct?

If the EVPN routes are not propagated between PE-devices, you have a BGP route propagation problem. Check the BGP sessions and the address families activated on those sessions.

If you see the expected EVPN routes on the PE-devices but the next hops are incorrect, you have a problem with next-hop processing on EBGP sessions.

Finally, you might be dealing with other subtle challenges like the [FRRouting bug](/2025/06/evpn-route-attributes-matter/) I stumbled upon in June 2025. To troubleshoot those issues, it helps to have a working EVPN route (for example, one that was generated locally or at least inside the BGP AS) to compare it to the problematic route. When you spot the difference, try to figure out whether it's a missing nerd knob, a compatibility issue (in case you're brave enough to run a multi-vendor EVPN environment), or a bug.

Good luck!
