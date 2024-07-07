---
date: 2014-10-27 10:25:00+01:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_13-Cumulus_Linux.mp3
tags:
- Cumulus Linux
- SDN
- Software Gone Wild
- podcast
title: Cumulus Linux in Real Life on Software Gone Wild
url: /2014/10/cumulus-linux-in-real-life-on-software/
---
A year ago Matthew Stone first heard about Cumulus Linux when I [ranted about it on a Packet Pushers podcast](http://packetpushers.net/show-162-the-bourbonator-rises-at-nfd6/) (which only proves that any publicity is good publicity even though some people thought otherwise at that time), and when his cloud service provider company started selecting ToR switches he considered Cumulus together with Cisco and Arista... and chose Cumulus.
<!--more-->
I firmly believe hands-on experience in production environment always beats vendor marketing, so I was really keen to hear how he feels after running his whole data center network on Cumulus-powered switches for a few months... and thus the [Episode 13 of Software Gone Wild](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_13-Cumulus_Linux.mp3) was recorded.

It's obvious Matt's a true believer, but he was also very open about the glitches he found in Cumulus Linux, so I'm positive you'll enjoy our hour-long chat. Here are a few highlights.

### Why did they go with Cumulus?

-   They were selecting ToR switches and had to choose between Cisco, Arista or Cumulus.
-   Cisco lacked programmability features, Arista was (obviously) more expensive than whitebox switch + Cumulus Linux.

### On the command line interface and glitches:

-   Most network features are handled by open-source Linux daemons like Quagga;
-   You don't have a unified CLI, you're using Linux commands to configure Linux networking;
-   Various daemons have inconsistent interfaces - for example, you have to telnet to Quagga VTY to configure it -- but Cumulus is working on fixing those inconsistencies;

### Does it make sense?

Matt claims that Cumulus might be an ideal solution for large shops that have the resources to developed things themselves, for everyone else it opens the possibility of third-party applications running on top of it. In his own words, "*you could switch the operating system if you don't like the one you use today*" (let's ignore that there's approximately one at the moment).

[Enjoy the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_13-Cumulus_Linux.mp3) and don't forget to [subscribe](http://www.ipspace.net/Feeds) to the [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild) feed.
