---
title: "CCIE Preparation with netlab"
date: 2024-07-18 06:12:00+0200
tags: [ netlab, certifications ]
netlab_tag: overview
---
Ben asked an [interesting question](https://blog.ipspace.net/2024/07/bgp-labs-year-later/#2329):

> Do you think, realistically in 2024, netlab would suffice to prepare the CCIE lab exam? Particulary for the SP flavor, since netlab supports a lot of routing protocols. Thanks!

**TL&DR:** No.

_[netlab](https://netlab.tools/)_ would be a great tool to streamline your CCIE preparation studies. You could:
<!--more-->
* Create optimized topologies that match what you're trying to master instead of cramming the challenges into an 8-router superlab (or whatever it is these days).
* Start labs with zero hassle (apart from having to make lunch while waiting for IOS XR to boot).
* Have someone else do all the tedious configuration (IP addressing, IGP setup, BGP sessions, VLANs, and VRFs).

That's exactly how I use _netlab_ in [BGP labs](https://bgplabs.net/). However:

* A great tool does not make an expert. An excellent set of [high-end power tools](https://www.felder-group.com/en-si/brand/felder) won't make me a master woodworker or allow me to create stuff [old masters made with hand tools](https://en.wikipedia.org/wiki/Antique_Woodworking_Tools). It's just faster and more convenient.
* _netlab_ does not cover the intricate features you'll probably need to know to pass the CCIE lab exam. We're focusing on providing the "_let someone else do the boring stuff_" functionality on a wide range of platforms, not on "_YAML nerd knobs to emulate vendor nerd knobs_."
* We have no plans to touch certain protocols in the CCIE SP blueprint, such as IP multicast, MPLS TE, VPLS, NAT, QoS, or fast reroute.

Finally, practicing for the CCIE lab exam is more than just typing commands. You need challenging scenarios to work on, and they are not trivial to create. That's why [Narbik](https://micronicstraining.com/) is still running CCIE preparation classes ;)

However, it would be great if someone would use _netlab_ to develop a training program, and if you happen to be doing something along those lines, please let me know.
