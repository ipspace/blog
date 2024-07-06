---
date: 2021-06-02 08:59:00+00:00
series:
- unnumbered-interfaces
tags:
- IP routing
- networking fundamentals
title: Unnumbered Ethernet Interfaces
---
Imagine an Internet Service Provider offering Ethernet-based Internet access (aka everyone using fiber access, excluding people believing in [Russian dolls](/2008/10/internet-access-russian-dolls.html)). If they know how to spell security, they might be nervous about connecting numerous customers to the same multi-access network, but it seems they have only two ways to solve this challenge:

* Use private VLANs with proxy ARP on the head-end router, forcing the customer-to-customer traffic to pass through layer-3 forwarding on the head-end router.
* Use a separate routed interface with each customer, wasting three-quarters of their available IPv4 address space.

Is there a third option? Can't we pretend Ethernet works in [almost the same way as dialup](/2021/05/fundamentals-unnumbered-ip-interfaces.html) and use unnumbered IPv4 interfaces? 
<!--more-->
Considering what we [already know about unnumbered interfaces](/2021/05/routing-unnumbered-interfaces.html), it shouldn't be too hard to get it done, considering that Ethernet forces you to supply next-hop layer-2 information even on point-to-point links.

Here's what we have to do:

* We'd need a static host route on our access router for each client, pointing toward an unnumbered interface. The static routes could be preconfigured or created on the fly based on DHCP address allocation.
* We'd need ARP entries for client IP addresses connected to unnumbered interfaces to get the destination MAC address for the outbound IP packets.

It turns out that we had all the necessary bits and pieces for decades but couldn't use them because network operating systems didn't allow us to configure unnumbered multi-access interfaces.  

{{<note info>}}Recent versions of Cisco IOS XE, Cisco Nexus OS, Arista EOS, and Junos no longer have that restriction. If anyone feels like tracking down the exact software version that added unnumbered Ethernet functionality, please write a comment.{{</note>}}

### Using Static Routes

We'll start with the simplest scenario: using static routes. We'll use a simple lab with an access router and two clients, each one of them connected to the access router with an Ethernet point-to-point link:

{{<figure src="/2021/06/Addr-Ethernet-Unnumbered-Static.png" caption="Lab topology">}}

First, we need to configure a few unnumbered interfaces on the access router.

{{<cc>}}Unnumbered Ethernet interfaces on access router{{</cc>}}
```
interface Loopback0
 ip address 10.2.1.1 255.255.255.255
!
interface GigabitEthernet2
 description rtr -> c1
 ip unnumbered Loopback0
!
interface GigabitEthernet3
 description rtr -> c2
 ip unnumbered Loopback0
```

Next, we configure static routes for the client IP addresses pointing to those interfaces:

{{<cc>}}Static routes pointing toward the clients{{</cc>}}
```
ip route 10.2.1.2 255.255.255.255 GigabitEthernet2
ip route 10.2.1.3 255.255.255.255 GigabitEthernet3
```

That's it. Now you can log in to one of the clients and ping the other client.

{{<note warn>}}I'm ignoring a dirty detail -- you have to configure IP addresses on clients' uplinks. See [device configurations](https://github.com/ipspace/netlab-examples/tree/master/routing/lan-unnumbered/static-routes) for details.{{</note>}}

### How Does It Work?

Here's the magic trick: whenever you configure a static route pointing to an interface (without a next-hop), the router assumes that any destination within the configured prefix is directly connected (even though all printouts claim it's still a static route).

{{<cc>}}Routing table on the access router{{</cc>}}
```
rtr#show ip route 10.2.0.0 longer-prefixes | begin Gateway
Gateway of last resort is 192.168.121.1 to network 0.0.0.0

      10.0.0.0/32 is subnetted, 3 subnets
C        10.2.1.1 is directly connected, Loopback0
S        10.2.1.2 is directly connected, GigabitEthernet2
S        10.2.1.3 is directly connected, GigabitEthernet3
rtr#show ip route 10.2.1.2
Routing entry for 10.2.1.2/32
  Known via "static", distance 1, metric 0 (connected)
  Routing Descriptor Blocks:
  * directly connected, via GigabitEthernet2
      Route metric is 0, traffic share count is 1
```

How do you reach a directly connected IP host? You ARP for its IP address and use the MAC address you get back to send the packet to it... and it doesn't matter if the destination IP address belongs to the same subnet or not. ARP will kick in as soon as a router forwards an IP packet using a route without a next-hop.

Here's the (expected) ARP cache on our access router. The loopback IP address has an ARP entry on all unnumbered interfaces; the ARP entries for adjacent IP addresses (10.2.1.2 and 10.2.1.34) point to different interfaces.

{{<cc>}}ARP cache on the access router{{</cc>}}
```
rtr#show arp 10.2.0.0 255.255.0.0
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.2.1.1                -   5254.0049.6b64  ARPA   GigabitEthernet2
Internet  10.2.1.1                -   5254.003a.5bba  ARPA   GigabitEthernet3
Internet  10.2.1.2                1   5254.00e3.3048  ARPA   GigabitEthernet2
Internet  10.2.1.3                1   5254.00cb.bf02  ARPA   GigabitEthernet3
```

Mission accomplished? Not exactly. While it's possible to automate static route configuration, we still need to tell the clients what IP addresses to use. Time to add DHCP to the picture -- the topic of the next blog post in [this series](/series/unnumbered-interfaces.html).

### Want to Know More?

* The configurations I used to generate the printouts are on [GitHub](https://github.com/ipspace/netlab-examples/tree/master/routing/lan-unnumbered).
* I discussed numerous aspects of network addressing in *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.
