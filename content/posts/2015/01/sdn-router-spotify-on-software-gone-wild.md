---
date: 2015-01-16 10:32:00+01:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_19-SDN_Router_at_Spotify.mp3
tags:
- podcast
- SDN
- Software Gone Wild
title: SDN Router @ Spotify on Software Gone Wild
url: /2015/01/sdn-router-spotify-on-software-gone-wild/
series: vagg
vagg_tag: sdn
---
Imagine you need a data center WAN edge router with multiple 10GE uplinks. You'd probably go for an ASR or an MX-series router, right? How about using a 2 Tbps ToR switch and an SDN solution to make it work with the full Internet routing table?

[David Barroso](https://www.linkedin.com/in/dbarrosop) from Spotify decided to do exactly that. He figured out he needs only a small fraction of the functionality of a reassuringly expensive WAN edge router. Then he listened to the NANOG presentation by Elisa Jasinska, said "*that's exactly how I could figure out what I really need in my forwarding tables*", and implemented a good-enough solution that solves his WAN connectivity challenges with an Arista ToR switch.
<!--more-->
You'll find more details in [Episode 19](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_19-SDN_Router_at_Spotify.mp3) of [Software Gone Wild](http://ipspace.net/SGW); and here's even more background information:

- [David's presentation](https://www.youtube.com/watch?v=o1njanXhQqM) from [SDN meetup in Stockholm](http://www.meetup.com/Spotify/events/212616582/)
- [SDN Internet Router documentation](https://media.readthedocs.org/pdf/sdn-internet-router-sir/latest/sdn-internet-router-sir.pdf)
- [SDN Internet Router project at Github](https://github.com/dbarrosop/sir)
- [SDN Internet Router - Part 1](https://labs.spotify.com/2016/01/26/sdn-internet-router-part-1/) (what is Internet and other stories)
- [SDN Internet Router - Part 2](https://labs.spotify.com/2016/01/27/sdn-internet-router-part-2/) (technical details and deployment experience)
- [SDN Internet Router In Production](/2015/10/sdn-internet-router-is-in-production-on/) - followup podcast with David Barroso
- [Toolsmith @ Netflix](/2014/08/toolsmith-netflix-on-software-gone-wild/) podcast with Elisa Jasinska
- [Pmacct podcast](/2014/08/pmacct-traffic-analysis-tool-with/) with Paolo Lucente
- [NANOG presentation](https://www.youtube.com/watch?v=4VnwwkZG1n8) from Elisa Jasinska and Paolo Lucente
