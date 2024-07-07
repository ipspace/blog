---
date: 2010-10-21 08:19:00.002000+02:00
dmvpn_tag: routing
eigrp_tag: deploy
tags:
- DMVPN
- EIGRP
title: EIGRP Summarization in DMVPN Phase 2 Networks
url: /2010/10/eigrp-summarization-in-dmvpn-phase-2/
---
Imagine the following scenario: you've configured a Phase 2 DMVPN network with a hub and a few spokes. DMVPN is configured properly, IPSec and NHRP are working, you can ping all around the DMVPN cloud.

Next step: configuring EIGRP. You know you have to disable EIGRP split horizon and EIGRP next-hop processing. You even remember to configure interface bandwidth.

Someone told you to minimize the EIGRP routing traffic, so you use EIGRP stub routers on the spokes and route summarization on the hub router. The final EIGRP configuration is shown in the following diagram:
<!--more-->
{{<figure src="/2010/10/s1600-eigrpsum.png">}}

**Note**: Your network is using 10.0.0.0/8 addresses for LAN links and loopbacks and 192.168.0.0/16 for WAN links.

Would your Phase 2 DMVPN network perform as expected? If not, what's wrong with it? If you think it has a problem, what would you change?

Don't cheat, answer the questions before [reading the solution](/2010/10/solution-eigrp-summarization-breaks/).
