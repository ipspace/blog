---
anycast_tag: design
date: 2016-11-28 09:46:00+01:00
high-availability_tag: external
series:
- anycast
series_title: Ingress Traffic Flow in Multi-Data Center Deployments
tags:
- design
- data center
- WAN
- high availability
title: 'Q&A: Ingress Traffic Flow in Multi-Data Center Deployments'
url: /2016/11/q-ingress-traffic-flow-in-multi-data/
---
One of my readers was watching the [Building Active-Active Data Centers webinar](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) and sent me this question:

> I'm wondering if you have additional info on how to address the ingress traffic flow issue? The egress is well explained but the ingress issue wasn't as well explained.

There's a reason for that: there's no good answer.
<!--more-->
### The Problem

Let's briefly describe the problem before going into the details. Assume someone forced you to deploy stretched VLANs (so you have the same subnet in multiple locations) or you only got a single /24 from your ISP or RIR (because that's all that's left and since [nobody uses IPv6 yet](https://www.google.com/intl/en/ipv6/statistics.html) going there is not an option -- hope you noticed the sarcasm).

In both cases you have to advertise the same /24 from multiple data centers and the clients are confused: which way should they go? Here's the diagram I used in the webinar:

{{<figure src="/2016/11/s1600-Ingress+Traffic+Flow.jpg" caption="Ingress traffic flow when multiple sites advertise the same prefix">}}

## Potential Solutions

If your problem is lack of address space, you could use anycast: advertise the same prefix from multiple data centers, but terminate the TCP sessions on a different set of load balancers, all using the same outside IP address. Works surprisingly well across the global Internet (just ask [CloudFlare](https://blog.cloudflare.com/a-brief-anycast-primer/) or [LinkedIn](https://engineering.linkedin.com/network-performance/tcp-over-ip-anycast-pipe-dream-or-reality)).

If however someone forced you to implement a stretched subnet design, or you did it on your own because you [trust your $vendor](/2016/01/the-sad-state-of-enterprise-networking/) and [you know you can make it work](/2013/08/temper-your-macgyver-streak/), you're in deep \*\*\*\* anyway. [There's no good solution](/2015/10/sometimes-you-have-to-decide-how-badly/), particularly if the traffic has to traverse any stateful service (please don't get me started on [stretched](/2011/06/stretched-clusters-almost-as-good-as/) [firewall clusters](/2011/04/distributed-firewalls-how-badly-do-you/)).

I spent a lot of time a while ago describing the [intricacies of redundant Internet connectivity](http://content.ipspace.net/get/X1%20Redundant%20Data%20Center%20Internet%20Connectivity.mp4) (free video) and [wrote a case study documenting how you might solve the external routing with L2 DCI](http://www.ipspace.net/External_Routing_with_Layer-2_Data_Center_Interconnect_(DCI)), so if you need more details you'll find them there.

### Even More Details

On a more real-life front, [Ethan Banks did a great presentation describing real-life lessons learned while operating active/active data centers](http://nextgendc.ipspace.net/Public:5-High-Availability_Concerns#Guest_speaker) during the autumn 2016 session of [Building Next-Generation Data Center course](http://www.ipspace.net/Building_Next-Generation_Data_Center) (you get access to the recording as soon as you [register for the course](http://www.ipspace.net/Building_Next-Generation_Data_Center#register)).
