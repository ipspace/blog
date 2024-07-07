---
date: 2018-06-13 08:52:00+02:00
intent-based-networking_tag: overview
tags:
- automation
- intent-based networking
title: What Is Intent-Based Networking?
url: /2018/06/what-is-intent-based-networking/
---
Whenever someone mentions *intent-based networking* I try to figure out what exactly they're talking about. Not surprisingly, I get a different answer every single time. Confused by all that, I tried to find a good definition, but all I could find was vendor marketing along the lines of "*Intent-based networking captures and translates business intent so that it can be applied across the network,*" or industry press articles regurgitating vendor white papers.
<!--more-->
{{<note info>}}This blog post is a summary of the introductory part of [*Intent-Based Networking*](https://my.ipspace.net/bin/list?id=AutConcepts#INTENT) section of [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar. That webinar includes other aspects of intent-based networking like layers of abstraction, network-wide intent, intent validation and automated remediation.

The blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.{{</note>}}

Next step: if we can't find a good definition of what intent-based networking is, maybe we should define what intent is. Here's what Merriam-Webster has to say on the topic:

> Intent: a usually clearly formulated or planned intention.

Not exactly useful. So, what is an intention?

> Intention: what one intends to do or bring about

To be fair, there are other more useful definitions, but you get my point: we're pretty close to "[*recursion: see recursion*](http://www.catb.org/jargon/html/R/recursion.html)".

However, when reading vendor whitepapers, it seems most everyone who managed to move beyond fluff understands *intent-based networking* as *telling the network what to do and not how to do it*.

Now think about the way we deal with network devices. Did you ever tell a device *how* to do its stuff or did you tell it *what* you want to have done?

Unfortunately for tinkerers and fortunately for most networks we cannot tell the network devices *how* to do stuff, we can only tell them *what* we want to get done. For example, we tell a network device that we want OSPF running on a set of links, not how it should run OSPF or select the best paths.

Side note: every now and then there's a networking engineer who's pushing the devices beyond their design limits (example: running 1000 OSPF routers in an area, or redistributing the whole Internet routing table into OSPF), or trying to save his broken design by tweaking the way network devices do stuff... and thus the ever-more-convoluted nerd knobs are born.

To recap: like the network devices (apart from unmanaged hubs and cables) were always software-defined, the way we're configuring network devices has always been intent-based. *Intent-based Networking* is thus as meaningless (as a term) as *Software-Defined Networking*.

However, that doesn't mean that some of the ideas advertised by intent-based vendors are not useful. More about that in other [blog posts in this series](/tag/intent-based-networking/) and in the [Network Automation Concepts](https://www.ipspace.net/Network_Automation_Concepts) webinar.
