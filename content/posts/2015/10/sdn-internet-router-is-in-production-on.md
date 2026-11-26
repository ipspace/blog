---
date: 2015-10-16 08:45:00+02:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_42-SDN_Internet_Router_-_Update.mp3
tags:
- podcast
- SDN
- Internet
- WAN
- Software Gone Wild
title: SDN Internet Router Is in Production on Software Gone Wild
url: /2015/10/sdn-internet-router-is-in-production-on/
series: vagg
vagg_tag: sdn
---
You might remember the [great idea David Barroso had last autumn](/2015/01/sdn-router-spotify-on-software-gone-wild/) -- turn an Arista switch into an Internet edge router (SDN Internet Router -- SIR). In the meantime, he implemented that solution in a production environment serving high-speed links at multiple Internet exchange points. It was obviously time for [another podcast on the same topic](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_42-SDN_Internet_Router_-_Update.mp3).
<!--more-->
As this was the first podcast recording after the summer holidays, we had to start with the great fun some of us had during July and August (just to make you jealous), and then turned to more serious topics:

- What's going on with SDN Internet Router (which is now in production);
- The redesign and refactoring of the original idea;
- The hardware problems David experienced while preparing for the production deployment;
- How a smart engineer increases the switch IP forwarding table size by squeezing IP prefixes into the MAC address table;
- How Arista EOS got decent BGP daemon and fast parsing of prefix lists;
- Why you really don't need forwarding toward full routing table anywhere;
- The details of the fully-packaged solution David is putting together;
- How you could use SIR to improve your IXP peerings;
- How you could make SIR work on Juniper or Cumulus boxes;

For more details, listen to [Episode 42](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_42-SDN_Internet_Router_-_Update.mp3) (yes, I know what 42 is ;) of [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild), and follow these links:

- [David's presentation](https://www.youtube.com/watch?v=o1njanXhQqM) from [SDN meetup in Stockholm](http://www.meetup.com/Spotify/events/212616582/)
- [SDN Internet Router documentation](https://media.readthedocs.org/pdf/sdn-internet-router-sir/latest/sdn-internet-router-sir.pdf)
- [SDN Internet Router project at Github](https://github.com/dbarrosop/sir)
- [SDN Internet Router - Part 1](https://labs.spotify.com/2016/01/26/sdn-internet-router-part-1/) (what is Internet and other stories)
- [SDN Internet Router - Part 2](https://labs.spotify.com/2016/01/27/sdn-internet-router-part-2/) (technical details and deployment experience)
- [SDN Internet Router @ Spotify](/2015/01/sdn-router-spotify-on-software-gone-wild/) - the first podcast with David Barroso
- [Pmacct podcast](/2014/08/pmacct-traffic-analysis-tool-with/) with Paolo Lucente

{{<jump>}}
[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_42-SDN_Internet_Router_-_Update.mp3)
{{</jump>}}
