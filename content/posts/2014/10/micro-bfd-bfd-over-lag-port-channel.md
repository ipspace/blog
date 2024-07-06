---
date: 2014-10-20 07:15:00+02:00
tags:
- link aggregation
- IP routing
title: 'Micro-BFD: BFD over LAG (Port Channel)'
url: /2014/10/micro-bfd-bfd-over-lag-port-channel.html
---
The discussion in the comments to my [*LAG versus ECMP*](/2014/10/lag-versus-ecmp.html) post took a totally unexpected turn when someone mentioned BFD failure detection over port channels (link aggregation groups -- LAGs).

What's the big deal?
<!--more-->
### What is BFD

Bidirectional Forwarding Detection (BFD) is a lightweight protocol that "*provides low-overhead, short-duration detection of failures in the path between adjacent forwarding engines*" (straight from [RFC 5880](http://tools.ietf.org/html/rfc5880)).

Networking engineers love BFD for several reasons:

-   It's simpler and less CPU-intensive than routing protocol adjacency messages;
-   It can be implemented in smart linecards, further reducing the control-plane CPU load, and making it possible to detect forwarding failures in milliseconds even on boxes with hundreds of interfaces (try doing that with OSPF);
-   It detects [byzantine failures](http://en.wikipedia.org/wiki/Byzantine_fault_tolerance) between two forwarding engines that cannot be reliably detected at physical and data-link layers.

BFD uses the principle of [*shared fate*](/2014/08/fate-sharing-in-ip-networks.html) to do its job -- it tests the actual transmission path using the same protocol (IP) as the forwarded traffic -- and thus reliably detects a forwarding failure in a simple transmission path, regardless of the number of components in the path.

{{<figure src="s1600-MicroBFD+-+Single+link.png" caption="BFD over a single link">}}

### BFD and LAG

LAG appears as a single layer-2 forwarding path to layer-3 forwarding engine. BFD messages can take any one of the links in the LAG (based on the LAG load balancing algorithm), breaking the *shared fate* assumption -- a forwarded packet traversing another LAG member link might encounter a partially failed component, and it's impossible for BFD to detect that.

{{<figure src="/2014/10/s1600-MicroBFD+-+BFD+over+LAG.png" caption="BFD over a Link Aggregation Group">}}

The only solution to this problem is to run BFD across *every* LAG member link -- the BFD code has to become LAG-aware and test end-to-end connectivity across every member link independently (see [RFC 7130](http://tools.ietf.org/html/rfc7130) for more details). Even more, LACP and BFD have to work in parallel -- a member is added to a LAG only when both LACP and BFD agree it's OK to do so.

{{<figure src="s1600-MicroBFD+Sessions.png" caption="Micro BFD sessions over LAG">}}

## More information

I discussed the role of BFD in fast convergence in the *[Advanced Routing Protocol Topics](https://my.ipspace.net/bin/list?id=Net101#ADV_ROUTING)* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.
