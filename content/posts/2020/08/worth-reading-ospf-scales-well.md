---
date: 2020-08-24 06:48:00+00:00
ospf_tag: read
series_title: What I've Learned About Scaling OSPF in Data Centers
tags:
- OSPF
- design
- worth reading
title: "MUST READ: What I've learned about scaling OSPF in Datacenters"
---
Justin Pietsch published a fantastic 
[recap of his experience running OSPF in AWS infrastructure](https://elegantnetwork.github.io/posts/What-Ive-learned-about-OSPF/). You MUST read what he wrote, here's the TL&DR summary:

* Contrary to popular myths, OSPF works well on very large leaf-and-spine networks.
* [OSPF nuances are really hard to grasp intuitively](/2018/04/is-ospf-unpredictable-or-just-unexpected.html), and the only way to know what will happen is to run tests with the same codebase you plan to use in a production environment.

Dinesh Dutt made [similar claims on one of our podcasts](/2018/08/is-bgp-good-enough-with-dinesh-dutt-on.html), and I wrote [numerous blog posts on the same topic](/series/dcbgp.html). Not that anyone would care or listen; it's so much better to watch vendor slide decks full of the latest unicorn dust... but in the end, it's [usually not the protocol that's broken](/2018/05/is-ospf-or-is-is-good-enough-for-my.html), but the network design.