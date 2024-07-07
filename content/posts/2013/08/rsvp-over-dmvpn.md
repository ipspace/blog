---
date: 2013-08-17 17:55:00+02:00
dmvpn_tag: integrate
tags:
- DMVPN
- QoS
title: RSVP over DMVPN
url: /2013/08/rsvp-over-dmvpn/
---
A while ago [Tomasz Kacprzynski](http://kemot-net.com/about) asked me whether I'd ever run RSVP over DMVPN. I hadn't - after all, you'd only need that in VoIP environments and I try to stay as far away from voice as possible.

In the meantime, Tomasz solved the problem (short summary: you have to turn Phase 3 DMVPN into Phase 2 DMVPN) and wrote a [lengthy blog post describing the problem (RSVP split horizon rule) and his solution](http://kemot-net.com/blog/making-rsvp-work-over-dvmpn) (including numerous debugging printouts). Definitely worth reading if there's a non-zero chance you'll have to get the two working together.

{{<jump>}}[Keep reading](http://kemot-net.com/blog/making-rsvp-work-over-dvmpn){{</jump>}}