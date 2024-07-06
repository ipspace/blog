---
date: 2010-12-21 09:40:00.002000+01:00
mlag_tag: overview
series:
- mlag
tags:
- link aggregation
- load balancing
title: MLAG and Load Balancing
url: /2010/12/mlag-and-load-balancing.html
---
FullMesh added an excellent comment to my [Multi-Chassis Link Aggregation (MLAG) and hot potato switching](/2010/12/multi-chassis-link-aggregation-mlag-and.html) post. He wrote:

> If there are two core routing switches and two access switches which are MLAGged together in both directions, and hosts that are dual-active LAGged to the pair of access switches, then the traffic would stay on whichever side the host places it.

He also opened another can of worms: load balancing in MLAG environment is dictated by the end hosts. It doesn't pay to have fancy switches that support L3 or L4 load balancing; a stupid host implementing destination-MAC-address-based load balancing can easily ruin your day.
<!--more-->
Let's start with simple baseline architecture: two web servers and a router connected to a switch. Majority of the traffic flows from the web servers through the router to outside users.

{{<figure src="/2010/12/s320-MLAG_LB_Baseline.png">}}

In this architecture, the switch can reshuffle the packets based on its load balancing algorithm regardless of the load balancing algorithm used by the servers. Even if the servers use source-destination-MAC algorithm (which would send all the traffic over a single link), the switch can spread packets sent to different destination IP addresses[^5TUPLE] over both links toward the router. As long as the links between the servers and the switch aren't congested, we don't really care about the quality of the load balancing algorithm the servers use.

[^5TUPLE]: Or even packets from different TCP/UDP sessions sent to the same destination if you configured 5-tuple load balancing.

Now let's make the architecture redundant, introducing a second switch and combining the two switches into a [multi-chassis link aggregation group](/series/mlag.html):

{{<figure src="/2010/12/s400-MLAG_LB.png" caption="Redundant architecture using an MLAG cluster">}}

All of a sudden, the switches (using [hot potato switching](/2010/12/multi-chassis-link-aggregation-mlag-and.html)) can no longer influence the traffic flow toward the router. If all the hosts decide to send their outgoing traffic toward S1, the link S1-R will be saturated even though the link S2-R will remain idle. The quality of the servers' load balancing algorithm becomes vital.

Finally, let's add two more links between the switches and the router:

{{<figure src="/2010/12/s400-MLAG_LB_Double.png" caption="More is not always better">}}

In this architecture, each switch can use its own load balancing algorithm on the directly connected links: if all the hosts decide to send outbound traffic to S1, S1 can still load-balance the traffic according to its own rules on the parallel links between S1 and R. Of course it still cannot shift any of the traffic toward S2.

#### More information

-   Multi-chassis Link Aggregation (and numerous other LAN, SAN and virtualization technologies) is described in the [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30) webinar ([buy a recording](https://www.ipspace.net/SingleRecording?code=DC30) or [yearly subscription](https://www.ipspace.net/Subscription)).
-   Read my posts about [Multi-chassis Link Aggregation basics](/2010/10/multi-chassis-link-aggregation-basics.html), [Stacking on Steroids](/2010/10/multi-chassis-link-aggregation-stacking.html) and [External Brains](/2010/11/multi-chassis-link-aggregation-mlag.html) architectures.
-   The load balancing issues described in this article are caused by the [hot potato switching](/2010/12/multi-chassis-link-aggregation-mlag-and.html).
