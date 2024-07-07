---
title: "Intent-Based Networking: Another Victim of Sturgeon's Law"
date: 2020-05-18 07:41:00
tags: [ intent-based networking ]
intent-based-networking_tag: drawback
---
A few days ago Greg Ferro published an interesting post claiming [DHCP is an example of intent-based networking](https://etherealmind.com/was-dhcp-the-first-intent-networking-feature/) (a bit less tongue-in-cheek than my "_[so is OSPF configuration](/2017/09/intent-based-hype/)_" rant from 2017). BTW, so is RADIUS or TACACS+ ;)

He got quickly "corrected" by Phil Gervasi who loosely relied on [Gartner's definition of Intent-Based Networking](https://blogs.gartner.com/andrew-lerner/2017/02/07/intent-based-networking/), and claimed that an [intent-based networking system should have three major components](https://networkphil.com/2020/05/12/blog-response-dhcp-is-not-intent-based-networking/):
<!--more-->
* Network abstraction;
* Continuous validation;
* Autonomous remediation.

That seems like a reasonable and useful set of requirements, but guess what - any decent routing protocol meets these three criteria... and so does vCenter with VMware Tools and DRS (although in server virtualization, not networking domain). The proof is left as an exercise for the devious reader ;) 

Greg tried to save the day by trying to differentiate between [automated- and autonomous intent stack](https://networkphil.com/2020/05/12/blog-response-dhcp-is-not-intent-based-networking/) (in which case a routing protocol would be an example of autonomous intent stack), but unfortunately you can't win - like Software-Defined Networking, Intent-Based Networking is another fatality of [Sturgeon's Law](https://en.wikipedia.org/wiki/Sturgeon%27s_law) with a [meaningless name](/2018/06/what-is-intent-based-networking/) that a horde of well-paid marketers and industry analysts try to spin in 100 different ways hoping it will finally make sense to [naive PowerPoint consumers](/2011/09/long-distance-irf-fabric-works-best-in/).

We had systems with plenty of network abstraction decades ago. They were called Customer- or Service Management Systems, or Orchestration Systems, or Provisioning Systems.

Some of them included some sort of validation (Tail-F comes to mind), but we also designed networks in a way to make them autonomous and self-healing, reporting errors to the management system... and some of those management systems were able to perform pretty good root cause analysis in early 1990s.

If you wanted to add continuous validation and autonomous remediation to the mix, you could use tools like Cariden MATE... but nobody in their right mind allowed that tool to make automated changes to the network (or so Cariden's engineers told me) - the tool would propose changes, someone would review them, and then they got pushed into the devices.

Those tools never had a fighting chance to be a big hit in the modern networking industry landscape: they tried to cope with [never-ending MacGyverism](/2013/08/temper-your-macgyver-streak/) of networking engineers, and they were not "disruptive" enough to excite VCs or IT vendors' CEOs. Cariden was acquired for $141M, Tail-F for $175M, but a product implementing bridging over host-to-host tunnels at speeds barely exceeding 1 Gbps on modern x86 servers but branded with all the right buzzwords fetched a cool $1.26B.

So what's the big deal with _intent-based networking_? After everyone realized SDN is an ill-defined lame duck, someone invented another random buzzword to get funding, VCs got a new hype balloon to invest in, and industry analysts were only too happy to have another category to draw quadrants in. A pure win-win-win scenario.

You can happily participate in that game and enjoy glitzy product pitches... or you can take the red pill and do your homework:

* [Figure out what BUSINESS problem you're trying to solve](/2019/12/figure-out-what-problem-youre-trying-to/)
* Is it a [technology problem or a people/processes problem](/2017/10/are-you-solving-right-problem/)? You can never [fix a broken process](/2014/09/youve-been-doing-same-thing-for-last-20/) by throwing unproven technology at it.
* Can you [solve the problem with existing tools](/2014/03/network-automation-just-do-it/)?
* If not, [what tools would you need](/2019/01/network-automations-is-more-than-just/) to solve the problem?
* Even if you had those tools, would you be able to use them, or [would you be back to square one due to people/processes](/2013/11/typical-enterprise-application/)?

Want to know more? Explore our [Intent-Based Networking Resources ](/tag/intent-based-networking/) or watch [Intent-Based Networking](https://my.ipspace.net/bin/list?id=AutConcepts#INTENT) section of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
