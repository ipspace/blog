---
title: "Worth Reading: Lab as Code (containerlab and netlab)"
series_title: "Lab as Code (containerlab and netlab)"
date: 2026-04-28 08:26:00+0200
tags: [ netlab, worth reading ]
netlab_tag: overview
---
[@sjhloco](https://github.com/sjhloco) wrote an excellent in-depth description of how you can [use containerlab and netlab to manage your labs as code](https://theworldsgonemad.net/2025/lab-as-code-pt2/).

He also documented a few _netlab_ shortcomings (one of which caused a crash); fortunately, I found his blog post (admittedly over a year later) and fixed most of them in [release 26.04](/2026/04/netlab-26-04/):
<!--more-->
* The new **[bgp.advertise](https://netlab.tools/module/bgp/#using-bgp-advertise-link-attribute)** attribute is exactly what he asked for. It's a [list of prefixes to advertise](https://netlab.tools/module/bgp/#advertised-bgp-prefixes) into BGP, and implemented as **network** statements (Cisco IOS, Arista EOS, FRR...) or as prefix lists for BGP **export** policies (Junos, SR Linux, SR OS).
* Once I had the **bgp.advertise** attribute, the next logical step was, "*Gee, I could use that with static discard routes to reimplement **[bgp.originate](https://netlab.tools/module/bgp/#using-bgp-originate-node-attribute)***!" (an old attribute added to _netlab_ before it became dual-stack-aware, and years before it got static routes). Having realized that, it was only a short process to get dual-stack **bgp.originate** working in global- and VRF BGP instances *on platforms where we know how to configure static discard routes*. Now you know why so many platforms got [static routing support](https://netlab.tools/module/routing/#id17) in release 26.04 ;)
* The node **bgp.as** versus global **vrf.as** confusion was exactly that, and I [updated the documentation](https://netlab.tools/module/vrf/#default-rd-rt-values) to make it (hopefully) a bit more obvious.
* I did forget node **router_id** attribute, and fixed that omission.
* The **bgp.policy** plugin borked the **module** node attribute for hosts. The workaround (if you knew the code) would have been to set **module** node attribute to `[]`, but of course, such a FUBAR [deserves to be fixed](https://github.com/ipspace/netlab/issues/3212).

It's great to see someone diving so deep into _netlab_ and documenting its shortcomings. If only there were a mechanism to report them, rather than my random stumbling upon the blog post. Oh, [wait](https://github.com/ipspace/netlab/issues) ;)

On a more serious note, even dropping me a message with a pointer to that wonderful blog post would be enough to get me started.