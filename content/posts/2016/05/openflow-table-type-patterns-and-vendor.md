---
date: 2016-05-26 12:26:00+02:00
tags:
- SDN
- OpenFlow
title: OpenFlow Table-Type-Patterns and Vendor Hype
url: /2016/05/openflow-table-type-patterns-and-vendor.html
---
Network Computing recently published an [article](http://www.networkcomputing.com/networking/network-disaggregation-opening-last-black-box/1394596654) with a promising title "*Network Disaggregation: Opening the Last Back Box*" and a subtitle I could totally relate to: "*switch ASICs must be opened up to provide real networking flexibility*."
<!--more-->
The article starts with excited black-box-busting cheerleading describing hardware disaggregation (first black box), centralized control plane (second black box -- I [disagree](https://blog.ipspace.net/2014/05/does-centralized-control-plane-make.html) but let's move on) and network operating system (third black box)... and finally identifies the final black box: switch ASICs, where it mysteriously fails to identify the real problem: [major ASIC vendors are hiding their documentation from public scrutiny](http://blog.ipspace.net/2016/05/what-are-problems-with-broadcom.html).

Well, the mystery is solved the moment you get to the end of the article -- it was written by head of product marketing for Pica8, whose whole product line uses one or another Broadcom ASIC, totally destroying the potential credibility of the article.

And what's the "solution" proposed by Pica8? OpenFlow [Table Type Patterns](https://github.com/OpenNetworkingFoundation/TTP_Repository/blob/master/TTP-FAQ.md) (TTPs), which are nothing more than templates specifying which forwarding features an OpenFlow switch should support. Now let's see what supposed superpowers these data models give a switch running on an undocumented ASIC:

> With TTP, network engineers and operators can now implement OpenFlow at greater scale -- in some cases, up to two million flows (a 1,000x increase from previous methodologies) -- while still using standard, white-box hardware.

![Deja-Moo](/2021/01/deja-moo.jpg)

An OpenFlow-based switch can do only whatever the underlying hardware can do and whatever the NOS vendor implemented in the OpenFlow agent. If Pica8 claims that their software works better with TTPs they're just saying that their previous software sucked.

> TTP does this by allowing the NOS to access all of the ASIC's memory tables  \--VLAN, MAC, and IP along with ternary content-addressable memory (TCAM) tables \-- to store flow forwarding information.

More of the same. Every network operating system could access whatever hardware capabilities of the ASIC... at least as long as the NOS developers had access to hardware documentation (see above) and were willing to read it. Or maybe the author is really trying to say that with [Broadcom's OF-DPA](https://www.broadcom.com/docs/support/OF-DPA-Specs_v2.pdf) you could finally get the most out of Broadcom hardware without having to read the documentation (or deal with hardware intricacies)?

> Prior to the advent of TTP, OpenFlow scalability was limited by the size of the TCAM, since only the TCAM could be used for storing flow forwarding information. 

Yet another misleading claim. As anyone watching my [OpenFlow Deep Dive](http://www.ipspace.net/OpenFlow_Deep_Dive) or [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinars knows smart networking vendors (including Arista, Cisco, Dell and HP) used TCAM as well as L2 and L3 forwarding tables to store OpenFlow flows for years.

Finally, the article concludes with:

> By opening up the ASIC, NOS products allow network engineers to choose any switch as the basis of a custom networking solution. 

Broadcom ASIC is as closed as it ever was, but at least now we have public APIs that could be used to program certain aspects of it (OF-DPA and [OpenNSL](http://packetpushers.net/hitchhikers-guide-to-everything-open-in-networking/)), and Intel ASIC is as open as it ever was (but that wouldn't interest the Pica8 marketing guys because they're not using Intel ASICs in their products).
