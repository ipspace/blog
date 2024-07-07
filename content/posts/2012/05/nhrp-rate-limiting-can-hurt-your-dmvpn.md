---
date: 2012-05-09 08:06:00+02:00
dmvpn_tag: quirk
tags:
- DMVPN
title: NHRP Rate Limiting Can Hurt Your DMVPN Network
url: /2012/05/nhrp-rate-limiting-can-hurt-your-dmvpn/
---
[NHRP-based interface state control](http://www.cisco.com/en/US/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-2mt/sec-conn-dmvpn-tun-mon.html#GUID-E968E183-0022-4E8C-89A6-69AE3AE2AFF9) is a fantastic feature that you can use for faster convergence of very large DMVPN networks (as explained in the [DMVPN Designs](http://www.ipspace.net/DMVPN_Designs) webinar, you can also use it to solve some interesting backup scenarios). We tested it in a network with over 1000 spokes (using ASR1K as the hub router) using very short registration timeouts, and the CPU utilization of the NHRP process rarely exceeded a few percents.
<!--more-->
However, the engineer doing the tests forgot to tell me a crucial bit of the puzzle -- he had to tweak the NHRP rate limiting (configured with **ip nhrp max-send** command). This omission was gracefully pointed out by George Mihalachioaie who stumbled across the same problem during his DMVPN deployment.

**Summary:** Having short registration timeouts in large NHRP networks is not a problem per-se (and NHRP-based interface state control may significantly simplify your design), but you have to know what you're doing, and change the defaults. The [usage guidelines provided with the **ip nhrp max-send** command](http://www.cisco.com/en/US/docs/ios/ipaddr/command/reference/iad_nhrp.html#wp1011514) should give you more than enough information, and don't forget that NHRP replies (not just requests) also count as NHRP packets.
