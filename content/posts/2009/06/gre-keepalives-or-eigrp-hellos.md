---
date: 2009-06-12 06:59:00+02:00
eigrp_tag: deploy
tags:
- EIGRP
- IPsec
- GRE
title: GRE Keepalives or EIGRP Hellos?
url: /2009/06/gre-keepalives-or-eigrp-hellos.html
---
It looks like everyone who's not using DMVPN is running IPSec over GRE these days, resulting in interesting questions like »should IP use EIGRP hellos or [GRE keepalives](/2007/10/gre-tunnel-keepalives.html) to detect path loss?«

Any dedicated link/path loss detection protocol should be preferred over tweaking routing protocol timers (at least in theory), so the [politically correct](http://en.wikipedia.org/wiki/Political_correctness) answer is »use GRE keepalives and keep EIGRP hellos at their default values«. Even better, use BFD over GRE (if your device supports it) instead of a hodgepodge of point technologies.
<!--more-->
Back to EIGRP-or-GRE: although EIGRP hellos and GRE keepalives use small packets that are negligible compared to today's link bandwidths, enabling GRE keepalives introduces yet another overhead activity. On the other hand, the GRE keepalive overhead is local to the router on which you've configured them (the remote end performs simple packet switching), whereas both ends of the tunnel are burdened with frequent EIGRP hello packets.

If you need to detect the path loss on the remote sites (to trigger the backup link, for example), GRE keepalives are the perfect solution. EIGRP timers are left unchanged and the overhead on the central site is minimal.

If your routing design requires the central site to detect link loss, there's not much difference between the two methods. However, due to the intricacies of the EIGRP hello protocol, improving neighbor loss on the central site requires hello timer tweaking on the remote sites. It's probably easier to configure GRE keepalives on the central site routers than to reconfigure all remote sites.

Last but not least, do not forget that GRE keepalives do [not work under all circumstances](http://www.cisco.com/en/US/tech/tk827/tk369/technologies_tech_note09186a008048cffc.shtml).
