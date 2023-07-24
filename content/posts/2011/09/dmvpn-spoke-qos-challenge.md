---
date: 2011-09-29 07:14:00+02:00
dmvpn_tag: integrate
tags:
- DMVPN
title: 'DMVPN: Spoke QoS Challenge'
url: /2011/09/dmvpn-spoke-qos-challenge.html
---
Got the following question with an invalid return address, so I'm broadcasting the reply ;)

> I am running a DMVPN network and recently got a requirement for spoke-to-spoke communication. We currently shape traffic on a per spoke basis on the hub, and have a single shaper at the remote site. However, if a spoke is receiving a large amount of traffic from the hub and another spoke site, how will the sites sending traffic know that the remote port is congested?

Short answer -- they won't. You have a mission-impossible problem (very similar to [ADSL QoS](https://blog.ipspace.net/2009/06/adsl-qos-basics.html)), but there might be some slight silver lining:
<!--more-->
-   TCP traffic adapts to congestion. If most of your traffic is TCP, you'll do fine. If you have voice in the mix, you have a real problem. Even though TCP will eventually back off, congestion on the Internet-to-site link causes increased latency making VoIP users unhappy.
-   To keep voice latency within reasonable bounds, you have to shape TCP traffic to approximately two thirds of your access bandwidth. Jared Valentine wrote a great article describing his [adaptive ADSL QoS solution](http://www.xmission.com/~hidden/aatqos/). You could do something similar on your DMVPN spoke routers.
-   You can always use appliances like [PacketShaper](http://www.bluecoat.com/products/packetshaper)/Packeteer or [Ipanema](http://www.ipanematech.com/) -- but make sure you understand what they do and don't buy the snake oil. If your problem involves a combination of inbound traffic streams from multiple sites, you need on-site appliance, not something like emulated [tele\|engine](http://www.ipanematech.com/en/tele-engine).
-   Worst case, buy two Internet access links for each spoke -- one for data, one for voice. At \$50/month, this solution just might be cheaper than an on-site appliance.

### More Information

* I wrote about DMVPN QoS before. Read [QoS in Large-Scale DMVPN Networks](https://blog.ipspace.net/2011/06/qos-in-large-scale-dmvpn-networks.html).
* DMVPN QoS issues are similar to those faced by DSL users. Read [ADSL QoS Basics](https://blog.ipspace.net/2009/06/adsl-qos-basics.html).
* You can implement adaptive QoS with EEM, but it [won't be reacting to fast changes](https://blog.ipspace.net/2008/12/this-is-qos-who-cares-about-real-time.html) in line utilization ([here's an update](https://blog.ipspace.net/2010/01/update-workaround-for-sluggish-cb-qos.html)).

DMVPN QoS is also described in the [DMVPN New Features](https://www.ipspace.net/DMVPN150) webinar. You get it as part of the [yearly subscription](https://www.ipspace.net/Subscription).
