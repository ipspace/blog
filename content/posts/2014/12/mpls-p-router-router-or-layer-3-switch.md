---
date: 2014-12-02 06:31:00+01:00
tags:
- bridging
- MPLS
- switching
- IP routing
title: MPLS P-Router, Router or Layer-3 Switch?
url: /2014/12/mpls-p-router-router-or-layer-3-switch/
---
One of my readers is struggling with the [aftermath of marketing gimmicks](/2011/02/how-did-we-ever-get-into-this-switching/):

> We will implement a new network soon, and we\'re discussing P-routers versus regular routers versus switches. I\'m looking for arguments to go one way or the other.

TL&DR: [there's no difference between router and L3 switch](/2012/08/is-layer-3-switch-more-than-router/).
<!--more-->
The critical part is the functionality you need. Based on their intended use, some boxes tend to have low table sizes (you can't pump a full BGP table into a ToR L3 switch even though it runs BGP unless you're David Barroso -- more about that in an upcoming [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild) podcast), or limited QoS, or no shaping, or...

You should always start with "[*what services do I want to offer*](https://www.youtube.com/watch?v=ClKEkCRvWTQ)", continue with "[*how would I best implement them with the simplest possible design*](/2013/08/temper-your-macgyver-streak/)", go down the path of "*which functions do I need to make this design work*" and finally "*which boxes from which vendors fit my needs?*"

As for MPLS, do keep in mind that very few L3 switches support MPLS, and even those that do [tend to have a very limited number of MPLS labels](/2014/03/mpls-requires-custom-silicon-really/) (although QFX5100 does an excellent job squeezing 16K labels out of Trident-II chipset), which might or might not be a problem depending on what the outcome of the previous paragraph is.

### Need to Know More About MPLS?

Explore my [MPLS/VPN books](http://www.ipspace.net/Books#MPLS.2FVPN), and [Enterprise MPLS](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment) and [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials) webinars.