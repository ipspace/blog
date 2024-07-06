---
date: 2017-01-27 09:02:00+01:00
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_70-To_Drop_or_Not_to_Drop.mp3
tags:
- podcast
- QoS
- Software Gone Wild
title: To Drop or To Delay, That’s the Question on Software Gone Wild
url: /2017/01/to-drop-or-to-delay-thats-question-on.html
---
A while ago I decided it\'s time to figure out [whether it\'s better to drop or to delay TCP packets](/2016/09/policing-or-shaping-it-depends.html), and quickly figured out you get 12 opinions (usually with no real arguments supporting them) if you ask 10 people. Fortunately, I know someone who deals with TCP performance for living, and [Juho Snellman](https://www.snellman.net/blog/) was kind enough to agree to record another podcast.

{{<note update>}}Update 2017-03-31: Added *More information* section{{</note>}}
<!--more-->
**Spoiler alert:** many things we \"know\" about TCP are not exactly true. For example, packet drops are not a big deal (but selective acknowledgments and default retransmit timeouts are).

Interestingly, we started discussing the reasons some [people want to reinvent TCP, do it over UDP, and hide what they\'re doing from the network](https://www.snellman.net/blog/archive/2016-12-01-quic-tou/), but quickly got back to the fundamental question: to drop or to delay.

The answer is surprising: while you might get better results responding to increased delays (as opposed to packet drops), responding only to drops is a better survival strategy, as latency-sensitive algorithms back off sooner than drop-sensitive ones and thus starve in a congested networks when competing with drop-sensitive algorithms.

For more details, listen to [Episode 70](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_70-To_Drop_or_Not_to_Drop.mp3) of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild).

### More information

-   [TIMELY article by Google researchers](https://research.google.com/pubs/pub43840.html)
-   [ACM queue article on BBR](http://queue.acm.org/detail.cfm?id=3022184)
-   [Great BBR summary by The Morning Paper](https://blog.acolyer.org/2017/03/31/bbr-congestion-based-congestion-control/)

{{<jump>}}[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_70-To_Drop_or_Not_to_Drop.mp3){{</jump>}}

