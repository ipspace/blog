---
date: 2011-04-18 06:29:00.010000+02:00
high-availability_tag: ignore
ha-cluster_tag: firewall
needs_fix: true
series:
- ha-cluster
tags:
- firewall
- data center
- load balancing
- WAN
- high availability
title: 'Distributed Firewalls: a Ticking Bomb'
url: /2011/04/distributed-firewalls-how-badly-do-you/
---
Are you ever asked to use a layer-2 Data Center Interconnect to implement distributed active-active firewalls, supposedly solving all the L3 issues and asymmetrical-traffic-flow-over-stateful-firewalls problems? Don't be surprised; I was stupid enough (or maybe just blinded by the L2 glitter) in 2010 to draw the following diagram illustrating a sample use of VPLS services:
<!--more-->
{{<figure src="/2011/04/s1600-SS_FW.png" caption="Distributed Firewalls Connected with Layer-2 Data Center Interconnect">}}

The solution looks ideal: both WAN routers would advertise the same IP prefix to the outside world, attract the customer traffic and pass the traffic through the nearest firewall. The inside routers would take care of proper traffic distribution (inbound traffic might need to traverse the DCI link) and the return traffic would follow the shortest path toward the WAN (or Internet) cloud. The active-active firewalls would exchange flow information, solving the asymmetrical flow problems.

Now ask yourself: what happens if the DCI link fails? Some of the inbound traffic will arrive to the wrong edge router and get dropped, and the firewalls will go into split-brain mode. You'll clearly experience problems in both data centers.

Usually we use pairs of devices (routers and firewalls in this particular example) in redundant configurations to increase the overall system availability. I am no expert in high availability calculations, but one of the hidden assumptions in designs where devices have to exchange state information (active-active firewalls, for example) is that the non-redundant component (the link between the devices) has to be as reliable as the devices themselves.

In a stretched subnet design the weakest link of the whole system is the data center interconnect; in most cases, stretched subnets would decrease the overall availability of the system.

A reliable layer-3 solution is not much easier to design. A while ago I was involved in a redesign of a global network. The customer had very knowledgeable networking team (it was a total pleasure working with them) and we tried really hard to find a redundant data center design that would allow them to advertise a single L3 prefix from both data centers. We even reached the point where we had a working design that would survive all sorts of failures, but it got too complex for the customer (and they were absolutely right to reject it and fall back to simpler options).

Unless you believe in the miracles of TCP-based anycasting, it seems the best option you have to implement distributed data centers is still the time-proven design: DNS-based load balancing between data centers in combination with data-center-specific+summary-as-a-backup prefix advertising into BGP.

{{<figure src="/2011/04/s1600-SS_LB.png" caption="DNS-based multisite load balancing">}}

{{<note warn>}}You have to move the firewalls deeper into the data center if you want to avoid session loss following an Internet link failure.{{</note>}}

### More information

The [*Data Center Interconnects*](https://www.ipspace.net/DCI) webinar describes numerous design and implementation aspects of L2 and L3 data center interconnects, but if you want to design a reliable data center multisite architecture, you REALLY SHOULD watch the _[Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)_ webinar.

### Related Blog Posts

* [Sometimes You Have to Decide How Badly You Want to Fail](/2015/10/sometimes-you-have-to-decide-how-badly/)
* [Do I Need Redundant Firewalls?](/2016/10/do-i-need-redundant-firewalls/)
* [Stretched Firewalls across Layer-3 DCI? Will the Madness Ever Stop?](/2015/11/stretched-firewalls-across-layer-3-dci/)
* [Stretched VLANs and Failing Firewall Clusters](/2019/11/stretched-vlans-and-failing-firewall/)
