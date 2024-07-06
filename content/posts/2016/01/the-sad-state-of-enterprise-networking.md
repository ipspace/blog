---
date: 2016-01-11 07:25:00+01:00
tags:
- SDN
- data center
title: The Sad State of Enterprise Networking
url: /2016/01/the-sad-state-of-enterprise-networking.html
---
John wrote an optimistic comment to my [fashionable designs rant](/2015/12/the-grumpy-old-network-architects-and.html):

> Nobody in their right mind does \"fashionable\" things when dealing with infrastructures that are required to be solid, dependable and robust.

Unfortunately many enterprises aren't that prudent -- the last [Expert Express](https://www.ipspace.net/ExpertExpress) engagement I had in 2015 was yet another customer who lost two major data centers due to a [bridging loop](/2012/05/layer-2-network-is-single-failure.html) spilling over a [stretched VLAN infrastructure](/2011/06/stretched-clusters-almost-as-good-as.html).
<!--more-->
### Why oh Why?

One has to wonder why reasonable people implement fatally flawed architectures that are bound to explode sooner or later. Sometimes it's due to lack of understanding of how things really work (and what their drawbacks are), sometimes it's a CIO (often prodded by pressure from all other teams) overriding networking team's objections and believing vendor marketectures more than their own employees.

{{<note info>}}I'm always flabbergasted when realizing someone trusts a vendor (whose primary goal is to sell more products) more than own employees (who are at least marginally concerned with the health of their network because their jobs depend on it), but that's life. Let's move on.{{</note>}}

OK, so why do vendors promote crazier and crazier architectures that nobody building a scalable network would touch with a 10-foot pole? It's really simple (aka *follow the money*): the networking industry has a fundamental problem. After you get to a point where everyone can watch Netflix at reasonable quality and most of the data center problems can be solved by throwing more bandwidth at the problem and/or fixing the problem in server operating system or application, there's not much more you can sell, so you have to start selling unicorn droppings and pixie dust hoping you'll dazzle everyone so they won't realize networking shouldn't be more than fast plumbing utility.

Obviously you can't sell those works-best-in-PowerPoint products to anyone who actually understands how networking works, so you [start selling magic](/2013/04/this-is-what-makes-networking-so-complex.html) to CIO and all the teams that have to interact with the networking team, all the time telling them how stupid the networking team is because they can't make it work (but don't worry, our next-generation controller-based machine learning tool will solve that as well, and you won\'t need those darn CCIEs any longer). 

The whole shenanigan works because like most people many CIOs prefer to believe in Santa Claus and magic instead of realizing that they have to fix application design, development and deployment processes if they want their organization to be more like Google or Amazon or Netflix... until they realize they have to [reformat their data center](/2015/11/can-you-afford-to-reformat-your-data.html) instead of their iPhone.

However, when facing such a CIO, you might want to play the Gartner trump card: try to engage [Andrew Lerner](http://www.gartner.com/analyst/45420/Andrew-Lerner) who yet again (not surprisingly) [totally agrees with me](http://blogs.gartner.com/andrew-lerner/2015/12/08/worst-networking-practices/).
