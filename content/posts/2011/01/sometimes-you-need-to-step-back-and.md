---
date: 2011-01-13 10:04:00+01:00
dmvpn_tag: design
ospf_tag: dmvpn
tags:
- DMVPN
- OSPF
title: Sometimes You Need to Step Back and Change Your Design
url: /2011/01/sometimes-you-need-to-step-back-and.html
---
A few days ago I received the following e-mail from one of my readers:

> I am trying presently to put in place a DMVPN solution running OSPF. I was wondering if you ever saw a solution with dual hub dual cloud design with OSPF working in practice because since I started I have issue with asymmetric routing because of the OSPF functionality.

Actually, I did... and exactly the same setup is included in the tested router configurations you get with the [*DMVPN: from Basics to Scalable Networks*](http://www.ipspace.net/DMVPN) webinar. While there are many things that can go wrong with DMVPN, I've never heard about *asymmetric routing* problems, so I started to investigate what's actually going on.
<!--more-->
As the story unfolded in the subsequent e-mails, I figured out the poor guy had been trying all sorts of random fixes: changing OSPF network type, changing the number of DMVPN subnets (one subnet with two hubs or two subnets with one hub each), doing weird inter-area aggregation tricks, even changing the administrative distance of OSPF neighbors (which does not work too well with OSPF).

All that seemed totally weird; finally we managed to step back and focus on the business need: the two hub routers are widely separate (one is on the East Coast, the other one on the West Coast) and the spokes should use the closer one as the primary hub and the other one as the backup hub. I am positive the right combination of kludges could get you there with just two DMVPN subnets (one per hub), but a much cleaner design is the following:

**Create two DMVPN tunnels on each hub router.** One of them is the *primary* tunnel (with low OSPF cost), the other one is the *backup* tunnel (with high OSPF cost). Spokes that use the hub as their primary hub should connect to the *primary* tunnel; the others should connect to the *backup* tunnel.

**Create two DMVPN tunnels on each spoke router**. On the primary tunnel of the spoke router, use the parameters that match the *primary* tunnel on the *closer* hub router (hub IP address, tunnel key, NHRP network ID \...). Use low OSPF cost (preferably matching the cost on the hub) on that tunnel.

Do the same for the backup spoke tunnel, this time using the DMVPN parameters for *backup* tunnel on the *far away* hub router.

### Lessons Learned

The first problem I'm often encountering with very smart network engineers is the *CCIE mentality* (having nothing to do with actual engineers having that title, but with the way the lab exams are structured): they try to make the implementation work with existing broken design, no matter the complexity. CCIE lab exams (and lab preparation guides) have been pushing us in that direction for years.

Real life is different: you should strive to have a design that results in a minimalistic implementation (which will be easier to roll out, operate and troubleshoot). When the implementation becomes too complex, it's time to step back, rethink and potentially even change the design. Sometimes you have to go as far back as questioning the actual business needs ([long-distance vMotion](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) immediately comes to mind).

The second problem I see quite often is the lack of fundamental understanding of how networking technologies work. For example: trying to use point-to-multipoint OSPF network type in a Phase 2 DMVPN subnet makes absolutely no sense. You should discard that idea based on your understanding of how OSPF and DMVPN work, not based on a failed lab test.
