---
date: 2023-01-31 07:50:00+00:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- design
title: 'Design Clinic: Small-Site IPv6 Multihoming'
---
I decided to stop caring about IPv6 when the protocol became old enough to buy its own beer (now even in US), but its [second-system effects](https://en.wikipedia.org/wiki/Second-system_effect) keep coming back to haunt us. Here's a question I got for the [February 2023 ipSpace.net Design Clinic](https://designclinic.ipspace.net/):

> How can we do IPv6 networking in a small/medium enterprise if we’re using multiple ISPs and don’t have our own IPv6 Provider Independent IPv6 allocation. I’ve brainstormed this with people far more knowledgeable than me on IPv6, and listened to IPv6 Buzz episodes discussing it, but I still can’t figure it out.
<!--more-->
I [wrote about this particular elephant-in-the-room](/2010/12/small-site-multihoming-in-ipv6-mission/) in 2010 (a dozen years ago), and [concluded NPT66 might be the only viable option](/2011/12/we-just-might-need-nat66/) in 2011.

In the meantime, a number of RFCs modified [host source address selection rules](https://www.rfc-editor.org/rfc/rfc6724.html), [first-hop router selection](https://www.rfc-editor.org/rfc/rfc8028.html#section-3) and [other aspects of IPv6 prefix advertisements](https://www.rfc-editor.org/rfc/rfc9096). Either those fixes weren't good enough or weren't implemented --  questions along the same lines keep popping up on v6ops mailing list and every time the sad conclusion is "_we're not there yet_". There's also exceedingly-complex [Enterprise Multihoming Using Provider-Assigned IPv6 Addresses](https://www.rfc-editor.org/rfc/rfc8678.html) stating in its abstract:

> Connecting an enterprise site to multiple ISPs over IPv6 using provider-assigned addresses is difficult without the use of some form of Network Address Translation (NAT). Much has been written on this topic over the last 10 to 15 years, but it still remains a problem without a clearly defined or widely implemented solution.

[Nick Buraglio](https://www.ipspace.net/Expert:Nick_Buraglio)[^NB], the author of [IPv6 ULA Made Useless](/2022/05/ipv6-ula-made-useless/) draft, agreed to join us in the live [Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic) session on February 2nd, and we'll try to figure out how one could do small site IPv6 multihoming in real-life scenarios. Have an IPv6 grudge? Join us!

[^NB]: Who's still trying to get IPv6 working in environments other than mobile networks or WiFi hotspots -- the only scenarios [some vendors seem to care about](/2021/10/dhcpv6-matters/).