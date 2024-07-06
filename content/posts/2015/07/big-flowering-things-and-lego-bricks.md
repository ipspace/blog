---
date: 2015-07-29 08:46:00+02:00
tags:
- SDN
title: Big Flowering Things and Lego Bricks
url: /2015/07/big-flowering-things-and-lego-bricks.html
---
[Matt Oswalt](http://keepingitclassless.net/about-matt/) wrote a great blog post [complaining about vendors launching ocean-boiling solutions instead of focused reusable components](https://oswalt.dev/2015/07/big-flowering-thing/), and [one of the comments his opinion generated](/2015/07/must-read-big-flowering-thing.html?showComment=1437168590824#c2836266398982409387) was along the lines of "*I thought one of the reasons people wanted SDN, is because they wanted to deal with The Network -- think about The Network\'s Performance, Robustness and Services instead of dealing with 100s or 1000s of individual boxes.*"

The comment is obviously totally valid, so let me try to reiterate what Matt wrote using Lego bricks ;)
<!--more-->
If you ever played with Lego bricks (or Minecraft ;), you know you can use them to build almost anything (including [TCP/IP packets](https://righteousit.wordpress.com/2010/06/27/practical-visual-three-dimensional-pedagogy-for-internet-protocol-packet-header-control-fields/) and a [data center model](/2013/10/lego-data-center.html)). Not surprisingly, like any good engineer Matt wants Lego bricks -- reusable components that he could use to build his solutions.

{{<note>}}This doesn't mean that anyone apart from the engineers working with the bricks have to understand how they work -- although it helps if [they grasp the basics](/2015/07/why-should-i-care-about-networking.html). It's also no excuse for zillions of lame *network management* products.{{</note>}}

Unfortunately, it's hard to get useful Lego bricks in networking land. What we usually get are pretty useless components that can only be used in one way.

With the advent of SDN, the situation got worse -- most SDN vendors are selling you prefab solutions that [use proprietary protocols](/2015/06/software-defined-wanwell-orchestrated.html) and work only if [all components run their software](/2015/06/vertically-integrated-musings.html) - if anything, the networking is becoming even more monolithic than it has been before. It's like getting a Lego Death Star after Lord Business glued all the bricks together -- it looks awesome from the outside, but it's impossible to use the components to build anything else.

{{<figure src="http://images.amazon.com/images/G/01/toys/detail-page/B000FTXNRI-1-lg.jpg">}}

{{<note>}}Oh, do I have to mention that Death Star looks even cooler from the inside? You can never enjoy that view if you bought a glued-together version. Yeah, I know I\'m digressing ;){{</note>}}

Obviously the business people paying the engineers can't understand why they should pay people playing with Lego bricks (and even send them to training to understand the next-generation bricks coming out). All they want is a great toy, and I totally support that sentiment -- if all you want to do is look at the Death Star, there's no need to get involved with the individual bricks.

Unfortunately, the people who don't want to know anything about the bricks usually never consider what might happen when [they drop their toy](https://youtu.be/kEHRrZrXOdQ?t=4m20s) (or their younger sister sits on it). We all know vendors tend to promise heavens-on-earth when they're selling their warez, and most of us have at least one gruesome tech support story to share.

Finally, since everyone and their dog think their business is unique, they're usually not happy just looking at their Death Star -- they want to adapt it to the uniqueness of their situation, which is a bit hard to do if you cannot change it, because you bought a pre-glued toy, and not a box of bricks.

{{<note>}}Before you start writing a comment about SDN applications sitting on top of SDN controllers, do me a favor and read the documentation of those controllers. Most of them are no better than routers and switches we're dealing with today -- while all of them have a REST API, it's impossible to make them do something they were not supposed to do.{{</note>}}

### Want More?

For more real-life (or "contrarian" as someone put it) SDN perspectives [read my SDN books](http://www.ipspace.net/Books) or watch my [SDN webinars](https://www.ipspace.net/Roadmap/SDN_and_OpenFlow_webinars) and [presentations](http://www.ipspace.net/Presentations#Software_Defined_Networking).
