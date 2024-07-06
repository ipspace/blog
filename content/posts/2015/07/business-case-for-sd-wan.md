---
date: 2015-07-02 09:16:00+02:00
tags:
- SD-WAN
- SDN
- WAN
title: Business Case for SD-WAN
url: /2015/07/business-case-for-sd-wan.html
sd-wan_tag: bc
---
An anonymous commenter wrote this comment to my [initial SD-WAN post](/2015/06/software-defined-wanwell-orchestrated.html):

> I can still hardly imagine the business case behind SD-WAN. Any thoughts?

This question is really easy to answer. There's a huge business case that SD-WAN products are aiming to solve: replacing traditional MPLS/VPN networks with encrypted transport over public Internet. However...
<!--more-->
**Why would you want to do that?** Internet access is often orders of magnitude cheaper than traditional circuits. Replacing MPLS/VPN circuits with IPsec-over-Internet (or something similar) can drastically reduce your WAN costs. Trust me -- I've seen dozens of customers make the move and save money.

**Why is anyone still using WAN circuits?** **Where's the catch?** Contrary to some very vocal opinions, traditional WAN circuits still use lower oversubscription ratios and get close to the promised SLA most of the time. Some service providers offer business-class Internet services with guaranteed bandwidth and SLA, but these solutions tend to cost approximately as much as more traditional alternatives. Reserving bandwidth, providing support and fixing errors in real time costs money.

**Weren't we doing it a decade ago?** Glad you asked. Of course we did. When I was working for a system integrator we migrated most of our customers to hybrid WAN in early 2000s, and I've worked with multinationals that run hybrid WAN on a global scale (sometimes coupled with PBR to separate business-critical traffic from the nice-to-have one).

Companies that prefer spending money on WAN circuits instead of upgrading their infrastructure and investing in people who actually understand how to run it are obviously stuck in the past and a ripe target for an SD-WAN sales pitch.

**What's the big deal then?** If a smart group of engineers works on solving a problem for a decade, and then starts from scratch, they're bound to create a more elegant and more optimized solution.

If they think about orchestration and monitoring from the moment they start designing the system, their orchestration system (aka controller) tends to be orders of magnitude better than Java-based GUI slapped in front of the hard-to-automate CLI.

The emerging SD-WAN solutions thus tend to be way better than a hodgepodge of protocols that grew organically for over a decade (keep in mind that we used NHRP to build shortcuts across ATM subnets).

Last but definitely not least, do keep in mind that at the moment every SD-WAN vendor focuses on what they perceive to be the sweet spot. Once their products hit reality and the customer pressure to implement per-customer knobs, they'll slowly get as complex as the current solutions.

**Finally, why is everyone so ecstatic?** Because people always want to believe that it's possible to replace investment and hard work with magic. The same managers that believed Cisco's slide decks about the beauties of DMVPN (and got burned by the complexity of the real-life) now believe that it's possible to throw away all the old stuff and replace it with next-generation magic. I wish them luck.
