---
date: 2016-07-26 13:50:00+02:00
dr_tag: fail_fix
high-availability_tag: dr
series:
- dr
tags:
- bridging
- data center
- WAN
- ACI
- high availability
title: Stretched ACI Fabric Is Sometimes the Least Horrible Solution
url: /2016/07/stretched-aci-fabric-is-sometimes-least.html
---
One of my readers sent me a lengthy email asking my opinion about his ideas for new data center design (yep, I pointed out [there's a service for that](http://www.ipspace.net/ExpertExpress) while replying to his email ;). He started with:

> I have to design a DR solution for a large enterprise. They have two data centers connected via Fabric Path.

There's a red flag right there...
<!--more-->
While it's definitely better to use Fabric Path (or Avaya's SPB fabric, or Brocade's Metro VCS Fabric) than the MLAG-over-WAN kludges, extending bridging across two data centers makes them a [single failure domain](http://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html), as some people [found out the hard way](http://blog.ipspace.net/2016/01/the-sad-state-of-enterprise-networking.html).

> Most of the applications run in a HA manner in both locations.

I wonder why people [still think that's a good idea](http://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html). Loss of DCI link will probably just break every application running across both locations (if the application would be written correctly they wouldn't need L2 extension anyway).

> Services run in a HA manner - one service device is active in one location and standby in the other. They communicate via Layer 2.

Stretched firewalls [never made much sense](http://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html), but the [vendors are making sure the myth persists](http://blog.ipspace.net/2015/11/stretched-firewalls-across-layer-3-dci.html). However, let's not go there...

Anyway, the reader's idea was to replace Fabric Path with ACI:

> According to Cisco and to your webinars ACI is a good candidate for a DR solution.

I don't remember ever saying ACI is a good candidate for a DR solution ;), but it's definitely the [least horrible one](http://blog.ipspace.net/2015/03/cisco-aci-stretched-fabric-that.html). In fact, any solution that replaces bridging with host routing (ACI, DFA or Cumulus Linux *redistribute ARP*) is infinitely better than stretched VLANs because it removes the uncontrolled flooding behavior that's the root cause of many catastrophic network failures.

Finally, as my reader was talking about *disaster recovery* I advised him to go back and talk about the [real business needs](http://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html). Once you get into that discussion, you often realize you don't need stretched layer-2 fabrics, because the other infrastructure (example: storage) doesn't support fully automated recovery.

### Want to Know More?

Watch the [Building Active-Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar or the [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course.