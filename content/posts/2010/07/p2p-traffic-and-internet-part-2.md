---
date: 2010-07-27 07:21:00.004000+02:00
tags:
- service providers
- Internet
- QoS
title: P2P Traffic and the Internet, Part 2
url: /2010/07/p2p-traffic-and-internet-part-2/
---
As expected, my [*P2P traffic is bad for the network*](/2010/07/p2p-traffic-is-bad-for-network/) post generated lots of comments; from earning me another wonderful title (*shill for Internet monopolies)* that I'll proudly add to my previous awards to numerous technical comments and even a link to a [very creative use of BitTorrent to solve software distribution problems](http://torrentfreak.com/facebook-uses-bittorrent-and-they-love-it-100625/) (thanks again, @[packetlife](http://twitter.com/packetlife)).

Most of the commentators missed the main point of my post and somehow assumed that since I don't wholeheartedly embrace P2P traffic I want to ban it from the Internet. Far from it, what I was trying to get across was a very simple message:
<!--more-->
-   current QoS mechanisms allow P2P clients to get disproportionate amount of bandwidth;
-   per-session queuing needs to be replaced with per-user queuing;
-   few devices (usually dedicated boxes) can do per-user bandwidth management.

Not surprisingly, Petr Lapukhov was even more succinct: "*The root cause of P2P QoS problem is the flow-fairness and congestion-adaption model that has been in the Internet since the very first days*" and thus made a great introduction to a more fundamental problem: while we're rambling about the "popular" P2P topic, we're forgetting that Internet was never designed to cope with what we're throwing at it.
<!--more-->
The basic premise commonly used in the design of Internet protocols was the cooperative user behavior. This attitude allowed Internet to become fast and cheap and finally triumph in the public data arena. While the ITU was struggling to design foolproof protocols that the users could never abuse, IETF was happily creating just-good-enough protocols that worked well between a few friends. The ultimate example: SMTP versus X.400. Unfortunately, in this case ITU had the last laugh \... with sender authentication and nonrepudiation embedded in X.400 and per-message charges billed to the sender our inboxes would be spam-free. Obviously, the victory (if there was one) was pyrrhic, as (public) X.400 has years ago shared the fate of T.rex.

Likewise, TCP was designed for an environment in which every session should get the same share of bandwidth (in the early days, one user would have one or at most a few sessions). It works astonishingly well: if you run X parallel TCP sessions across a link (even without using any decent QoS mechanism), each one will (on average) get its fair share. Low-speed queuing mechanisms like WFQ enhanced the concept to ensure that:

-   TCP sessions get their fair share even when non-TCP traffic tries to grab more than expected;
-   Interactive sessions are not preempted by batch sessions (with large packet bursts).

The third example: years ago, when Internet QoS became a hot topic, we had two competing architectures:

-   *Intserv*, where each application session would have to reserve the bandwidth it needs and routers could perform explicit CAC (call admission control), even tied to an authentication server (yeah, it was probably an ITU plant) and
-   *Diffserv,* where the core network would rely on the DSCP markers in individual packets and perform only low-granularity QoS decisions (for example, per-class queuing and intra-class selective dropping).

As we all know, *Diffserv* won because it scales \... but it comes with an implicit risk: the core routers have to trust the edge routers (or the users).

Last example (this one very close to my heart): BGP. It was [designed to be used between cooperating entities](/2010/03/secure-bgp/) and thus has very few security mechanisms (inbound and outbound filters are primarily a policy tool) and no authentication-of-origin mechanisms. The simple design was an obvious success: [IDRP](http://www.javvin.com/protocolIDRP.html) never moved far beyond whiteboard (PowerPoint was not so popular in those days), but we're occasionally paying a high price: [a router you've never heard about can cause Internet-wide flaps](/2009/02/root-cause-analysis-oversized-as-paths/).

To summarize: Internet is as successful as it is because it's simple and just-good-enough \... and it was designed that way because the designers assumed cooperative behavior of all parties. People that game the system might in the end force the industry to design and deploy more complex (and thus more expensive) solutions.
