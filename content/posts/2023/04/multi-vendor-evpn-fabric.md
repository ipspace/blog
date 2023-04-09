---
title: "Multi-Vendor EVPN Fabrics"
date: 2023-04-20 06:11:00
tags: [ EVPN ]
---
Daniel left an interesting comment on my _[Studying EVPN to Prepare for a Job Interview](https://blog.ipspace.net/2023/03/evpn-job-interview.html)_ blog post:

> I also never build a VXLAN fabric with two vendors. So, is it possible now to build one large fabric consisting of multiple vendors?

TL&DR: Yes, but just because you could doesn't mean that you should.
<!--more-->
EVPN is a complex technology full of optional nerd knobs, and early implementations quickly turned it into _SIP of Networking_[^SN]. Fortunately (for the rest of us), EVPN vendors quickly came to their senses and started participating in EVPN interoperability testing, usually done during the MPLS & SDN World Congress ([2022 test report](https://eantc.de/fileadmin/eantc/downloads/events/2022/EANTC-InteropTest2022-TestReport.pdf)).

However, just because boxes from different vendors work together doesn't mean we're in a carefree plug-and-play world[^PP]. If you're forced to build a multi-vendor EVPN fabric it makes sense to stay as far away as possible from the vendor shenanigans ([like IBGP EVPN over EBGP underlay](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics)) and simplify your design:

* **Use a single vendor for a layer** (leaf or spine). You might claim that's cheating as all the hard work is done on the leafs, and the spines serve only as route reflectors (or not even that). It is possible to have mixed-vendor leafs, but it will make your life more interesting.
* **Use IBGP for EVPN address family**. Most EVPN implementations use BGP AS number as part of the EVPN route target and while it's [possible to make multi-AS EVPN work](https://www.ipspace.net/Data_Center_BGP/EVPN_Route_Target_Considerations) it's a needless hassle.
* **Use an IGP for the underlay routing**. You're not a hyperscaler[^HS] and [don't need EBGP to scale your underlay routing](https://blog.ipspace.net/2020/02/the-evpnbgp-saga-continues.html). It doesn't matter whether you use OSPF or IS-IS (most vendors have decent implementations of both), but you might want to stick with OSPF to be extra safe[^EI].
* **Stay away from complex stuff** like EVPN multihoming. It's safer to use [traditional MLAG with anycast VTEP](https://blog.ipspace.net/2022/09/mlag-deep-dive-vxlan-fabric.html).
* **Multicast BUM replication** is not supported by all vendors. Stay with EVPN-driven ingress replication.
* **Use symmetric integrated routing and bridging**. It's supported by most vendors these days, although you might encounter a few anycast gateway quirks.

In the ideal world I wouldn't have to write what comes next, but some people love to live dangerously and push the envelope, so here we go.

Don't even think about:

* **Complex nerd knobs** unless you need eternal job security.
* **Using stuff that is not explicitly supported**. Don't try to be overly smart. Your coworkers, your users, and vendor TAC engineers will appreciate that.
* **VXLAN-to-VXLAN bridging**. [Multiple vendors can do it](https://blog.ipspace.net/2022/06/vxlan-bridging-dci.html), but you probably don't want to be the one to figure out how to make them work together[^FTW].
* **Multivendor MLAG clusters**. MLAG is more than just a few hacks in the EVPN route types; not all of its [mandatory components](https://blog.ipspace.net/2022/06/mlag-deep-dive-overview.html) are standardized.

For more details, watch the excellent *[Multivendor Data Center EVPN](https://my.ipspace.net/bin/list?id=EVPN#MULTIVENDOR)* presentation by [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt).

[^SN]: If you ever had to use DTMF tone generator because your VoIP gateway and the public VoIP exchange to which it was connected couldn't agree on how to do [DTMF signaling](https://www.voip-info.org/sip-dtmf-signalling/) you know what I'm talking about.

[^HS]: And if you are, I hope you're reading my blog for the snark, not to get fabric design advice.

[^PP]: We might have reached the plug-and-pray phase though.

[^EI]: Hint: EIGRP is a wrong answer. So is RIP, but for other reasons.

[^FTW]: Once I asked a TAC engineer whether it's OK to run ~20 EIGRP processes on a single router and he replied: "_sure, just keep in mind you'd be the only one in the world doing it_." FWIW, that design was in production for over a decade before we managed to replace it with MPLS/VPN.