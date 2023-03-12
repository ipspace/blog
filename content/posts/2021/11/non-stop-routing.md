---
date: 2021-11-11 06:54:00+00:00
distributed-systems_tag: device
ha-switching_tag: mechanism
high-availability_tag: external
series:
- ha-switching
- distributed-systems
series_title: Non-Stop Routing (NSR)
tags:
- IP routing
- high availability
title: Non-Stop Routing (NSR) 101
---
After [Non-Stop Forwarding](/2021/09/non-stop-forwarding.html), [Stateful Switchover](/2021/09/stateful-switchover.html) and [Graceful Restart](/2021/09/graceful-restart.html), it's time for the pinnacle of *high-availability switching*: Non-Stop Routing (NSR)[^JNSR].

The PowerPoint-level description of this idea sounds fantastic:

* A device runs two active copies of its control plane.
* There is no cold/warm start of the backup control plane. The failover is almost instantaneous.
* The state of all control plane protocols is continuously synchronized between the two control plane instances. If one of them fails, the other one continues running.
* A failure of a control plane instance is thus invisible from the outside.

If this sounds an awful lot like [VMware Fault Tolerance](https://blog.ipspace.net/2011/08/high-availability-fallacies.html), you're not too far off the mark.
<!--more-->
[^JNSR]: Juniper calls this functionality Nonstop Active Routing.

Unfortunately, VMware FT becomes totally useless once the hardware reliability exceeds software reliability -- in you feed two VM instances the same inputs and one of them crashes, it's quite likely that the other one will crash at the same time. One can only hope the vendors implementing this concept (it seems like Cisco, Juniper and Huawei support something along these lines) did something smarter than that.

Non-Stop Routing seems like a no-brainer from the software architecture perspective (ignoring a bunch of minor details like the need to have BGP TCP sessions somewhat-open in two independent TCP stacks):

* Store the state of a control-plane protocol in a distributed key-value store that's automatically synchronized across all control-plane instances;
* Whenever processing incoming messages, make sure the state is fully synchronized before acknowledging the message and updating the session counters. If the control plane instance processing the message crashes before the state has been propagated, the other instance can claim packet loss and request retransmission.
* Apply similar principles to outbound messages.

Does that mean we should use NSR whenever possible? In the ideal world, the answer would be "yes, of course!" As [Erik Auerswald wrote](https://blog.ipspace.net/2021/10/big-picture-bfd-nsf-gr.html):

> IMHO NSR/SSO should be implemented completely transparently and always be enabled when there are two or more control plane processors. Why even have hardware redundancy for the control plane when it does not work well enough to enable unconditionally?

In reality, I would expect NSR implementations to look like a spaghetti mess of band-aids on top of 30 years old code. Vendors cautiously recommend to use it when the adjacent devices don't support Graceful Restart functionality, and you have to enable NSR for individual control plane protocols[^SUP], and even for individual BGP address families. 

[^SUP]: Assuming the control plane protocols you're using support NSR. Trying to figure out what works and what doesn't work from Cisco IOS XE 17 documentation turned out to be such a royal PITA that I gave up in disgust. Cisco IOS documentation was once a shining beacon in the bleak world of networking industry (lack of) documentation and turned into a total nightmare when I was busy looking somewhere else.

I would also worry about the simultaneous crashes caused by malformed incoming packets or corrupt internal data structures. If a control plane protocol instance crashes when trying to process an incoming packet, why would the second instance not crash when faced with a retransmitted packet and the same data structures?

**Long story short**

* Be very careful.
* NSR might not be able to protect you against software failures, and software failures are way more likely than hardware failures.
* Proper design beats convoluted vendor tricks every time.
