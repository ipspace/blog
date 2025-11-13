---
title: "Building VXLAN/EVPN Data Center Lab with netlab"
date: 2025-11-20 07:56:00+0100
tags: [ worth reading, netlab ]
netlab_tag: use
---
[Dmitry Klepcha](https://www.linkedin.com/in/dmitri-klepcha-8b97491b8/) published an excellent document describing how you can use netlab to build a series of data center fabric labs, starting from a simple IP network (without routing) and finishing with a complex EVPN/VXLAN network using symmetric IRB and MLAG toward hosts.

But wait, there's more: all the lab topologies he used in his exercises are [available on GitHub](https://github.com/aeangel/otus-DC-net/tree/main), which means that you could just clone the repo and start using them (I also "borrowed" some of [his ideas](https://aeangel.gitbook.io/netlab_for_otus/en-docs/useful/09_customizing) as future _netlab_ improvements).

Finally, thanks a million to [Roman Pomazanov](https://www.linkedin.com/in/roman-pomazanov/) for bringing Dmitry's work to my attention (and for the quote at the end of [his post](https://www.linkedin.com/posts/roman-pomazanov_theres-a-saying-that-goes-those-who-know-activity-7394645032164827136-ELmR/) ;).
