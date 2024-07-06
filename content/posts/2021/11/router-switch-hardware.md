---
title: "Hardware Differences between Routers and Switches"
date: 2021-11-18 07:35:00
tags: [ switching ]
---
One of my readers sent me this age-old question:

> Is there a real difference in the underlying hardware of switches and routers in terms of the traffic processing chips and their capabilities in terms of routing and switching (or should I say only switching)?

Let's get the terminology straight. [Router](/2010/07/bridging-and-routing-is-there.html) is a technical term for a device that forwards packets based on network layer information. [Switch is a marketing term](/2011/02/how-did-we-ever-get-into-this-switching.html) for a device that does something with packets.

Rephrasing the question: is there a hardware difference between a box *marketed as a router* and another box *marketed as a layer-3 switch*?

**TL&DR: Yes.**
<!--more-->
Doing packet forwarding at high speeds is expensive, and simpler forwarding pipeline results in cheaper (or faster) silicon. 

If you don't need complex high-speed functionality (like a thousand interface output queues with per-flow classifier), you create a simpler ASIC and call the device a switch. If you thrive on overpriced products, you create as complex an ASIC as you can make it and call the device using it a router. EX9200 is an obvious counterexample, but then Juniper always looked like DEC of networking to me.

There’s even a difference in capabilities between spine- and leaf data center switches (example: Broadcom Tomahawk versus Trident), or sometimes between edge and core routers (example: Juniper MX- versus PTX-series)

For example, the Broadcom Tomahawk ASIC (spine) has limited VXLAN support, while the Broadcom Trident-3 ASIC (leaf) can do VXLAN bridging and routing.

On the WAN edge, you’d want to have more buffers (due to speed mismatch), maybe more queues (in case you want to do QoS), tunneling mechanisms beyond VXLAN, encryption beyond MACsec, or functionality like NAT that’s hard to implement in hardware.

While you can use a deep-buffer data center switching ASIC like Broadcom Jericho as a WAN edge router ([example](/2015/10/sdn-internet-router-is-in-production-on.html)), you’d be pretty limited in what that router can do. It would be awesome in terms of forwarding performance and relatively cheap, but it wouldn’t have all the bells and whistles people usually want to see in a device called router for no particular reason.

Is there a need for the difference? If you know what you’re doing, you buy the optimal box for your needs, and you don’t care how it’s called. If you have no idea because you were not able to get a reasonable set of requirements apart from "*as fast as possible, and make it future-proof*", then you buy an expensive insurance policy called *router* believing that if you ever need that stuff, you can just configure it.

And that (plus a [gazillion similar stupidities](/2013/08/temper-your-macgyver-streak.html)) is [what makes enterprise networking so complex](/2013/04/this-is-what-makes-networking-so-complex.html) and expensive.

### Beyond Marketing

Want to know what the real difference between routing and bridging (or should I say *layer-2 switching* and *layer-3 switching*) are? Watch _[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)_ section of the _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.

