---
date: 2022-10-06 06:05:00+00:00
evpn_tag: details
lastmod: 2022-11-03 16:36:00
tags:
- BGP
- EVPN
title: More Arista EOS BGP Route Reflector Woes
---
Most BGP implementations I've worked with split the neighbor BGP configuration into two parts:

* Global configuration that creates the transport session
* Address family configuration that activates the address family across a configured transport session and changes the parameters that affect BGP updates

AS numbers, source interfaces, peer IPv4/IPv6 addresses, and passwords clearly belong to the global neighbor configuration.

{{<note info>}}Starting with EOS release 4.29.0F, you can [configure the **neighbor next-hop-self** option within IPv4 and IPv6 address families](https://www.arista.com/en/support/toi/eos-4-29-0f/16340-next-hop-self-in-address-family-mode-for-ipv4-and-ipv6-unicast). Great job! Hopefully, we can consider this blog post a [historical curiosity](https://xkcd.com/979/).
{{</note>}}
<!--more-->
BGP policies like route maps and prefix lists clearly belong to the address family configuration, but what about route reflector clients and next-hop processing?

One might argue that these parameters belong to the address family configuration. After all, they affect BGP updates within an address family. One might also argue that having different route reflector topologies for individual address families doesn't make sense. That might have been the argument that caused Arista to implement **neighbor route-reflector-client** and **neighbor next-hop-self** commands on the global BGP configuration level. I would have no problem with that if only they were implemented consistently.

As I [described in April 2022](/2022/04/eos-route-reflector-next-hop-self.html), Arista EOS takes **next-hop-self** a bit too literally. That option also changes the next hops on reflected routes. No problem; one can also use the **bgp route-reflector preserve-attributes** command to fix it. The "only" remaining problem is that this command does not work on all address families, and there's no way to fix that.

Here are the relevant parts of the global BGP configuration *netlab* created when I started testing the [leaf-and-spine EVPN topology](https://github.com/ipspace/netlab/blob/dev/tests/integration/evpn/vxlan-bridging-leaf-spine.yml) with Arista EOS:

{{<figure src="/2022/10/vxlan-evpn-eos-topology.png" caption="BGP session topology">}}

{{<cc>}}Relevant parts of Arista EOS route reflector configuration created with *netlab* release 1.3{{</cc>}}
```
router bgp 65000
  bgp advertise-inactive
  bgp log-neighbor-changes
  no bgp default ipv4-unicast
  no bgp default ipv6-unicast
  router-id 10.0.0.7
  bgp cluster-id 10.0.0.7
  bgp route-reflector preserve-attributes
!
  neighbor 10.0.0.5 remote-as 65000
  neighbor 10.0.0.5 description l1
  neighbor 10.0.0.5 update-source Loopback0
  neighbor 10.0.0.5 next-hop-self
  neighbor 10.0.0.5 route-reflector-client
  neighbor 10.0.0.5 send-community standard extended

!
  neighbor 10.0.0.6 remote-as 65000
  neighbor 10.0.0.6 description l2
  neighbor 10.0.0.6 update-source Loopback0
  neighbor 10.0.0.6 next-hop-self
  neighbor 10.0.0.6 route-reflector-client
  neighbor 10.0.0.6 send-community standard extended
```

So far, so good. IPv4 works; the next hops are correct. Now for the EVPN part:

{{<cc>}}EVPN BGP configuration on Arista EOS route reflector{{</cc>}}
```
router bgp 65000
 address-family evpn
!
  neighbor 10.0.0.5 activate
  neighbor 10.0.0.6 activate
  neighbor 10.0.0.8 activate
```

Looks simple, right? The only problem is *it doesn't work*. No routes are reflected between L1 and L2. I tried all sorts of things, and the only way to get the EVPN route reflector to work was to remove the **neighbor next-hop-self** from the IBGP neighbors.

It looks like EVPN BGP AF processing ignores the **bgp route-reflector preserve-attributes** setting. As the change in the next hop would bring the traffic to the spine switch (which did not have the VXLAN interfaces to handle it), the spine switch decided not to send the updates.

Interestingly, you can configure **neighbor next-hop-unchanged**  within the EVPN address family. Still, it only applies to EBGP neighbors (you need that when you believe in building EBGP-only data centers). It does not affect the **neighbor next-hop-self** global setting.

OK, so I gave up and removed all the **neighbor next-hop-self** commands from the global configuration. All of a sudden, EVPN worked like a charm, but of course, the [test IBGP+EBGP topology](https://github.com/ipspace/netlab/blob/dev/tests/integration/bgp/ibgp-ebgp.yml) wouldn't work because the next hops of some routes (EBGP neighbors) wouldn't be reachable.

In the end, I was forced to use the BGP equivalent of the Swiss Army knife: a route map that sets the next hop ([netlab commit](https://github.com/ipspace/netlab/commit/be1c546aeb029960f231f3382ccf0768c918656a)), resulting in the following configuration:

{{<cc>}}Final Arista EOS BGP IPv4 configuration{{</cc>}}
```
route-map next-hop-self-ipv4 permit 10
   match route-type external
   set ip next-hop peer-address
!
route-map next-hop-self-ipv4 permit 20
!
 address-family ipv4
!
  network 10.0.0.7/32
!
  neighbor 10.0.0.5 activate
  neighbor 10.0.0.5 route-map next-hop-self-ipv4 out
  neighbor 10.0.0.6 activate
  neighbor 10.0.0.6 route-map next-hop-self-ipv4 out
```

### More Information

* Want to reproduce my tests? [Install netlab](https://netlab.tools/install/) and [use Arista cEOS containers](https://netlab.tools/labs/ceos/).
* Want to learn more about EVPN? There's probably no better source than [EVPN Deep Dive webinar](https://www.ipspace.net/EVPN_Technical_Deep_Dive) with Dinesh Dutt (the author of *BGP in the Data Center*), Lukas Krattiger (the author of *Building Data Centers with VXLAN BGP EVPN*), and Krzysztof Grzegorz Szarkowicz (the author of *MPLS in the SDN Era*)

### Revision History

2022-11-03
: Arista EOS supports per-AF next-hop-self in release 4.29.0F
