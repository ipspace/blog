---
title: "BGP Labs: a Year Later"
date: 2024-07-08 06:57:00+0200
tags: [ BGP, netlab ]
netlab_tag: bgplab
---
Last summer, I started a long-term project to [revive the BGP labs I created in the mid-1990s](https://bgplabs.net/99-about/).  I completed the original lab exercises (BGP sessions, IBGP, local preference, MED, communities) in late 2023 but then kept going. This is how far I got in a year:

* Twenty-six *[deploy BGP](https://bgplabs.net/basic/)* exercises, including [advanced settings](https://bgplabs.net/basic/#advanced) like [AS path manipulations](https://bgplabs.net/basic/#aspath), MD5 passwords and BFD, and new technologies like TCP/AO and interface EBGP sessions.
* Fifteen [BGP routing policies](https://bgplabs.net/policy/) exercises, covering the basic mechanisms as well as dirty tricks like route disaggregation
* Four [load balancing](https://bgplabs.net/basic/#lb) exercises, from EBGP ECMP to BGP Link Bandwidth and BGP Additional Paths.
* [Five challenges](https://bgplabs.net/#challenge-labs) for everyone who got bored doing the simple stuff ;)

That completes the BGP technologies I wanted to cover. I'll keep adding the challenge labs and advanced scenarios. [Here are some ideas](https://bgplabs.net/3-upcoming/); if you have others, please leave a comment.
<!--more-->
The labs are free of charge and can use [more than a dozen](https://netlab.tools/platforms/#platform-routing-support) different network operating systems. There's just a tiny gotcha: unless you're OK [with a device that can run as a container](https://blog.ipspace.net/2023/06/learn-routing-protocols-frr/) (in which case you can [get started in a few seconds](https://blog.ipspace.net/2024/06/bgp-labs-github-codespaces/)), you will have to invest your time into building the infrastructure first, but even then, you can build it with free/open-source software (apart from the network devices, of course).

