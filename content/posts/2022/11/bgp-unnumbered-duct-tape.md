---
title: "BGP Unnumbered Duct Tape"
date: 2022-11-15 07:18:00
tags: [ BGP ]
pre_scroll: True
dcbgp_tag: cl
series:
- dcbgp
- unnumbered-interfaces
short_summary: |
  We could always [run BGP across unnumbered links](/2021/05/routing-unnumbered-interfaces/#bgp) if we used an IGP or static routes to propagate the loopback addresses of adjacent nodes. Recently, many vendors started supporting another solution: run EBGP over IPv6 LLA and exchange IPv4 prefixes over that EBGP session using the next-hop encoding specified in [RFC 5549](https://www.rfc-editor.org/rfc/rfc5549.html). How exactly does that work?
---
Every time I mention unnumbered BGP sessions in a webinar, someone inevitably asks "_and how exactly does that work?_" I always replied "_gee, that's a blog post I should write one of these days,_" and although some readers might find it long overdue, here it is ;)

We'll work with a simple two-router lab with two parallel unnumbered links between them. Both devices will be running Cumulus VX 4.4.0 (FRR 8.4.0 container generates almost identical printouts).
<!--more-->
{{<figure src="/2022/11/bgp-unnumbered.png" caption="EBGP sessions in unnumbered BGP lab">}}

Just in case you want to replicate the results, here's the [netlab topology I used](https://github.com/ipspace/netlab-examples/tree/master/BGP/Unnumbered):

{{<cc>}}Unnumbered BGP test lab topology{{</cc>}}
```
---
module: [ bgp ]
defaults.device: cumulus
provider: clab

nodes:
  r1:
    bgp.as: 65001
  r2:
    bgp.as: 65002

links:
- r1:
  r2:
  unnumbered: True
- r1:
  r2:
  unnumbered: True
```

netlab configures loopback IPv4 address on unnumbered Linux interfaces. While that doesn't change the results, I removed it to prove that Linux happily sends and receives IPv4 packets over an interface that does not have an IPv4 address[^IPSEC]:

[^IPSEC]: Keep that in mind the next time you'll think that removing an IPv4 address from a Linux interface makes it impossible to break in through that interface.

{{<cc>}}Interface addressing on R1{{</cc>}}
```
r1(bash)#ip addr show dev swp1
1985: swp1@if1984: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether aa:c1:ab:14:a7:c9 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::a8c1:abff:fe14:a7c9/64 scope link
       valid_lft forever preferred_lft forever
r1(bash)#ip addr show dev swp2
1987: swp2@if1986: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether aa:c1:ab:ea:a0:ad brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::a8c1:abff:feea:a0ad/64 scope link
       valid_lft forever preferred_lft forever
```

We know that unnumbered BGP sessions use IPv6 link-local addresses, and that FRR advertises IPv4 prefixes with IPv6 next hops using encoding specified in [RFC 5549](https://www.rfc-editor.org/rfc/rfc5549.html) (now [RFC 8950](https://www.rfc-editor.org/rfc/rfc8950)).

A quick look at the BGP neighbors on R1 confirms that:

* The IP address of the BGP neighbor is a link-local IPv6 address;
* The BGP session has been established between IPv6 link-local addresses;
* The routers have negotiated _extended next hop_ capabilities for IPv4 address family
* The local next hop used on outgoing updates will be the local link-local IPv6 address

{{<cc>}}First BGP neighbor on R1{{</cc>}}
```
r1# sh ip bgp nei
BGP neighbor on swp1: fe80::a8c1:abff:fe14:ea9e, remote AS 65002, local AS 65001, external link
 Description: r2
Hostname: r2
  BGP version 4, remote router ID 10.0.0.2, local router ID 10.0.0.1
  BGP state = Established, up for 00:13:10
  Last read 00:00:01, Last write 00:00:01
  Hold time is 9, keepalive interval is 3 seconds
  Neighbor capabilities:
    4 Byte AS: advertised and received
    AddPath:
      IPv4 Unicast: RX advertised IPv4 Unicast and received
    Extended nexthop: advertised and received
      Address families by peer:
                   IPv4 Unicast
...
Local host: fe80::a8c1:abff:fe14:a7c9, Local port: 60794
Foreign host: fe80::a8c1:abff:fe14:ea9e, Foreign port: 179
Nexthop: 10.0.0.1
Nexthop global: fe80::a8c1:abff:fe14:a7c9
Nexthop local: fe80::a8c1:abff:fe14:a7c9
```

BGP table (displayed by FRR) confirms FRR uses IPv6 next hops for IPv4 prefixes:

{{<cc>}}BGP table entry for R2 loopback on R1{{</cc>}}
```
r1# show ip bgp 10.0.0.2
BGP routing table entry for 10.0.0.2/32
Paths: (2 available, best #2, table default)
  Advertised to non peer-group peers:
  r2(swp1) r2(swp2)
  65002
    fe80::a8c1:abff:feaf:4333 from r2(swp2) (10.0.0.2)
    (fe80::a8c1:abff:feaf:4333) (used)
      Origin IGP, metric 0, valid, external, multipath
      Last update: Fri Nov 11 14:17:52 2022
  65002
    fe80::a8c1:abff:fe14:ea9e from r2(swp1) (10.0.0.2)
    (fe80::a8c1:abff:fe14:ea9e) (used)
      Origin IGP, metric 0, valid, external, multipath, bestpath-from-AS 65002, best (Neighbor IP)
      Last update: Fri Nov 11 14:17:52 2022
```

Interestingly, the IPv4 routing table in Linux kernel still uses the IPv6 next hops[^6NH]:

[^6NH]: One of many Linux Kernel contributions made by Cumulus engineers

{{<cc>}}IPv4 routing table on R1{{</cc>}}
```
r1(bash)#ip route
10.0.0.2 nhid 23 proto bgp metric 20
	nexthop via inet6 fe80::a8c1:abff:fe14:ea9e dev swp1 weight 1
	nexthop via inet6 fe80::a8c1:abff:feaf:4333 dev swp2 weight 1
```

However, keep in mind that the role of next hops in any forwarding table is to point to ARP/ND entries that contain the next-hop MAC address[^NHG] -- the thing the router has to insert into the destination MAC address of the forwarded packets.

[^NHG]: I'm ignoring [nexthop groups](https://lwn.net/Articles/763950/) in this blog post.

Here are the ND entries for the BGP next hops:

{{<cc>}}IPv4 routing table on R1{{</cc>}}
```
r1(bash)#ip neigh
169.254.0.1 dev swp1 lladdr aa:c1:ab:14:ea:9e PERMANENT proto zebra
169.254.0.1 dev swp2 lladdr aa:c1:ab:af:43:33 PERMANENT proto zebra
fe80::a8c1:abff:feaf:4333 dev swp2 lladdr aa:c1:ab:af:43:33 router REACHABLE
fe80::a8c1:abff:fe14:ea9e dev swp1 lladdr aa:c1:ab:14:ea:9e router REACHABLE
```

By now it should be evident how Linux kernel makes the packet forwarding decisions:

* IPv4 packet can be received on any interfaces, even if that interface doesn't have an IPv4 address
* Forwarding table lookup results in a next hop that could belong to a different address family
* A lookup into the neighbor table produces the MAC address of the next hop
* The next hop MAC address is used as the destination MAC address when building the outgoing MAC header.

The above explanation works well for software-based forwarding, but what happens on a Cumulus Linux switch where the packet forwarding is done in hardware, and the hardware forwarding tables are derived from Linux kernel tables? According to [_TA_](#1513), the forwarding hardware is surprisingly flexible:

{{<long-quote>}}
On Mellanox ASICs, routes will index into a host table using (next-hop IP, egress router interface) as the key, and the address-family of the next-hop does not need to match the address-family of the route. The host entry determines the DMAC that will be used after the Ethernet header is re-written post-routing.

On Broadcom ASICs, routes don't directly point to a next-hop or host table; instead they index into an "egress" table by ID. So Broadcom natively has a decoupling of a route and the L2 rewrite information returned by the LPM lookup, this allowing the control plane to choose what rules it wishes to enforce with regards to address-families of routes vs next-hops. Another fun tidbit, the ARP/NDP tables are actually collapsed into the LPM lookup as if they were host routes, and these entries also index into the same egress table.
{{</long-quote>}}

Finally, what's the deal with the fake static ARP entries for 169.254.0.1? They were needed in the old days when Linux kernel didn't support IPv6 next hops for IPv4 routes, and they're left there in case someone disables nexthop-groups, or as [Donald Sharp](https://www.linkedin.com/in/donaldsharp/) explained:

{{<long-quote>}}
The 169.254.0.1 neighbor table entries are an artifact from pre-nexthop group implementations in FRR. Prior to nexthop groups the linux kernel would not accept a v6 nexthop for a v4 prefix. So the routes were entered with a 169.254.0.1/outgoing-intf as the actual nexthop.

The code to add this entry just has not gotten removed yet, since they have not done any current harm. Additionally they are there for when the operator enters the command to turn off nexthop groups for installation into the linux kernel.
{{</long-quote>}}

### Revision History

2022-11-16
: Updated the _hardware forwarding_ and _static ARP entries_ parts of the blog post based on comment by _TA_ and Donald Sharp.