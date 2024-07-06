---
anycast_tag: intro
date: 2021-03-03 06:02:00+00:00
lastmod: 2021-03-05 16:22:00
series:
- anycast
series_weight: 100
tags:
- IP routing
- load balancing
title: Chasing Anycast IP Addresses
---
One of my readers sent me this question:

> My job required me to determine if one IP address is unicast or anycast. Is it possible to get this information from the bgp dump?

TL&DR: Not with anything close to 100% reliability. An [academic research paper](https://www.eecis.udel.edu/~hnw/paper/sigcomm-ccr-2019.pdf) (HT: Andrea di Donato) documents a false-positive rate of around 10%.

If you're not familiar with *[IP anycast](/2008/07/anycast.html)*: it's a brilliant idea of advertising the same prefix from multiple independent locations, or the same IP address from multiple servers. Works [like a charm for UDP](/2019/10/worth-reading-anycast-dns-in-enterprise.html) (that's how all root DNS servers are built) and supposedly pretty well across distant-enough locations for TCP (with a long list of caveats when used within a data center).
<!--more-->
Forgetting the trivial intra-DC case (analyze next hops on edge switches and figure out if the same IP prefix points to multiple servers), the question "*is a prefix advertised from multiple locations (anycast), or is it just an AS advertising a single prefix from its global network (business-as-usual)*" is impossible to answer by looking at BGP updates.

You could explore public BGP looking glasses, or parse public BGP feeds, and you'll either:

* Observe the IP prefix being announced from the same AS world-wide, which would be perfectly legal if the organization had a global network of their own.
* Observe the IP prefix announced from multiple autonomous systems, which could indicate an anycast IP address, or a global organization too lazy to own an AS.

You could also look at geographical distribution of upstream AS, distance between upstream AS pairs, maximum distance of upstream AS... and still get a 10% false positive (see link above).

Years ago, someone got a great idea to use speed of light to answer the question. Deploy probes around the globe, and measure their RTT to the suspected anycast IP address. Assume you're dealing with a single IP address, and see if you can break the speed of light (example: short RTT in Sidney and London).

Deploying the probes shouldn't be a big deal. Even if you can't use [RIPE Atlas](https://atlas.ripe.net/), it shouldn't be a problem to deploy a few virtual machines in one of the large public clouds.

An even better idea is to send probes (example: pings, TCP SYNs) to the target IP address from a globe-spanning anycast network. If the destination is a unicast address, all responses will go to a single probing node (the one closest to the destination), if multiple probes receive the responses, you're almost certainly dealing with an anycast destination. For more details, [read this article](https://blog.apnic.net/2020/12/15/manycast2-using-anycast-to-measure-anycast/) (thanks a million to Alexander Grigorenko for posting the link in the comments).

### Revision history

2021-03-06
: Added a link to *‌Towards Passive Analysis of Anycast in Global Routing: Unintended Impact of Remote Peering* article suggested by Andrea di Donato.

2021-03-05
: Reworded the last paragraph together with a link to MAnycast² article.
