---
title: "Reliable ECMP with Static Routing"
date: 2023-09-08 07:00:00
tags: [ IP routing ]
---
One of my readers wanted to use [EIBGP](/2013/06/eibgp-load-balancing.html) to load balance outgoing traffic from a pair of WAN edge routers (hint: wrong tool for this particular job[^WTFTJ]). He's using a design very similar to [this one](/2022/02/nexus-icmp-redirects.html) with VRRP running between WAN edge routers, and the adjacent firewall cluster using a default route to the VRRP IP address.

The problem: all output traffic goes to the VRRP IP address which is active on one of the switches, and only a single uplink is used for the outgoing traffic.
<!--more-->
{{<note info>}}Fun fact: you might get better load balancing if you accept many prefixes from the upstream providers and do some smart route selection, maybe combined with NetFlow analysis. Careful readers might find the relevant details somewhere on this blog.{{</note>}}

This is how my reader wanted to use EIBGP load balancing:

> I considered changing settings in the firewall to do ECMP to the physical interfaces (IP) of the switches. We checked it and it seems easy but need to be tested. Or maybe I could use EIBGP, but I'm not sure about this solution and where to put it and how plus I read some comments about possible forwarding loops.

Unless you're using BFD with static routes (or some similar vendor-specific functionality like [reliable static routes](/2007/02/reliable-static-routing.html)), it's not a good idea to use  static routes pointing to physical IP addresses from the resiliency perspective. An interface might go down, and the static route would keep sending traffic into a black hole.

However, that's easy to solve with an ancient trick: use two VRRP (or HSRP or GLBP) groups, each one “owned” by one of the switches, and have two static routes pointing to the two VRRP addresses.

Ideally one would run a routing protocol between the WAN edge routers and the firewall cluster, and advertise the default route from both switches (that's why the routing protocols were invented). 

Finally, if you're faced with a security professional who considers OSPF insecure, go for EBGP.

[^WTFTJ]: The primary EIBGP use case is in MPLS/VPN WAN networks, and it usually requires MPLS transport and works in VRFs. Also, EIGBP is no longer the cool kid on the block (if it ever was). Cisco engineers would probably tell you to use segment routing (bonus points if you're persuaded to use SRv6) and Egress Peer Engineering.

### Revision History

2023-10-09
: Added link to a video explaining EIBGP load balancing
