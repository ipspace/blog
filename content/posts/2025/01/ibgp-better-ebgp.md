---
title: "IBGP Is the Better EBGP"
date: 2025-01-21 08:33:00+0100
tags: [ BGP, design ]
---
Whenever I was explaining how one could build EBGP-only data center fabrics, someone would inevitably ask, "But could you do that with IBGP?"

**TL&DR:** Of course, but that does not mean you should.

Anyway, leaving behind the land of sane designs, let's trot down the rabbit trail of IBGP-only networks.
<!--more-->
### It Looks Easy from a Distance

This is how we were building Boring Networks that Worked&trade; before the stampede toward the lands of GIFEE enlightenment started:

{{<figure src="/2025/01/design-igp-network.png" caption="An IP network built with a protocol designed for that purpose">}}

We added IBGP to the mix when we had to exchange a large number of routes or transport customer routes that had to remain invisible to the network core using VPNv4, VPNv6 or EVPN address families:

{{<figure src="/2025/01/design-ibgp.png" caption="Adding IBGP to an IP network">}}

Due to how the ancients designed IBGP to be used, the intermediate nodes must be *route reflectors*. We would also establish IBGP sessions between *loopback interfaces* to ensure IBGP does not have to deal with core link failures.

Following the *[BGP Is the Better IGP](https://www.youtube.com/watch?v=yJbqnOdD3cg)* rallying cry, people started building networks in which every node would be a different autonomous system:

{{<figure src="/2025/01/design-ebgp-only.png" caption="EBGP-only network with no IBGP or IGP">}}

Now, let's bring that journey to the obvious conclusion and use IBGP as a better EBGP. What could possibly go wrong?

{{<figure src="/2025/01/design-ibgp-only.png" caption="IBGP-only network with no IGP">}}

### The Details

The above diagram already hints at a number of details:

* As there is no IGP to propagate loopback prefixes, the IBGP sessions must be established between directly connected interfaces.
* All intermediate nodes (spine switches or P-routers) must be IBGP route reflectors.
* You'll need a chain of route reflectors in larger networks.

All that would be easy to do. Unfortunately, there's an additional detail:

* [BGP next hops are not supposed to change within an autonomous system](https://blog.ipspace.net/2011/08/bgp-next-hop-processing/). IBGP should be used just to exchange reachability information, and IGP should be used to resolve the next hops.
* Within an IBGP-only network, [contrary to what I wrote a while ago](/2022/10/bgp-route-reflector-next-hops/), the route reflectors have to change the BGP next hops to mimic the behavior of EBGP sessions.
* That is a direct violation of the SHOULD NOT directive of the [RFC 4456 Section 10](https://datatracker.ietf.org/doc/html/rfc4456#section-10), and some implementations might not allow you to tweak that rule.[^SN]

[^SN]: But we all know that SHOULD NOT really means "but we know you will," and a lot of implementations play along.

**To recap:** You can build IBGP-only networks if you can configure IBGP sessions between directly connected IP addresses *and* change the BGP next hops on route reflectors.

### Does It Work?

Of course, it does. We had a network like that running[^LP] in the 1990s[^RRNH], and it only got simpler in the meantime.

[^LP]: At least in the lab. I have no idea whether that ever moved to production.

[^RRNH]: We probably had to force the value of the next hops on the reflected routes with an inbound route map -- a nasty kludge if I ever saw one.

To prove it, I set up a [simple _netlab_ topology](https://github.com/ipspace/netlab-examples/blob/master/BGP/interface-IBGP/topology.yml) with a [plugin](https://github.com/ipspace/netlab-examples/blob/master/BGP/interface-IBGP/ibgp.interface/plugin.py) that removes all IBGP sessions from a network and replaces them with IBGP sessions between directly connected nodes. This is the relevant part of the spine switch configuration running Arista EOS ([full device configurations are on GitHub](https://github.com/ipspace/netlab-examples/tree/master/BGP/interface-IBGP/config)):

{{<cc>}}BGP configuration of a spine switch in an IBGP-only network{{</cc>}}
```
router bgp 65000
   router-id 10.0.0.3
   no bgp default ipv4-unicast
   bgp cluster-id 10.0.0.3
   bgp advertise-inactive
   neighbor 10.1.0.1 remote-as 65000
   neighbor 10.1.0.1 next-hop-peer
   neighbor 10.1.0.1 description leaf-1
   neighbor 10.1.0.1 route-reflector-client
   neighbor 10.1.0.1 send-community standard extended large
   neighbor 10.1.0.9 remote-as 65000
   neighbor 10.1.0.9 next-hop-peer
   neighbor 10.1.0.9 description leaf-2
   neighbor 10.1.0.9 route-reflector-client
   neighbor 10.1.0.9 send-community standard extended large
   !
   address-family ipv4
      neighbor 10.1.0.1 activate
      neighbor 10.1.0.9 activate
      network 10.0.0.3/32
```

The only changes from the traditional IBGP configuration are:

* The neighbor IP addresses are interface addresses, not loopback addresses.
* There is no **neighbor update-source** command. The IP address of the outgoing interface is used as the [source address of the IBGP session](/2024/12/ibgp-source-interface-trivia/).
* The **neighbor next-hop-peer** command sets the BGP next hop in the incoming BGP updates to the peer IP address. The same command is used on the leaf switches[^NHP].

[^NHP]: This nicely circumvents the "[does **next-hop-self** apply to reflected routes?](/2022/04/eos-route-reflector-next-hop-self/)" question.

Here's the BGP table from one of the leaf switches:

{{<cc>}}BGP table on leaf-1{{</cc>}}
```
leaf-1#show ip bgp
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
 * >      10.0.0.2/32            10.1.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.3
 *        10.0.0.2/32            10.1.0.6              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.3
 * >      10.0.0.3/32            10.1.0.2              0       -          100     0       i
 * >      10.0.0.4/32            10.1.0.6              0       -          100     0       i
 * >      172.16.0.0/24          -                     -       -          -       0       i
 * >      172.16.1.0/24          10.1.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.3
 *        172.16.1.0/24          10.1.0.6              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.3
 ```
 
 As you can see:
 
 * The leaf switch receives remote routes from two spine switches.
 * The BGP next hops are set to the IP addresses of the spine switches.

Not surprisingly, `leaf-1` can ping the loopback IP address of `leaf-2`, proving the end-to-end connectivity:

```
leaf-1#ping ip leaf-2 source 10.0.0.1
PING leaf-2 (10.0.0.2) from 10.0.0.1 : 72(100) bytes of data.
80 bytes from leaf-2 (10.0.0.2): icmp_seq=1 ttl=63 time=0.649 ms
80 bytes from leaf-2 (10.0.0.2): icmp_seq=2 ttl=63 time=0.349 ms
80 bytes from leaf-2 (10.0.0.2): icmp_seq=3 ttl=63 time=0.459 ms
80 bytes from leaf-2 (10.0.0.2): icmp_seq=4 ttl=63 time=0.489 ms
80 bytes from leaf-2 (10.0.0.2): icmp_seq=5 ttl=63 time=0.520 ms

--- leaf-2 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4ms
rtt min/avg/max/mdev = 0.349/0.493/0.649/0.096 ms, ipg/ewma 1.000/0.572 ms
```

Want to repeat my tests? The easiest way would be to use [netlab-examples repository with GitHub Codespaces](/2024/07/netlab-examples-codespaces/) ([import Arista EOS container if needed](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) and change the directory to `BGP/interface-IBGP`).

### Benefits and Drawbacks

Should you use this design? Probably not, but let's go through the benefits and drawbacks:

**Benefits**:

* You don't need to deal with BGP AS numbers. BGP CLUSTER_LIST attribute replaces the AS_PATH attribute as the loop prevention mechanism. 
* You don't need to worry about the BGP update interval. Most implementations do not delay/batch IBGP updates.
* You don't have to worry about [valley-free routing](/2018/09/valley-free-routing-in-data-center/) or path hunting. Leaf switches will not reflect IBGP routes. 
* Your job security has increased by a few percentage points.
* You can go to conferences and boast about how cool you are.

**Drawbacks**

* You're relying on implementations deviating from the recommended behavior.
* I never tested whether BFD would work on IBGP sessions.
* You might be the only one in the world using this design, so you might be the first one to discover subtle bugs. Good luck persuading the vendor to fix them unless you're armed with a ginormous purchase order.

Anything else? Please write a comment!
