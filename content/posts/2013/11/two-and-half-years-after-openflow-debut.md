---
cdate: 2022-07-09
comment: 'SDN and the idea of centralized control plane were hotly debated in the
  early 2010s, and we tried to bring at least some sanity into the discussion. The
  so-called "_industry press_" couldn''t be bothered -- here’s my response to a particularly
  misleading article written in November 2013.


  Fun fact: while HP did have a few interesting [SDN/OpenFlow-based solutions](/2015/05/openflow-in-hp-campus-solutions-on/),
  they never managed to get any reasonable foothold beyond ~~cheap~~ optimally-priced
  campus networking, and finally resorted to acquisitions to stay in that business.

  '
date: 2013-11-11 05:59:00+01:00
sdn_hype_tag: clueless
series:
- sdn_hype
tags:
- SDN
- OpenFlow
title: Two and a Half Years after OpenFlow Debut, the Media Remains Clueless
url: /2013/11/two-and-half-years-after-openflow-debut/
---
If you repeat something often enough, it becomes a "fact" (or an urban myth). SDN is no exception, industry press [loves to explain SDN like this](https://web.archive.org/web/20140111002549/https://www.businessinsider.com/the-hp-woman-knocking-out-cisco-2013-11):

> \[SDN\] takes the high-end features built into routers and switches and puts them into software that can run on cheaper hardware. Corporations still need to buy routers and switches, but they can buy fewer of them and cheaper ones.

That nice soundbite contains at least one stupidity per sentence:
<!--more-->
**SDN cannot move hardware features into software**. If a device relies on hardware forwarding, you cannot move the same feature into software without significantly impacting the forwarding performance.

**SDN software runs on cheaper hardware**. Ignoring the intricacies of custom ASICs and merchant silicon (and the fact that Cisco produces more custom ASICs than all merchant silicon vendors combined), complexity and economies of scale dictate the hardware costs. It's pretty hard to make cheaper hardware with the same performance and feature set.

However, all networking vendors bundle the software with the hardware devices and expense R&D costs (instead of including them in [COGS](http://en.wikipedia.org/wiki/Cost_of_goods_sold)) to boost their perceived margins.

Does the above paragraph sound like Latin to you? Don't worry -- just keep in mind that software usually costs about as much (or more) as the hardware it runs on, but you don't see that.

**Corporations can buy fewer routers and switches**. It can't get any better than this. If you need 100 10GE ports, you need 100 10GE ports. If you need two devices for two WAN uplinks (for redundancy), you need two devices. SDN won't change the port count, redundancy requirements, or laws of physics.

**Corporations can buy cheaper \[routers and switches\]**. Guess what -- you still need the software to run them, and until we see price tags of SDN controllers, and do a TCO calculation, claims like this one remain wishful thinking (you did notice I'm extremely diplomatic today, didn't you?).
