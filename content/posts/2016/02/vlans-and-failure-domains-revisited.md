---
date: 2016-02-24 09:09:00+01:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- bridging
- data center
- workshop
- fabric
- high availability
title: VLANs and Failure Domains Revisited
url: /2016/02/vlans-and-failure-domains-revisited/
---
My friend [Christoph Jaggi](http://uebermeister.com/about.html), the author of fantastic [Metro Ethernet and Carrier Ethernet Encryptors](/2015/06/just-out-metro-and-carrier-ethernet/) documents, sent me this question when we were discussing the [Data Center Fabrics Overview workshop](http://www.digs.ch/digs-workshop-data-center-fabrics-overview/) I'll run in Zurich in a few weeks:

> When you are talking about large-scale VLAN-based fabrics I assume that you are pointing towards highly populated VLANs, such as VLANs containing 1000+ Ethernet addresses. Could you provide a tipping point between reasonably-sized VLANs and large-scale VLANs?

It\'s not the number of hosts in the VLAN but the span of a bridging domain (VLAN or otherwise).
<!--more-->
### Before We Start

Please note that I\'m looking at the problem purely from the data center perspective - transport VLANs offered by Metro Ethernet or VPLS service providers are a totally different story for several reasons:

-   There\'s a difference between [providing transport service and being responsible for the whole infrastructure](/2012/07/the-difference-between-metro-ethernet/) (and all stupidities people do on top of it);
-   Sensible people don\'t bet their whole IT infrastructure on a single service provider (those that do eventually get the results they deserve). Failure in the transport network is thus not as critical as a data center failure;
-   Sensible people isolate their internal networks from transport network failures by using *routing functionality* between their LAN and WAN networks. Some data center architects happily extend a single (v)LAN network across a WAN network.

### What Could Possibly Go Wrong?

There are two failure scenarios I often see when [people come to me](http://www.ipspace.net/ExpertExpress) after [experiencing a data center meltdown](/2016/01/the-sad-state-of-enterprise-networking/):

-   [bridging loop caused by a host (or VM)](/2011/11/virtual-switches-need-bpdu-guard/);
-   bridging loop on the fabric edge - from something as stupid as technicians plugging TX fiber in RX port or [connecting two ports](/2012/04/stp-loops-strike-again/) to see if the fiber is OK (sometimes [coupled with device misconfiguration](/2015/06/another-spectacular-layer-2-failure/)) to software bugs in MLAG implementations.

The first one is annoying, the second one is catastrophic, as the ToR switches easily do packet flooding at wire speed.

### Back to the Failure Domains

In any case, anyone that\'s part of the same VLAN gets affected, and if someone (in their infinite wisdom) configured [all VLANs on all server-facing ports](/2011/12/vm-aware-networking-improves-iaas-cloud/) because that\'s easier than actually talking with the server/virtualization team or [deploying a VLAN provisioning solution](/2013/03/what-did-you-do-to-get-rid-of-manual/), every server gets impacted.

Furthermore, every link that the affected VLAN crosses has to carry the unnecessary traffic. Not a big deal if you have a 10Gbps bridging loop at the network edge and 40 Gbps fabric links, but a major disaster if your bridging domain includes 1Gbps or 10Gbps links between data centers.

### It's Not a Numbers Game

Christoph continued his question with two example:

> 1 VLAN = 1 failure domain\
> 100 VLANs = 100 separate failure domains

Not necessarily. The 100 VLANs touch all the core links, so there's at least partial overlap between them (a bridging loop in a VLAN that results in saturation of DCI link will kill all other VLANs traversing that link), and if the networking team configured every VLAN on every server-facing port to make their lives easier, the whole data center fabric becomes a single failure domain.

> 1 VLAN - 100 MAC-adresses = I am OK\
> 1 VLAN - 1000 MAC addresses = I am close to the limit\
> 1 VLAN = 2000 MAC adresses = I am looking for trouble\
> 1 VLAN = 3000+ MAC adresses = I will get into trouble

That's the traditional view of the problem: bridging doesn't scale because hosts are chatty and more hosts in a VLAN result in more flooding overhead.

In reality, you will get into trouble with many IP nodes (hosts or routers) in the same VLAN (that's why some large layer-2 fabrics use ARP sponges), but the most common causes of network meltdowns that I see are the bridging loops.
