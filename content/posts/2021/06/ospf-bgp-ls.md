---
date: 2021-06-23 06:56:00+00:00
ospf_tag: mp
tags:
- SDN
- OSPF
- BGP
title: Why Do We Need BGP-LS?
---
One of my readers sent me this interesting question:

> I understand that an SDN controller needs network topology information to build traffic engineering paths with PCE/PCEP... but why would we use BGP-LS to extract the network topology information? Why can’t we run OSPF with controller by simulating a software based OSPF instance in every area to get topology view?

There are several reasons to use BGP-LS:
<!--more-->
* It uses BGP and thus TCP transport. It's trivial to setup a BGP session between an SDN controller and any router in your network (ideally at least two routers per area). Establishing OSPF adjacencies with routers across your network would require building GRE tunnels.
* BGP-LS is a one-way information exchange. The controller can get the topology information, but cannot influence the routing. An OSPF area is a single failure domain -- any router participating in an OSPF area can inject any information into the OSPF topology database.
* Corollary: when using BGP-LS, bugs in the SDN controller cannot cannot bring down the network. When an SDN controller running OSPF with your network goes bonkers all bets are off[^1].

Moving from BGP-LS to PCEP:

> Why can't we use something like fibbing to control traffic paths?

Fibbing always felt like a proof-of-concept to me. It does allow you to steer traffic *in an OSPF network* assuming *all destinations you're interested in are external routes*, but does not introduce virtual circuits like MPLS-TE does[^2], so it cannot implement scenarios that cannot be implemented with hop-by-hop destination-only packet forwarding (the *fish diagram* comes to mind).

{{<figure src="/2021/06/TE-Fish.png" caption="Desired traffic flow: X-A-B-E-Z and Y-A-C-D-E-Z cannot be implemented with fibbing">}}

For more details:

* Listen to the _[Fibbing: OSPF-Based Traffic Engineering](/2015/11/fibbing-ospf-based-traffic-engineering/)_ episode of _[Software Gone Wild Podcast](https://www.ipspace.net/Podcast/Software_Gone_Wild/)_;
* Watch the _[PCEP and BGP-LS Deep Dive](https://www.ipspace.net/PCEP_and_BGP-LS_Deep_Dive)_ webinar.
* For a bigger picture, watch the 
_[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)_ part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.

{{<note free>}}Both webinars mentioned above are available with _[Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free)_{{</note>}}

[^1]: That's also the reason I'm [highly recommending running BGP between your data center fabric and virtual appliances](/2013/08/virtual-appliance-routing-network/). It looked like the VMware NSBU grasped the concept when they made BGP the only routing protocol supported in NSX-T, but of course the sane days didn't last long... NSX-T 3.1.1 [added OSPF support to NSX Edge](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/3.1/rn/VMware-NSX-T-Data-Center-311-Release-Notes.html).

[^2]: *Virtual circuits* are the important bit -- it doesn't matter whether they're established with RSVP, PCEP, or segment routing label stack pushed into head-end device.
