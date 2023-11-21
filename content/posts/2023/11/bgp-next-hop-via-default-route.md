---
title: "Can a Router Use the Default Route to Reach BGP Next Hops?"
date: 2023-11-23 07:22:00
tags: [ BGP ]
pre_scroll: True
---
**TL&DR**: Yes.

Starting with RFC 4271, [Route Resolvability Condition](https://datatracker.ietf.org/doc/html/rfc4271#section-9.1.2.1):

* A route without an outgoing interface is resolvable if its next hop is resolvable without recursively using the same route.
* A route with an outgoing interface is always considered resolvable.
* BGP routes can be resolved through routes with just a next hop or an outgoing interface.
<!--more-->
It looks like the authors of RFC 4271 found the above conditions as confusing as I did -- they provided this summary in the following paragraph:

> Note that a BGP route is considered unresolvable in a situation where the BGP speaker's Routing Table contains no route matching the BGP route's NEXT_HOP.  Mutually recursive routes (routes resolving each other or themselves) also fail the resolvability check.

Did you notice that the *default* route is not mentioned anywhere? Being optimistic and assuming the default route is a route like any other, I would conclude that the default route can be used to resolve the BGP next hops. A corollary: All BGP routes are valid if a router has a default route.

That's the theory. What about reality? I set up a [simple lab topology](https://github.com/ipspace/netlab-examples/tree/master/BGP/Default-NH)[^J2] containing these devices:

* An external BGP speaker (XT)
* An AS boundary router (EDGE) with an EBGP and an IBGP session.
* An internal router (INT) with an IBGP session with the AS boundary router.
* The AS boundary router does not change the BGP next hop on the IBGP session (making it unreachable) but advertises the OSPF default route.

[^J2]: Together with a few Jinja2 templates needed to configure the EDGE router to advertise the default route into OSPF.

Here are the IP addresses of the lab devices:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **edge** |  10.0.0.2/32 |  | Loopback |
| eth1 | 172.16.0.2/24 |  | edge -> xt |
| eth2 | 172.16.1.2/24 |  | edge -> int |
| **int** |  10.0.0.3/32 |  | Loopback |
| GigabitEthernet0/1 | 172.16.1.3/24 |  | int -> edge |
| **xt** |  10.0.0.1/32 |  | Loopback |
| eth1 | 172.16.0.1/24 |  | xt -> edge |
{.fmtTable}

## Test Results

Cisco IOSv considers the BGP route with the next hop 172.16.0.1 (IP address of the XT router) valid even though it claims the next hop is not in the BGP table:

```
int#show ip bgp 10.0.0.1
BGP routing table entry for 10.0.0.1/32, version 2
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  65100
    172.16.0.1 (metric 1) from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      rx pathid: 0, tx pathid: 0x0
int#show ip route 172.16.0.1
% Subnet not in table
```

Arista EOS also uses the default route to resolve the BGP next hops but correctly displays the routing entry it used:

```
int#show ip bgp 10.0.0.1
BGP routing table information for VRF default
Router identifier 10.0.0.3, local AS number 65200
BGP routing table entry for 10.0.0.1/32
 Paths: 1 available
  65100
    172.16.0.1 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, IGP metric 1, weight 0, tag 0
      Received 00:00:09 ago, valid, internal, best
      Rx SAFI: Unicast
int#show ip route 172.16.0.1 | begin Gateway
Gateway of last resort:
 O E2     0.0.0.0/0 [110/1] via 172.16.1.2, Ethernet1
```

Cumulus Linux (and FRR) does not use the default route to resolve BGP next hops:

```
int# show ip bgp 10.0.0.1
BGP routing table entry for 10.0.0.1/32
Paths: (1 available, no best path)
  Not advertised to any peer
  65100
    172.16.0.1 (inaccessible) from edge(10.0.0.2) (10.0.0.2)
      Origin IGP, metric 0, localpref 100, invalid, internal
      Last update: Tue Nov 21 12:37:34 2023
int# show ip route 172.16.0.1
Routing entry for 0.0.0.0/0
  Known via "ospf", distance 110, metric 1, best
  Last update 00:00:21 ago
  * 172.16.1.2, via swp1, weight 1
```

You must configure `ip nht resolve-via-default` on FRR to allow it to use the default route to resolve the BGP next hops.

```
int# conf t
int(config)# ip nht resolve-via-default
int(config)# ^Z
int# show ip bgp 10.0.0.1
BGP routing table entry for 10.0.0.1/32
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  65100
    172.16.0.1 (metric 1) from edge(10.0.0.2) (10.0.0.2)
      Origin IGP, metric 0, localpref 100, valid, internal, bestpath-from-AS 65100, best (First path received)
      Last update: Tue Nov 21 12:37:34 2023
```

What about your favorite device? Rerun the test and let me know!