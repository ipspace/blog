---
date: 2013-05-28 07:10:00+02:00
tags:
- SDN
- switching
- OpenFlow
- Internet
title: Could IXPs Use OpenFlow to Scale?
url: /2013/05/could-ixps-use-openflow-to-scale.html
---
The SDN industry probably considers me an old and grumpy naysayer (and I'm positive Mrs Y has a special place in their hearts after [her recent blog post](http://packetpushers.net/sdn-savior-or-grifter/)), so I tried really hard to find a real-life example where OpenFlow could be used to solve [mid-market innovator's dilemma](http://telecomoccasionally.wordpress.com/2012/02/20/mid-market-innovators-dilemma/) to balance my usual [OpenFlow and SDN](http://demo.ipspace.net/get/OpenFlow%20SDN.pdf) presentation.
<!--more-->
[Internet Exchange Points (IXP)](http://packetpushers.net/show-24-internet-exchanges-peering/) seemed a perfect fit -- they are high-speed mission-critical environments usually implemented as geographically stretched layer-2 networks, and facing all sorts of security and scaling problems. [Deploying OpenFlow on IXP edge switches](http://demo.ipspace.net/get/Could%20IXPs%20Use%20OpenFlow%20To%20Scale.pdf) would results in standardized security posture that wouldn't rely on idiosyncrasies of particular vendor's implementation, and we could use OpenFlow to implement ARP sponge (or turn ARPs into unicasts sent to ARP server).

I presented these ideas at [MENOG 12](/2013/03/the-best-of-menog-12.html) in March 2013 and got a few somewhat interested responses ... and then I asked a really good friend with significant operational experience in IXP environments for feedback. Not surprisingly, the reply was a cold shower:

> I am not quite sure how this improves current situation. Except for the ARP sponge everything else seem to be implemented by vendors in one form or another. For the ARP sponge, AMS-IX uses great software developed in house that they've open-sourced.

As always, from the ops perspective proven technologies beat shiny new tools ;)

On a somewhat tangential topic, Dean Pemberton runs [OpenFlow in production in New Zealand Internet Exchange](http://www.apricot2013.net/__data/assets/pdf_file/0011/58934/project-cardigan_1361872406.pdf). His deployment model is totally different: the IXP is a layer-3 fabric (not a layer-2 fabric like most Internet exchanges), and his route server is the only way to exchange BGP routes between members. He's using Quagga and RouteFlow to program Pica8 switches.

A note from a grumpy skeptic: his deployment works great because he's carrying a pretty limited number of BGP routes -- the Pica8 switches he's using [support up to 12K routes](http://www.pica8.com/documents/pica8-datasheet-48x1gbe-p3290-p3295.pdf). IPv4 or IPv6? Who knows, the data sheet ignores that nasty detail.

{{<jump>}}[View the presentation](http://demo.ipspace.net/get/Could%20IXPs%20Use%20OpenFlow%20To%20Scale.pdf){{</jump>}}

