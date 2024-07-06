---
date: 2012-02-14 07:31:00+01:00
tags:
- SDN
- OpenFlow
- QoS
title: 'Bandwidth-On-Demand: Is OpenFlow the Silver Bullet?'
url: /2012/02/bandwidth-on-demand-is-openflow-silver.html
---
Whenever the networking industry invents a new (somewhat radical) technology, bandwidth-on-demand seems to be one of the much-touted use cases. OpenFlow/SDN is no different -- Juniper used its OpenFlow implementation ([Open vSwitch sitting on top of Junos SDK](https://developer.juniper.net/content/dam/jdn/Programmable%20Networks/OpenFLow_APP_JDN_Overview.pdf)) to demonstrate *Bandwidth Calendaring* (see [Dave Ward's presentation @ OpenFlow Symposium](https://player.vimeo.com/video/31205041?title=0&byline=0&portrait=0) for more details), and Dmitri Kalintsev [recently blogged](http://telecomoccasionally.wordpress.com/2012/02/11/should-sdn-and-mpls-kiss-and-make-out/) "*How about an ability for things like Open vSwitch \... to actually signal the transport network its connectivity requirements \... say desired bandwidth*" I have only one problem with these ideas: I've seen them before.
<!--more-->
In the last 20 years, at least three technologies have been invented to solve the bandwidth-on-demand problem: RSVP, ATM Switched Virtual Circuits (SVC) and MPLS Traffic Engineering (MPLS-TE). None of them was ever widely used to create a ubiquitous bandwidth-on-demand service.

I'm positive very smart network operators (including major CDN and content providers like Google) use MPLS-TE very creatively. I'm also sure there are environments where RSVP is a mission-critical functionality. I'm just saying bandwidth-on-demand is like IP multicast -- [it's used by 1% of the networks that badly need it](http://www.fragmentationneeded.net/2011/12/pricing-and-trading-networks-down-is-up.html).

All three technologies I mentioned above faced the same set of problems:

-   [Per-flow (or per-granular-FEC) state in the network core never scales](/2011/10/openflow-and-state-explosion.html). This is what killed RSVP and ATM SVCs.
-   It's pretty hard to traffic engineer just the elephant flows. Either you do it properly and traffic engineer all traffic, or you end with a suboptimal network.
-   Reacting to short-term changes in bandwidth requirements can cause interesting oscillations in the network (I'm positive Petr Lapukhov could point you to a dozen sources analyzing this problem).
-   Nobody above the network layer really cares -- it's way simpler to blame the network when the [bandwidth fairy fails to deliver](http://en.wikipedia.org/wiki/Fallacies_of_Distributed_Computing).

You don't think the last bullet is real? Then tell me how many off-the-shelf applications have RSVP support \... even though RSVP has been available in Windows and Unix/Linux server for ages. How many applications can mark their packets properly? How many of them allow you to configure DSCP value to use (apart from IP phones)?

Similarly, it's not hard to implement bandwidth-on-demand for specific elephant flows (inter-DC backup, for example) with a pretty simple combination of MPLS-TE and PBR, potentially configured with Netconf (assuming you have a platform with a decent API). You could even do it with SNMP -- pre-instantiate the tunnels and PBR rules and enable tunnel interface by changing *ifAdminStatus*. When have you last seen it done?

{{<figure src="/2012/02/s400-HolyGrail.jpg" caption="Looking for the Holy Grail?">}}

So, although I'm the first one to admit OpenFlow is an elegant tool to integrate flow classification (previously done with PBR) with traffic engineering (using MPLS-TE or any of the novel technologies proposed by Juniper) using the [hybrid deployment model](/2011/11/openflow-deployment-models.html), being a seasoned skeptic, I just don't believe we'll reach the holy grail of bandwidth-on-demand during this hype cycle. However, being an eternal optimist, I sincerely hope I'm wrong.

#### Need help?

If you need technology-focused consulting, evaluation of emerging technologies, second opinion, or a review of your network, check out the [ExpertExpress service](http://www.ipspace.net/ExpertExpress).

To find more about OpenFlow, watch our [OpenFlow Deep Dive](https://www.ipspace.net/OpenFlow_Deep_Dive) webinar; you might also be interested in *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.