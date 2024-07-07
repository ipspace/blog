---
date: 2017-12-18 09:33:00+01:00
dcbgp_tag: abstract
series:
- dcbgp
tags:
- Internet
- BGP
title: 'BGP: the Tragedy of the Commons'
url: /2017/12/bgp-tragedy-of-commons/
---
Every now and then someone looks at a few recent BGP incidents (from fat fingers to more dubious ones) and says "[we need a better BGP](https://networkingnerd.net/2017/12/15/should-we-build-a-better-bgp/)".

It's like being unable to cope with your kids or your team members because you don't have the guts to tell them NO and trying to solve the problem by implementing new procedures and rules.

Like anything designed on a few napkins BGP has its limit. They're well known, and most of them have to do with trusting your neighbors instead of checking what they tell you.
<!--more-->
The solutions to the problem are [pretty simple](https://www.manrs.org/manrs/) and have been known for decades ([BCP38](https://tools.ietf.org/html/bcp38) was published in May 2000). In a nutshell you have to:

-   Build a global repository of who owns what address space;
-   Document who connects to whom and what their peering policies are;
-   Filter the updates received from your customers and peers based on the information from those repositories;
-   Filter the traffic from addresses that are obviously spoofed.

We have most of the tools we need to get the job done; you'll find them described in [Best Current Practice (BCP) 194](https://tools.ietf.org/html/rfc7454). It's also not impossible to get the job done from the operational perspective. NTT has been doing it for quite a while; [Job Snijders](https://twitter.com/JobSnijders) described their approach to [practical BGP filtering](https://www.youtube.com/watch?v=CSLpWBrHy10&feature=youtu.be) in a NANOG67 presentation.

Unfortunately you'll always find ISPs (including some so-called Tier-1 providers) who couldn't care less about fixing things and making global Internet a better place, because implementing those rules might impact their sloppy customers, and it's always easier to give in to your customer's (or your kid's) screaming instead of telling them "you can't have the candy because you haven't followed the rules"

The "only" problem of getting things done is that like in any dysfunctional family the kids (= customers) could go shopping around for someone more permissive, and they'll always find another ISP with lower prices, more relaxed rules, and connectivity to a dysfunctional transit provider.

Even worse than individual sloppy ISPs -- there are Internet Exchange Points running route servers with no filters. Job Snijders got so sick-and-tired of them that he added a public column-of-shame to his [IXP overview spreadsheet](http://peering.exposed/). Not that it would help much; Geoff Huston has been producing [deaggregation](https://www.cidr-report.org/as2.0/) and [excessive BGP updates](http://bgpupdates.potaroo.net/instability/bgpupd.html) reports for years with absolutely no visible effect.

Being good engineers who hate confrontations, we're trying to sneak our way around those problems with various cryptographic tools (like RPKI) instead of fixing the source of the problem: chaotic (or non-existent) operational practices of some major players.

Unfortunately, you can never solve people- or process problems with new technology, you can just make them more convoluted and harder to troubleshoot. What we'd really need to have are driving licenses for ISPs, and some of them should be banned for good due to repetitive drunk driving. Alas, I don't see that happening in my lifetime.

For more details, watch the [Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC) part of the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar, and the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar.
