---
date: 2015-10-22 11:05:00+02:00
tags:
- IP routing
- CLNP
title: Was CLNP Really Broken?
url: /2015/10/was-clnp-really-broken.html
---
One of my readers sent me this question after listening to the [podcast with Douglas Comer](https://blog.ipspace.net/2015/10/douglas-comer-on-future-of-networking.html):

> Professor Comer mentioned that IP choose a network attachment address model over an endpoint model because of scalability. He said if you did endpoint addressing it wouldn't scale. I remember reading a bunch of your blog posts about CNLP (I hope I'm remembering the right acronym) and I believe [you liked endpoint addressing better](https://blog.ipspace.net/2015/05/reinventing-clns-with-l3-only-forwarding.html) than network attachment point addressing.

As always, the answer is "it depends" (aka "we're both right" ;).
<!--more-->
{{<note info>}}CLNP or CLNS? CLNS is Connection-Less (= datagram) Network Service, CLNP is Connection-Less Network Protocol (the protocol used to implement CLNS). I'll use CLNP throughout this blog post.{{</note>}}

Host-based addressing definitely doesn't scale beyond a very limited local domain. As every network designer knows, aggregating at multiple boundaries is the only way to go if you want to build large-scale networks, and both CLNP and IP use aggregation to scale. Even more, after total failure of IDRP, they both use BGP for inter-domain routing (available on Cisco IOS and Junos).

The "only" difference between the two is the micro-level behavior. CLNP routers track adjacent hosts (with ES-IS protocol) and advertise *host ID* of every host *within an area* in the intra-area routing protocol (level-1 IS-IS), whereas IP routers don't care about individual hosts (unless they have to forward traffic to those hosts) and advertise only the subnets with IP routing protocols. Beyond the local domain (IP subnet or CLNP area), IP and CLNP routing protocols advertise prefixes, and IP and CLNP routers use longest-prefix matching rules to forward traffic.

{{<note warn>}}The IP forwarding model doesn't change when you use IS-IS for IP routing -- IS-IS routers don't advertise host prefixes but IP subnets in the LSPs. Using IS-IS in TRILL or 802.1aq is a totally different story, as those environments don't propagate IP addresses or subnets in IS-IS LSPs.{{</note>}}

### Another History Lesson

IPv4 was designed in the days when [hosts had a single interface](https://blog.ipspace.net/2021/05/fundamentals-interface-node-addresses.html) connected to [thick coaxial cables](https://blog.ipspace.net/2015/04/what-is-layer-2-and-why-do-we-need-it.html), and the whole IPv4/IPv6 forwarding model reflects the world in which hosts could talk directly to each other, and use *default gateway* only when trying to get out of the local network.

CLNP's roots are older than that -- host-based addressing goes back to early DECnet days when the minicomputers were connected by a haphazard mesh of point-to-point leased lines, and having interface addresses instead of host addresses made absolutely no sense. CLNP retained two important DECnet principles -- host-based addressing and host-to-router protocol (ES-IS). These properties allow:

-   A host to find an adjacent router (mission impossible in early IP networks -- does anyone remember the fun of manual configuration);
-   Automatic failover between multiple first-hop routers (which came to IP way later with introduction of first-hop redundancy protocols);
-   Host discovery and liveliness detection on first-hop routers (decades later IP implementations hacked ARP/ND to get the same functionality);
-   Anyone in the network to build a network-to-MAC address table (no more [RARP kludges on hypervisor switches](http://www.fragmentationneeded.net/2015/10/musings-on-datanauts-9.html));
-   **Unlimited host mobility within the local domain**;

The host-based addressing used by CLNP and the idea that hosts and routers discover each other made it an easy fit to any network topology, whereas the rigid IP subnet model (made worse by fixed classful boundaries) started breaking down the moment we [replaced coaxial cables with bridges](https://blog.ipspace.net/2010/07/bridges-kludge-that-shouldnt-exist.html) (anyone remembers the beauties of [Local Area Mobility](http://blog.ipspace.net/2012/08/mobile-arp-in-enterprise-networks.html)?), resulting in the nightmares we have to deal with in the data center environments to [support VM mobility](http://blog.ipspace.net/2012/03/video-networking-requirements-for-vm.html).

Not surprisingly, the networking industry started reinventing the wheel (there are only so many ways to get a job done) and [rediscovered the CLNP principles](https://blog.ipspace.net/2015/05/reinventing-clns-with-l3-only-forwarding.html) when trying to make IP work better, first with [anycast first-hop gateways](http://blog.ipspace.net/2013/06/vrrp-anycasts-fabrics-and-optimal.html) to bypass the problems of fixed first-hop gateway, later with host routing (Cisco's DFA, EVPN) based on ARP/ND snooping, and finally [full-blown layer-3-only networks](http://blog.ipspace.net/2015/04/rearchitecting-l3-only-networks.html) ([Enterasys Fabric Routing](http://blog.ipspace.net/2013/08/enterasys-host-routing-optimal-l3.html), [Cumulus Networks' Redistribute ARP](http://blog.ipspace.net/2015/08/layer-3-only-data-center-networks-with.html)).
