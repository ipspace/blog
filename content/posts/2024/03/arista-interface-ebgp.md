---
title: "Interface EBGP Sessions on Arista EOS"
date: 2024-03-19 07:48:00+0100
tags: [ BGP ]
---
Arista EOS and Cisco Nexus OS got *interface EBGP sessions* years after [Cumulus Linux](https://blog.ipspace.net/2015/02/bgp-configuration-made-simple-with.html). While they're trivially easy to configure on FRRouting (the routing daemon used by Cumulus Linux), getting them to work on Arista EOS is a bit tricky.

To make matters worse, my Google-Fu failed me when I tried to find a decent step-by-step configuration guide; all I got was a 12-minute video full of YouTube ads. Let's fix that.
<!--more-->
### Terminology Matters

A bit of terminology first (you know that I'm a bit obsessed with that). The functionality described in this blog post is sometimes called *unnumbered BGP sessions*, which makes no sense. BGP is running over TCP, and there's nothing unnumbered about TCP.

"Running BGP over unnumbered IPv4 interfaces" is a bit better but still misleading, as BGP runs over IPv6 LLA addresses. What we're doing is:

* Running BGP TCP session between IPv6 LLA addresses;
* Enabling IPv4 address family on that session;
* Use IPv6 next hops for IPv4 prefixes ([more details](https://blog.ipspace.net/2022/11/bgp-unnumbered-duct-tape.html))

That's a mouthful, isn't it? However, as most implementations allow you to configure an *interface* EBGP neighbor (the router figures out remote IPv6 LLA from ICMP messages), let's call this thingy *interface EBGP sessions*.

### Back to Arista EOS

To get interface EBGP sessions working on the Arista cEOS release 4.31.2F, you have to:

* Enable IPv6 on relevant interfaces (no surprise there)

```
interface Ethernet1
   ipv6 enable
!
interface Ethernet2
   ipv6 enable
```

* Enable IPv6 routing. Even though you're not routing IPv6 and have no IPv6 non-LLA addresses on the device, you still have to do it, or the box refuses to look for potential IPv6 LLA EBGP neighbors.[^RA]

```
ipv6 unicast-routing
```

[^RA]: It could be that enabling IPv6 routing starts IPv6 router advertisements.

* You can find several related examples using the **‌ip routing ipv6 interfaces** global configuration. I have no idea what it does. The latest Arista EOS documentation fares no better, but I got feedback along the lines of "*Use that when you don't have an IPv4 address on the interface.*" Throw it in for good measure if things fail to work 🤷‍♂️
* Create a BGP peer group. You cannot configure an interface peer without specifying a peer group.

```
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   neighbor ebgp peer group
```

* Specify interface neighbors, their parent peer group, and their BGP AS:

```
router bgp 65000
   neighbor interface Et1 peer-group ebgp remote-as 65100
   neighbor interface Et2 peer-group ebgp remote-as 65101
```

* Activate the *interface neighbor* peer group for the IPv4 address family. If you're not routing IPv6, you don't have to activate the IPv6 address family on these neighbors.

```
router bgp 65000
   address-family ipv4
      neighbor ebgp activate
```

* Specify that you want to use IPv6 LLA as the next hop for the IPv4 prefixes. Without this command, Arista EOS does not negotiate [RFC 8950](https://datatracker.ietf.org/doc/html/rfc8950) next hops for IPv4. The IPv4 BGP prefixes sent over the IPv6 LLA BGP session either get (useless) IPv4 next hops or aren't advertised at all.

```
router bgp 65000
   address-family ipv4
      neighbor ebgp next-hop address-family ipv6 originate
```

If you did everything right, you'd see IPv4 prefixes with IPv6 next hops in the BGP table:

```
rtr#show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      192.168.100.0/24       fe80::a8c1:abff:feb4:ab82%Et1 0       -          100     0       65100 i
 * >      192.168.101.0/24       fe80::a8c1:abff:fe18:8133%Et2 0       -          100     0       65101 i
```

You can practice the above recipe in the [EBGP Sessions over IPv6 LLA Interfaces](https://bgplabs.net/basic/d-interface/) BGP lab.

### Revision History

2024-03-21
: Added a hint that you might need **‌ip routing ipv6 interfaces** configuration command for *addressless forwarding* over IPv6 LLA interfaces.
