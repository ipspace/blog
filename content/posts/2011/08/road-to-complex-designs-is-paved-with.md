---
date: 2011-08-15 07:21:00+02:00
tags:
- Internet
- BGP
- design
title: The Road to Complex Designs Is Paved with Great Recipes
url: /2011/08/road-to-complex-designs-is-paved-with/
---
A while ago someone asked me to help him troubleshoot his Internet connectivity. He was experiencing totally weird symptoms that turned out to be a mix of MTU problems, asymmetric routing (probably combined with RPF checks on ISP side) and non-routable PE-CE subnets. While trying to figure out what might be wrong from the router configurations, I was surprised by the amount of complexity he'd managed to introduce into his DMZ design by following recipes and best practices we all dole out in blog posts, textbooks and training materials.
<!--more-->
His DMZ was a typical redundant DMZ design: two routers connected to two ISPs and running BGP with them, and a redundant pair of firewalls, as illustrated in the following RFC-ready diagram:

```
PE-ISP-A    PE-ISP-B
    |           |
  CE-A        CE-B
    |           |
=======PUB-SUB=======
    |           |
  FW-A        FW-B
```

EBGP sessions were established between CE-A and PE-ISP-A and between CE-B and PE-ISP-B (perfect). There was an IBGP session between CE-A and CE-B (perfect), but it was *running between loopback interfaces*.

*OSPF was running in the DMZ* to propagate loopback interface addresses between CE-routers (otherwise IBGP session would not start) and *default route to* *the* *firewalls*. He was also redistributing PE-CE subnets into OSPF to fix BGP next hop issues.

Both CE-routers had **network** statements to advertise the public IP subnet (PUB-SUB) to the Internet (perfect) *and a static route to null 0* to ensure the PUB-SUB would always be advertised.

I could easily recognize each and every design choice he made; the whole DMZ was a perfect implementation of various BGP recipes that I can trace back to (at least) the BGP course I developed for Cisco Europe in mid-1990s. Note: I don't think I could claim to be the author of any one of them; they were always considered (at least by some) best practices.

While most of the recipes made his design more complex than necessary, the last one (*static route to null 0*) was actually harmful (as the [academics say](http://www.catb.org/jargon/html/E/exercise--left-as-an.html): the proof is left as an exercise for the reader -- post it in the comments).

There are numerous changes one could make to simplify this design, for example:

**Run IBGP session over directly-connected interface** (PUB-SUB). If you have two routers connected with a single link, it makes no sense to run IBGP session between loopback interfaces; loopbacks are useful if you have multiple alternate paths between the IBGP neighbors or if the IBGP neighbors are not directly connected.

**Use static default route on the firewalls and HSRP on the CE-routers**. This design is almost equivalent to the OSPF-in-the-DMZ design from the firewall perspective; **track** objects and HSRP priorities can get pretty close to whatever OSPF default route manipulation you can do on the CE-routers.

**Use next-hop-self on the IBGP session**. When IBGP routers advertise themselves as the BGP next-hop, the redistribution of PE-CE subnets into OSPF is no longer needed.

**Remove the static route to null0**. The IP subnet the CE routers have to advertise to the Internet is directly connected, so there's no need to create an artificial IP prefix in the IP routing table to support the BGP **network** statement.

Last but definitely not least, **remove OSPF from DMZ**, as all the reasons for using it are gone.

Anything else? Please write a comment! And while speaking of misapplied recipes, [*Knowledge or recipes*](/2008/09/knowledge-or-recipes/) blog post comes to mind.