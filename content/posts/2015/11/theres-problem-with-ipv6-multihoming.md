---
date: 2015-11-05 13:26:00+01:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
title: There’s a Problem with IPv6 Multihoming
url: /2015/11/theres-problem-with-ipv6-multihoming/
---
In an amazing turn of events, at least one IETF working group recognized we have serious problems with IPv6 multihoming. According to the [email Fred Baker sent to a number of relevant IETF working groups](https://www.ietf.org/mail-archive/web/v6ops/current/msg23256.html):

> PI multihoming demonstrably works, but PA multihoming when the upstreams implement BCP 38 filtering requires the deployment of some form of egress routing - source/destination routing in which the traffic using a stated PA source prefix and directed to a remote destination is routed to the provider that allocated the prefix. The IETF currently has no such recommendation, or consensus that it should have.

Here are a few really old blog posts just in case you don't know what I'm talking about (and make sure you read the comments as well):
<!--more-->
-   [Lack of IPv6 multihoming -- the elephant in the room](/2009/05/lack-of-ipv6-multihoming-elephant-in/) (May 2009)
-   [Small-Site Multihoming in IPv6 -- Mission Impossible](/2010/12/small-site-multihoming-in-ipv6-mission/) (December 2010)
-   [IPv6 Multihoming without NAT -- The Problem](/2011/12/ipv6-multihoming-without-nat-problem/) (December 2011)
-   [We just might need NAT66](/2011/12/we-just-might-need-nat66/) (December 2011)
-   [IPv6 Legends and Myths -- more opinions than data points](/2012/04/ipv6-legends-and-myths-more-opinions/) (April 2012)

After that I mostly gave up and focused on more interesting topics.

Obviously this is very old news, and it's utterly sad to see a well-known real-life problem being ignored for years while at the same time whole working groups work on hypothetical problems like "how do I create a plug-and-play routed network with a chain of routers that can support thousands of segments in my home" (aka Homenet working group). The only explanations I could come up with are:

-   The problem is hard to solve and definitely not sexy, so nobody is interested in working on it;
-   IPv6-focused engineers working within IETF that have actual operational experience have solved their problems (large-scale enterprise networks, web properties or zillions of residential customers), and are not interested in the target audience (SMB), and people who do work in that segment don't have time to waste arguing their case in the IETF ivory tower -- see also [Mid-Market Innovator's Dilemma](https://telecomoccasionally.wordpress.com/2012/02/20/mid-market-innovators-dilemma/).

In short, I don\'t expect anything to change any time soon, and we\'ll probably remain stuck with NAT66 for decades.

{{<note>}}In case you find this blog post way too sarcastic, subscribe to a few IPv6 mailing lists and wait till someone restarts a "*do we need ULA*", "*shall we give /48 to every residential customer*" or "*do we need default gateway in DHCPv6*" debate (not to mention the fascinating discussions of whether SLAAC on non-64 prefixes should work or not).{{</note>}}
