---
title: "OSPF and ARP on Unnumbered IPv4 Interfaces"
date: 2023-08-31 06:20:00
tags: [ ARP, OSPF ]
series: unnumbered-interfaces
---
After figuring out [ARP details](/2023/08/arp-details.html), describing how [routers use ARP to resolve entries in the IP routing table](/2023/08/arp-static-routes.html), and considering what we already know about [OSPF on unnumbered IPv4 interfaces](/2022/01/ospf-unnumbered.html), we're finally ready to answer Daniel's question:

{{<figure src="/2023/08/ARP-Q.png">}}
<!--more-->
We'll use a simple OSPF lab consisting of three Arista cEOS routers with unnumbered point-to-point links. Here's the _[netlab](https://netlab.tools/)_ topology file describing the lab:

```
defaults.device: eos
addressing.p2p.ipv4: True
module: [ ospf ]

nodes: [ r1, r2, r3 ]
links: [ r1-r2, r1-r3, r2-r3, r1, r2, r3 ]
```

{{<figure src="/2023/08/ospf-unnumbered.png" caption="Lab topology">}}

### Exchanging OSPF Packets

OSPF does not need ARP. OSPF does not work over unnumbered IPv4 interfaces unless you configure them as a point-to-point OSPF link.

On a point-to-point link, OSPF sends all packets to the *all routers* IP multicast address (224.0.0.5). You don't need ARP to do that -- Section 6.4 of [RFC 1112](https://www.rfc-editor.org/rfc/rfc1112.html) describes a simple algorithm that translates an IP multicast address into a MAC address.

### Routing Table

When OSPF inserts best routes into the IP routing table, it sets the outgoing interface and the next-hop IP address for each route[^DMD]:

[^DMD]: The rest of this section describes Arista EOS behavior. Most OSPF implementations do something similar, but the details may vary. Run your own tests.

* The route toward the IP address used by the adjacent router on the point-to-point link is inserted as a directly connected (no next hop) OSPF route.
* All other routes going through the OSPF neighbor use the IP address of the neighbor as the next hop.

```
r1#show ip route ospf interface ethernet 2
...
 O        10.0.0.3/32 is directly connected, Ethernet2
 O        172.16.2.0/24 [110/20] via 10.0.0.3, Ethernet2
```

However, this trick only works if the neighboring router advertises the IP address it uses on the point-to-point link in its OSPF LSA (remember: the route inserted in the IP routing table has to be an OSPF route).

If we disable OSPF on the loopback address of R2, R1 can no longer insert that host route into the IP routing table, and the other routes advertised by R2 become unanchored (they use a next hop that does not exist)

```
r1#show ip route ospf interface ethernet 1

WARNING: Some of the routes are not programmed in
kernel, and they are marked with '%'.
...
 O%       172.16.1.0/24 [110/20] via 10.0.0.2, Ethernet1
```

**Lessons learned:**

* Use the loopback IP address as the source IP address of the unnumbered interfaces[^ADC]
* Make sure the loopback interface[^OWE] is advertised by OSPF.

[^ADC]: It seems that Arista EOS uses the loopback IP address as the source address in the OSPF packets regardless of what you configure with the **ip unnumbered** command.

[^OWE]: Or whatever other IP address you're using as the source IP address of the unnumbered interfaces

### What About ARP?

[ARP details](/2023/08/arp-details.html) and [ARP and Static Routes](/2023/08/arp-static-routes.html) blog posts contains all you need to know, here's the TL&DR:

* When trying to resolve the MAC address of the directly-connected remote IP address (usually: remote loopback interface), the router sends an ARP request for the remote IP address from the source IP address used on the interface (usually: local loopback interface).
* The remote router has no problem replying to the ARP request. The requested IP address is used on the interface (usually ARP works even if you turn off proxy ARP), and the source IP address is not checked.
* The router receiving the ARP reply knows that the source IP address (of the ARP reply) is reachable through the incoming interface, accepts ARP reply, and completes the forwarding entry in the IP forwarding table.
* All other OSPF routes use the remote IP address as the next hop and need no further ARP resolution.
