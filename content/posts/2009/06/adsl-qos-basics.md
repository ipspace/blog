---
date: 2009-06-30 07:25:00.005000+02:00
tags:
- WAN
- ADSL
title: ADSL QoS Basics
url: /2009/06/adsl-qos-basics.html
lastmod: 2020-12-07 17:17:00
---
Based on the [ADSL reference model](https://blog.ipspace.net/2009/06/adsl-reference-diagram.html), let's try to figure out how you can influence the quality of service over your ADSL link (for example, you'd like to prioritize VoIP packets over web download). To understand the QoS issues, we need to analyze the congestion points; these are the points where a queue might form when the network is overloaded and where you can reorder the packets to give some applications a preferential treatment.

**Remember**: QoS is always a zero-sum game. If you prioritize some applications, you're automatically penalizing all others.
<!--more-->
The primary congestion point in the downstream path is the PPPoE virtual interface on the NAS router (marked with a red arrow in the diagram below), where the Service Provider usually performs traffic policing. It's better from the SP perspective to police the traffic @ NAS than to send all the traffic to DSLAM where it would be dropped in the ATM hardware. Secondary congestion points might arise in the backhaul network (if the network is heavily oversubscribed) and in DSLAM (if the NAS policing does not match the QoS parameters of the ATM virtual circuit).

{{<figure src="ADSL_Downstream_Congestion.png" caption="xDSL downstream congestion">}}

In the upstream direction, the congestion occurs on the DSL modem -- the path between the CPE and the modem (Ethernet or Fast Ethernet) is much faster than the upstream ATM virtual circuit. Secondary congestions might occur in DSLAM or the backhaul network. NAS usually does not police inbound traffic, as it's assumed the DSL access network already limits the user traffic to its contractual upstream speed.

{{<figure src="ADSL_Upstream_Congestion.png" caption="xDSL upstream congestion">}}

Based on the congestion analysis, it's obvious [you cannot use queuing](/kb/tag/QoS/Queuing_Principles.html) on the CPE (marked "2" in the diagrams) to influence the ADSL QoS as you don't control the single congestion point. You have to use [traffic shaping](/kb/tag/QoS/Traffic_Shaping.html) on the CPE to introduce artificial congestion points in which the queues will form. You can then use the usual queuing mechanisms to prioritize the application traffic.

{{<figure src="ADSL_CPE_QoS.png" caption="Traffic shaping configured on xDSL CPE">}}

The shaping configured on the PPPoE interface on the CPE router neatly removes the congestion on the DSL modem. The backhaul network is rarely congested in the upstream direction (unless your [friendly neighbors are devoted fans of P2P protocols](https://blog.ipspace.net/2009/06/internet-socialism-all-i-can-eat.html)).

When configuring the upstream shaping rate, take in account the extra overhead introduced by the PPPoE framing, which is not yet present in packets shaped on the **Dialer** interface, and reduce the upstream shaping speed to a value slightly below your DSL upstream speed.

{{<note info>}}Depending on the Cisco IOS version you're using you might have to apply the traffic shaping on **dialer** interface or on the underlying Ethernet interface. See comments for more details.{{</note>}}

Assuming most of your traffic is TCP-based (or that all non-TCP traffic is prioritized), the shaping on the inside LAN interface will cause enough TCP delays to slow down the downstream TCP transmission. However, it's harder to determine the correct shaping rate and optimize the shaping behavior when the high-priority traffic is not present; we'll cover these issues in an upcoming post.

<!-- diagrams in Articles and Blog Diagrams (2020) -->