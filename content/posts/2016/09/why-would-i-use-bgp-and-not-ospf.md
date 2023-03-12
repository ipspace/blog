---
date: 2016-09-22 13:59:00+02:00
dcbgp_tag: server
series:
- dcbgp
series_weight: 800
tags:
- design
- OSPF
- data center
- fabric
- BGP
title: Why Would I Use BGP and not OSPF between Servers and the Network?
url: /2016/09/why-would-i-use-bgp-and-not-ospf.html
---
While we were preparing for the Cumulus Networks' [Routing on Hosts](https://vimeo.com/171631723) webinar [Dinesh Dutt](https://www.linkedin.com/in/ddutt) sent me a message along these lines:

> You categorically reject the use of OSPF, but we have a couple of customers using it quite happily. I\'m sure you have [good reasons](https://blog.ipspace.net/2013/08/virtual-appliance-routing-network.html) and the reasons you list \[in the presentation\] are ones I agree with. OTOH, why not use totally stubby areas with the hosts being in such an area?

How about:
<!--more-->
**Because OSPF stub areas would be a total mess to configure?** Hmm... maybe not really, we could make it reasonably easy, particularly with network automation.

**One host going crazy would impact at least all other hosts in the same area**. Definitely not as bad as running servers in backbone area but still. Maybe it's not so relevant if you're running the same version of FRR on both ends.

**Because you couldn't filter the prefixes announced by the host?** Well, you could control the summarization of prefixes from totally stubby area into backbone area (in theory, not sure many vendors actually implemented that), but within the area you'd still trust everyone. That might not be a problem if you control all the hosts, but would be a huge deal if you don't... and it would be a nirvana for any intruder trying to move laterally.

**Because you can't implement routing policies (like _no transit_) in OSPF?** I've seen designs where an IBM mainframe was a single link failure away from becoming a transit router.

Finally, server-to-network interface is usually a trust boundary, and **I don't believe in running OSPF across trust boundaries**. Maybe that's less of an issue if the same team controls the servers and the network, and runs the same routing software on both, but I definitely wouldn't run OSPF with just any software that happens to be lying around on a host.

Or maybe it's just that **I like BGP** and keep inventing reasons why it's the best tool for the \$job.

Want to know more? There's over 20 hours of goodies waiting for you in [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar.
