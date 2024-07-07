---
date: 2010-04-06 06:46:00.003000+02:00
tags:
- firewall
- PPP
- IP routing
- WAN
title: Small Steps to Large Complexity
url: /2010/04/small-steps-to-large-complexity/
---
Imagine you have a large retail network: your remote offices use ISDN to dial into the central site and upload/download whatever periodic reports they have. Having a core router connected to an ISDN PRI interface is the perfect solution:

{{<figure src="/2010/04/s400-L2TP_1.png">}}

A few years later, ISDN is becoming too slow for your increased traffic needs and you want to replace it with DSL or VPN-over-Internet solution. Your Service Provider offers you PPPoE forwarding with L2TP. This is a perfect solution as it allows you to minimize the changes:
<!--more-->
-   ISDN BRI is replaced with PPPoE in remote offices. No other configuration needs to be changed if you've already used dialer interfaces.
-   ISDN PRI is replaced with **vpdn-group** in your LNS. No other changes are needed if you've already used virtual templates.

Since the traffic from remote offices reaches the central site through its Internet link, it's prudent to implement IPSec encryption of sensitive traffic (although it's unlikely anyone would snoop the L2TP traffic between LAC and LNS).

{{<figure src="/2010/04/s400-L2TP_2.png">}}

There's almost no change in your connectivity requirements: instead of having an ISDN PRI and a LAN interface, the LNS router now has two IP-enabled interfaces: one toward the Internet and another one into your network core.

You could connect the LNS router to your firewall, but that would require major redesign of your firewall policies. It's simpler (but still relatively secure) to connect the outside LAN interface of the LNS router to the Internet and the inside LAN interface to the core network; a strict access list on the outside interface blocks all incoming traffic but the L2TP packets.

{{<figure src="/2010/04/s400-L2TP_3.png">}}

So far so good... but here's a catch: as you don't know the public IP addresses of the L2TP NAS (*LAC* in the above picture), the LNS router needs a default route pointing toward the Internet. It also needs a default route toward the core network; otherwise the traffic from remote offices to the Internet would not go through the firewall.

Assuming that you want to minimize the changes to your design, what would be your solution to this problem?
