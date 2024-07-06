---
date: 2016-09-22 13:59:00+02:00
dcbgp_tag: server
ospf_tag: trust
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

> You categorically reject the use of OSPF, but we have a couple of customers using it quite happily. I'm sure you have [good reasons](/2013/08/virtual-appliance-routing-network.html), and the reasons you list [in the presentation] are ones I agree with. OTOH, why not use totally stubby areas with hosts in such an area?

How about:
<!--more-->
**Because OSPF stub areas would be a total mess to configure?** Hmm... maybe not really; we could make it reasonably easy, particularly with network automation.

**One host going crazy would impact at least all other hosts in the same area**. It's not as bad as running servers in the backbone area, but still. Maybe it's irrelevant if you're running the same version of FRR on both ends (on the Top-of-Rack switch and the server).

**Because you couldn't filter the prefixes announced by the host?** Well, you could control the summarization of prefixes from the totally stubby area into the backbone area (at least in theory; I'm not sure how many data center switch vendors implemented that). However, within the area, you'd still trust everyone. That might not be a problem if you control all the hosts, but it would be a huge deal if you don't... and it would be a nirvana for any intruder trying to move laterally.

**Because you can't implement routing policies (like _no transit_) in OSPF?** I've seen designs where an IBM mainframe was a single link failure away from becoming a transit router.

Finally, the server-to-network interface is usually a trust boundary, and **I don't believe in running OSPF across trust boundaries**. Maybe that's less of an issue if the same team controls the servers and the network and runs the same routing software on both, but I definitely wouldn't run OSPF with just any software that happens to be lying around on a host.

Or maybe it's just that **I like BGP** and keep inventing reasons why it's the best tool for the $job.
