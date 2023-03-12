---
cdate: 2022-07-10
comment: "Ever since the SDN hype started, vendors and pundits were quick to tell\
  \ us how the SDN controllers (and programmers) will replace the traditional networking\
  \ engineers. \n\nIn 2012 I thought there's no need to worry about that happening\
  \ in foreseeable future, and not much has changed since then (apart from the obnoxious\
  \ never-ending _[should networking engineers become programmers](https://blog.ipspace.net/2014/06/will-network-engineers-become.html)_\
  \ debate).\n\nIn related news:\n\n* CCIE certification is still relevant (in 2022),\
  \ and Cisco introduced DevNet certification\n* While MP-TCP got into limited production,\
  \ we still haven't solved the major problems of the TCP/IP protocol stack\n* In\
  \ 2021 Hype Cycle, Gartner declared OpenFlow-based SDN _dead before reaching plateau_\n"
date: 2012-09-25 07:24:00+02:00
sdn_101_tag: extra
series:
- sdn_101
series_weight: 80
tags:
- SDN
- data center
- OpenFlow
- certifications
title: SDN, Career Choices and Magic Graphs
url: /2012/09/sdn-career-choices-and-magic-graphs.html
---
The current explosion of SDN hype (further fueled by recent VMworld announcement of Software-Defined Data Centers) made some networking engineers understandably nervous. This is the question I got from one of them:

> I have 8 plus years in Cisco, have recently passed my CCIE RS theory, and was looking forward to complete the lab test when this SDN thing hit me hard. Do you suggest completing the CCIE lab looking at this new future of Networking?

Short answer: the sky is not falling, [CCIE still makes sense](https://blog.ipspace.net/2012/02/does-ccie-still-make-sense.html), and [IT will still need networking people](http://packetpushers.net/does-sdn-mean-it-will-be-able-to-get-rid-of-network-people/).
<!--more-->
However, as I recently collected a few magic graphs for a short keynote speech, let me reuse them to illustrate this particular challenge we're all facing. Starting with the obvious, here's the legendary [*Diffusion of Innovations*](http://en.wikipedia.org/wiki/Diffusion_of_innovations): every idea is first adopted by a few early adopters, followed by early and late majority.

{{<figure src="http://upload.wikimedia.org/wikipedia/commons/0/0f/Diffusionofideas.PNG" caption="Source: [Wikipedia](http://en.wikipedia.org/wiki/File:Diffusionofideas.PNG)" width="500">}}

Networking in general is clearly in the late majority/laggards phase. What's important for our discussion is the destruction of value-add through the diffusion process. Oh my, I sound like a freshly-baked MBA whiz-kid, let's reword it: as a technology gets adopted, more people understand it, the job market competition increases, and thus it's harder to get a well-paying job in that particular technology area. Supporting Windows desktops might be a good example.

As a successful technology matures, it moves through the four parts of another magic matrix (this one from [Boston Consulting Group](http://en.wikipedia.org/wiki/Boston_Consulting_Group_Matrix)).

{{<figure src="/2012/09/s520-BCG_Graph.png">}}

Initially every new idea is a great unknown, with only a few people brave enough to invest time in it (CCIE R&S before Cisco made it mandatory for Silver/Gold partner status). After a while, the successful ideas explode into stars with huge opportunities and fat margins (example: CCIE R&S a decade ago, [Nicira-style SDN today](https://blog.ipspace.net/2012/07/vmware-buys-nicira-hypervisor-vendor.html)... at least for Nicira's founders), degenerates into a cash cow as the market slowly gets saturated (CCIE R&S is probably at this stage by now) and finally (when everyone starts doing it) becomes an old dog not worth bothering with.

Does it make sense to invest into something that's probably in a cash cow stage? The theory says "as much as needed to keep it alive", but don't forget that CCIE R&S will likely remain very relevant a long time:

-   The protocol stacks we're using haven't changed in the last three decades (apart from extending the address field from 32 to 128 bits), and although people are working on proposals like MP-TCP, those proposals are still in experimental stage;
-   Regardless of all the SDN hoopla, neither OpenFlow nor other SDN technologies address the real problems we're facing today: [lack of session layer in TCP](https://blog.ipspace.net/2009/08/what-went-wrong-tcpip-lacks-session.html) and the [use of IP addresses in application layer](https://blog.ipspace.net/2009/08/what-went-wrong-socket-api.html). They just give you different tools to implement today's kludges.
-   Cisco is doing constant refreshes of its CCIE programs to keep them in the *early adopters* or *early majority* technology space, so the CCIE certification is not getting commoditized.
-   If you [approach the networking certifications the right way](https://blog.ipspace.net/2008/09/knowledge-or-recipes.html), you'll [learn a lot about the principles and fundamentals](http://blog.ipspace.net/2008/11/sometimes-path-is-more-important-than.html), and you'll need that knowledge regardless of the daily hype.

Now that I've mentioned *experimental* technologies -- don't forget that not all of them get adopted (even by early adopters). Geoffrey Moore made [millions writing a book](http://en.wikipedia.org/wiki/Crossing_the_Chasm) that pointed out that obvious fact. Of course he was smart enough to invent a great-looking wrapper -- he called it *Crossing the Chasm*.

{{<figure src="/2012/09/chasm.gif" caption="Source: [Crossing the Chasm & Inside the Tornado](http://www.exampler.com/testing-com/writings/reviews/moore-chasm.html)">}}

The *crossing the chasm* dilemma is best illustrated with [Gartner Hype Cycles](http://en.wikipedia.org/wiki/Hype_cycle) (oh my, there's a Gartner reference in my blog post). After all the initial hype (that [we've seen with OpenFlow and SDN](https://blog.ipspace.net/2011/03/open-networking-foundation-fabric.html)) resulting in *peak of inflated expectations*, there's the ubiquitous *through of disillusionment*. Some technologies die in that quagmire; in other more successful cases we eventually figure out how to use them (*slope of enlightenment*).

{{<figure src="http://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Gartner_Hype_Cycle.svg/500px-Gartner_Hype_Cycle.svg.png" caption="Source: [Wikipedia](http://en.wikipedia.org/wiki/File:Gartner_Hype_Cycle.svg)">}}

We still don't know how well SDN will be doing crossing the chasm (according to the latest Gartner's charts, OpenFlow still hasn't reached the hype peak - I dread what\'s still lying ahead of us); we've seen only a few commercial products and none of them has anything close to widespread adoption (not to mention the [reality of three IT geographies](http://it20.info/2012/09/cloud-and-the-three-it-geographies-silicon-valley-us-and-rest-of-the-world/)).

Anyhow, since you've decided you want to work in networking, one thing is certain: technology will change (whatever the change will be), and it will happen with or without you. At every point in your career you [have to invest some of your time into learning something new](http://packetpushers.net/where-the-puck-is-going/). Some of those new things will be duds; others might turn into stars. See also [*Private Clouds Will Change IT Jobs, Not Eliminate Them*](https://web.archive.org/web/20130201081243/http://www.networkcomputing.com/private-cloud-tech-center/private-clouds-will-change-it-jobs-not-e/240007533) by Mike Fratto.

Finally, don't ask me for "what will the next big thing be" advice. Browse through the six years of my blog posts. You might notice a clear shift in focus; it's there for a reason.
