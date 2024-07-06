---
date: 2010-07-12 06:37:00.010000+02:00
tags:
- bridging
- switching
- networking fundamentals
title: 'Bridges: a Kludge that Shouldn''t Exist'
url: /2010/07/bridges-kludge-that-shouldnt-exist.html
---
During the last weeks I tried hard to sort out my thoughts on routing and bridging; specifically, what's the difference between them and why you should use routing and not bridging in any large-scale network (regardless of whether it happens to be cramped into a single building called *Data Center*).

My vague understanding of layer 2 (Data Link layer) of the [OSI model](http://en.wikipedia.org/wiki/OSI_model) was simple: it was supposed to provide frame transport between neighbors (a neighbor is someone who is on the same physical medium as you are); layer 3 (Network layer) was supposed to provide forwarding between distant end nodes. Somehow the bridges did not fit this nice picture.

As I was struggling with this ethereally geeky version of a much older [angels-on-a-pin](http://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F) problem, Greg Ferro of [EtherealMind.com](http://etherealmind.com/) (what a coincidence, isn't it) shared a link to a [GoogleTalk given by Radia Perlman](http://www.youtube.com/watch?v=N-25NoCOnP4), the author of the Spanning Tree Protocol and co-author of TRILL. And guess what -- in her opening minutes she said "*Bridges don't make sense. If you do packet forwarding, you should do it on layer 3*". That's so good to hear; I'm not crazy after all.
<!--more-->
Radia listed several shortcomings of layer-2 forwarding (@ 8:30 in her talk, long explanations are mine; if you think they are wrong, don't blame her):

-   *Layer-3 addresses have topological significance*. The layer-3 addressing space is hierarchical, so you can summarize and create addressing and routing hierarchies. *Layer-2 addressing space is flat*; from the perspective of a forwarding device, the layer-2 addresses are spread randomly across the network.
-   *Layer-2 protocols don't have a hop count*, so you can't detect a forwarding loop. You have to invent all sorts of fixes (like STP) to prevent the loops from ever happening.
-   *Layer-2 protocols don't support fragmentation* or path MTU discovery, so it's impossible to do forwarding across segments with mismatched MTUs \... but then Data Link layer was never designed to handle that task.
-   *Layer-2 protocols lack router-to-host error messages* (like ICMP). Yet again, it was never a layer-2 task, but you need them if you want to have a routable protocol.

I would add one more very significant drawback: layer-3 forwarding is deterministic; you know where the destination is supposed to be. Layer-2 forwarding is guesswork; if you don't know where the destination is, you just send a copy of the frame in all directions, just to make sure it will eventually hit the target.

OK, now we know bridges shouldn't exist, yet they do. What went wrong? Radia explains that as well.

Approximately 30 years ago when Ethernet just started to appear, Radia was working on DECnet, one of the first truly well-designed networking protocols. DECnet was used to connect minicomputers manufactured by Digital Equipment Corporation (DEC) over WAN links and later over Ethernet ([DECnet Phase IV](http://en.wikipedia.org/wiki/DECnet)). In those days, there were no PCs and users were using [text terminals](http://en.wikipedia.org/wiki/Computer_terminal) connected to computers with RS-232 cables. Using regular cables, [RS-232 connections could be only a few meters long](#Cables) (and you had a serial port in your minicomputer for every user attached to it).

DEC solved this problem by developing the first terminal servers. Obviously they had to be low(er) cost (nobody would buy another minicomputer just to connect terminals to it) with very limited RAM and CPU capabilities. Radia suggested using DECnet (@ 7:20), but the development team decided to create their own protocol ([LAT](http://en.wikipedia.org/wiki/Local_Area_Transport)) which had no layer 3 because "their customer would never want to talk between Ethernet segments" (@ 7:40).

I can understand the need for a separate protocol. DECnet was a behemoth. I was "fortunate" enough to have it running on MS-DOS as Pathworks; it consumed half of the then-available 640K of RAM (that's kilo-bytes \... for those of you who think your laptop needs 4GB of RAM). What I cannot understand is the very limited perspective of LAT developers \... but then our industry is filled with relics and wrong decisions that we still have to live with decades later (my favorites: [lack of session layer in TCP/IP](/2009/08/what-went-wrong-tcpip-lacks-session.html) and the [IP multihoming](/2009/05/lack-of-ipv6-multihoming-elephant-in.html)).

Anyhow, LAT was implemented and it was not routable \... and then all of a sudden the customers wanted to have terminal servers on one Ethernet segment talking to computers connected to another Ethernet segment. Instead of telling the LAT people to get lost (not an option, LAT-based terminal servers represented 10% of DEC's revenue) or redesign their broken protocol, the problem was rephrased as "we need a magic box that can connect two Ethernet segments" (@ 10:00).

The answer could be any of these:

-   You need a router and a routable protocol (member of an ISO/OSI standard committee);
-   You can't route non-routable protocols; I can write a paper proving that (academic researcher with a life-long tenure);
-   Told you so ([Network Zen Master](http://etherealmind.com/network-zen-most-important-technology-infrastructure/));
-   Let's build a workaround (MacGyver answer worthy of a true networking engineer).

The rest is history: they surged ahead, built the bridge, and Radia designed the STP. A masterpiece of engineering, but still a kludge fixing a problem that shouldn't have existed in the first place. The networking landscape was changed forever... and not necessarily for the better.
