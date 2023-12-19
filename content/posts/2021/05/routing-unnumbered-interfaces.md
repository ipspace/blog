---
date: 2021-05-26 07:06:00+00:00
dcbgp_tag: relevant
ospf_tag: unnumbered
series:
- unnumbered-interfaces
- dcbgp
tags:
- IP routing
- bridging
- networking fundamentals
- OSPF
- BGP
title: Packet Forwarding and Routing over Unnumbered Interfaces
---
In the previous blog posts in [this series](/series/unnumbered-interfaces.html), we explored whether we [need addresses on point-to-point links](/2021/05/fundamentals-need-interface-addresses.html) (TL&DR: no), whether it's better to have [interface or node addresses](/2021/05/fundamentals-interface-node-addresses.html) (TL&DR: it depends), and why we got [unnumbered IPv4 interfaces](/2021/05/fundamentals-unnumbered-ip-interfaces.html). Now let's see how IP routing works over unnumbered interfaces.

### The Challenge

A cursory look at an IP routing table (or at CCNA-level materials) tells you that the IP routing table contains prefixes and next hops, and that the next hops are IP addresses. How should that work over unnumbered interfaces, and what should we use for the next-hop IP address in that case?
<!--more-->
As always, oversimplifications (like the one in the previous paragraph) can impede your understanding. The job of a [forwarding table](https://blog.ipspace.net/2010/09/ribs-and-fibs.html) (FIB)[^1] in a router is to:

* Find the outgoing interface that is on the shortest path to the destination;
* Rewrite layer-2 header in the forwarded packet in a way that will make the downstream router receive it.

{{<figure src="/2021/05/Addr-Forwarding-101.png" caption="IP forwarding in a nutshell">}}

Have you noticed that I haven't mentioned the next-hop IP address at all? We commonly use next-hop IP addresses in routing tables as a convenient abstraction to:

* **Identify the outgoing interface** -- match the next-hop IP address to an interface subnet, and assume that must be the outgoing interface.
* **Get the destination layer-2 address** we need in the outgoing layer-2 header -- use ARP/ND table to map the next-hop IP address into MAC address[^2]

However, if we manage to get the same information in some other way, there's no need for next-hop IP addresses. For example, the outgoing layer-2 header on a point-to-point link is always the same (because it's a point-to-point link).

Let's walk through a few examples.

### Static Route Pointing to a Point-to-Point Interface

Imagine you configure a static route pointing to a GRE tunnel (because very few people know what serial interfaces are in 2021). Do you need a next-hop IP address for that route? Of course not. The outgoing interface is clearly identified (you configured it), and there's only one potential next-hop: the other end of the tunnel. Problem solved -- point-to-point tunnels can be unnumbered interfaces.

Here's a curveball: what happens if a static route without next-hop information points to an Ethernet interface? You REALLY SHOULD lab this, but I doubt you will, so you'll find the answer in the comments to [this blog post](https://blog.ipspace.net/2009/10/my-stupid-moments-interface-default.html).

### Getting Our Hands Dirty

Consider a simple 2-router network with a GRE tunnel between the routers. 

{{<figure src="/2021/05/Addr-GRE-Lab.png" caption="Simple 2-router lab">}}

We'll use static routes instead of a routing protocol and will add the following static route for remote loopback interface pointing to the tunnel:

{{<cc>}}Static route pointing to a GRE tunnel{{</cc>}}
```
ip route 10.0.0.2 255.255.255.255 Tunnel0
```

The route appears in the routing table *without any next-hop information*, the only unusual bit of the printout is the claim that it's a *directly connected* route.

{{<cc>}}Static route without next-hop information in the IP routing table{{</cc>}}
```
r1#sh ip route 10.0.0.2
Routing entry for 10.0.0.2/32
  Known via "static", distance 1, metric 0 (connected)
  Routing Descriptor Blocks:
  * directly connected, via Tunnel0
      Route metric is 0, traffic share count is 1
```
 
Not surprisingly, R1 can ping R2's loopback interface, but not its LAN interface (we'd need another static route for that)

```
r1#ping 10.0.0.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/2 ms
```

### Unnumbered Interfaces and Routing Protocols

Now let's assume you're running OSPF across unnumbered interfaces. It's perfectly legal, and there's even provision in the OSPF RFC for [what subnet mask one should be using on such occasions](https://blog.ipspace.net/2021/04/build-unnumbered-lab-netsim-tools.html) (hint: all zeroes).[^4]

Using some magic (aka SPF algorithm), OSPF figures out it needs to use an unnumbered interface to send traffic to some destination. No problem, it installs a route pointing to that interface, and takes the neighbor IP address (as taken from OSPF hello messages) as the next hop[^6].

[^6]: This behavior might be implementation-specific. After all, there's nothing in the OSPF topology database that would help the router figure out what to use as the next hop.

{{<cc>}}OSPF route uses source IP address of neighbor's OSPF HELLO packets as the next hop{{</cc>}}
```
r1#sh ip route 172.16.1.0
Routing entry for 172.16.1.0/24
  Known via "ospf 1", distance 110, metric 1001, type intra area
  Last update from 10.0.0.2 on Tunnel0, 00:00:34 ago
  Routing Descriptor Blocks:
  * 10.0.0.2, from 10.0.0.2, 00:00:34 ago, via Tunnel0
      Route metric is 1001, traffic share count is 1
```

Just in case you're wondering how to get to the next hop (because it sure doesn't belong to any of the connected subnets) -- there's a route in the routing table saying "_to get to the next hop, go to the next hop_."

{{<cc>}}OSPF route for the remote router ID{{</cc>}}
```
r1#sh ip route 10.0.0.2
Routing entry for 10.0.0.2/32
  Known via "ospf 1", distance 110, metric 1001, type intra area
  Last update from 10.0.0.2 on Tunnel0, 00:00:56 ago
  Routing Descriptor Blocks:
  * 10.0.0.2, from 10.0.0.2, 00:00:56 ago, via Tunnel0
      Route metric is 1001, traffic share count is 1
```

Fortunately, we don't really need the next hop on a point-to-point link. Everything works as expected as long as we can figure out what to put in the outgoing layer-2 header.[^3]

[^3]: Unnumbered Ethernet interfaces are a bit of a challenge. We'll get there in another blog post.

### Making BGP Work

You cannot run BGP over unnumbered interfaces... or at least it's hard establishing a TCP session with an IP address that's not in your routing table, but I know we all love [MacGyver-type challenges](https://blog.ipspace.net/2013/08/temper-your-macgyver-streak.html), so here's how you solve this conundrum:

* Figure out what the remote system wants to use as the source IP address of the BGP session (let's assume it's their loopback IP address)
* Create a static host route for that IP address pointing to the unnumbered interface.
* Establish a multihop EBGP session with that remote IP address.

Is anyone using such a nasty hack in real life? Sure -- that's how you establish a BGP session with Azure over a VPN connection.

{{<figure src="/2021/05/Addr-BGP-Unnumbered-Azure.png" caption="EBGP routing with Azure Virtual Network Gateway over an unnumbered IPsec tunnel">}}

### Want to See BGP Work? Here It Is...

I started with the initial configuration of our two-router network (static routes for remote loopback interfaces pointing to GRE tunnel) and configured BGP:

{{<cc>}}BGP configuration on R1{{</cc>}}
```
router bgp 65000
 bgp log-neighbor-changes
 network 172.16.0.0 mask 255.255.255.0
 neighbor 10.0.0.2 remote-as 65001
 neighbor 10.0.0.2 ebgp-multihop 255
 neighbor 10.0.0.2 update-source Loopback0
```

Here's the BGP table I was able to observe after a few seconds:

{{<cc>}}BGP table on R1{{</cc>}}
```
BGP table version is 5, local router ID is 10.0.0.1
...
     Network          Next Hop            Metric LocPrf Weight Path
 *>   172.16.0.0/24    0.0.0.0                  0         32768 i
 *>   172.16.1.0/24    10.0.0.2                 0             0 65001 i
```
 
 And here's the entry for remote LAN in the local IP routing table:
 
{{<cc>}}IP routing table entry for 172.16.1.0/24 on R1{{</cc>}}
```
Routing entry for 172.16.1.0/24
  Known via "bgp 65000", distance 20, metric 0
  Tag 65001, type external
  Last update from 10.0.0.2 00:03:21 ago
  Routing Descriptor Blocks:
  * 10.0.0.2, from 10.0.0.2, 00:03:21 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
      MPLS label: none
```

As you can see, BGP needs next hops to be happy, and the next hop is recursively resolved using the static route we configured.

### What About IPv6?

You might think that we don't have the same challenges in IPv6. After all, IPv6 always assigns a link-local address (LLA) to an interface, and we can use the LLA of the downstream router as the next hop, right?

That trick helps you build the outgoing layer-2 header -- there's a well-defined way to take the downstream IPv6 LLA, do a Neighbor Discovery (ND) cache lookup, and get layer-2 information -- but it doesn't help you identify the outgoing interface. After all, link-local addresses use the same prefix on all interfaces. You still need routes pointing to interfaces, not just IPv6 next-hops.

### Want to Know More?

* The configurations I used to generate the printouts are on [GitHub](https://github.com/ipspace/netlab-examples/tree/master/routing/gre-unnumbered).
* I discussed numerous aspects of network addressing in *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.

[^1]: The table used for data-plane packet forwarding should be called the forwarding table, not the routing table (although some systems might use the same data structure for both).

[^2]: Or whatever the underlying address of the outgoing interface is -- it could be another IP address when doing tunneling.

[^4]: Trying to implement this concept, you'll also encounter an interesting  Socket API challenge: at some point in time, you'll have to send unicast OSPF packets to an IP address that's not (yet) in your routing table. The details are left as an exercise for the reader.
