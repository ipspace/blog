---
date: 2010-11-05 08:46:00+01:00
tags:
- VPN
- MPLS VPN
- QoS
title: Solving the MPLS/VPN QoS Challenge
url: /2010/11/solving-mplsvpn-qos-challenge.html
---
Two weeks ago I [wrote about the challenges](/2010/10/qos-over-mplsvpn-networks.html) you'll encounter when trying to implement end-to-end QoS in an enterprise network that uses MPLS/VPN service as one of its transport components. Most of the issues you'll encounter are caused by the position of the user-SP demarcation point. The Service Providers smartly "assume" the demarcation point is the PE-router interface... and everything up to that point (including their access network) is your problem.

{{<figure src="/2010/11/s1600-mplsqos_before.png" caption="Typical MPLS/VPN demarcation point">}}
<!--more-->
The only workable solution to the QoS-across-MPLS/VPN problem I found (and believe me, every time I meet a customer using MPLS/VPN, the issue pops up) is to move the demarcation point. Instead of trying to deal with the hidden complexities of unknown access networks, ask the Service Provider to install their CE-routers at your premises, like they did in the old days when they were trying to sell Frame Relay as *Managed Network* service.

{{<figure src="/2010/11/s1600-mplsqos_after.png" caption="Onsite demarcation point">}}

The only task left to you is to shape your outbound traffic to the contractual rate (and [queue within the shaping queue](/kb/tag/QoS/Traffic_Shaping.html) if necessary) and the rest is now purely the Service Provider's responsibility. Make sure you have enforceable SLA violation penalties in your contract, deploy SLA-measurement tools, show your SP account manager the graphs (just to let them know you might have supporting documentation to enforce the penalties) \... and watch the QoS miraculously work as expected (OK, it helps if you're big enough and if they know what they're doing).

### More information

If you'd like to get an overview of numerous VPN services, their benefits, drawbacks, and challenges you might encounter deploying them, check out the [*Choose the Optimal VPN Service*](http://www.ipspace.net/Choose_the_optimal_VPN_service) webinar.

{{<note>}}This brilliantly simple solution was mentioned to me by one of my customers. For obvious reasons I have to keep quiet, but you know who you are.{{</note>}}
