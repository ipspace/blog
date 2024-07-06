---
cdate: 2022-07-06
comment: 'The industry press jumped onto the [ONF/OpenFlow hype](/2011/03/open-networking-foundation-fabric.html)
  with gusto, without ever trying to figure out what it''s all about. Not surprisingly,
  the articles they managed to produce were full of nonsense, prompting me to write
  yet another rant in April 2011.


  Sad fact: some publications never clean up the mess they made, even when there''s
  a huge clash between what they published and the reality. The Network World article
  was still on their web site in July 2022.

  '
date: 2011-04-19 07:23:00+02:00
sdn_hype_tag: initial
series:
- sdn_hype
tags:
- MPLS
- SDN
- OpenFlow
title: 'OpenFlow FAQ: Will the Hype Ever Stop?'
url: /2011/04/openflow-faq-will-hype-ever-stop.html
---
Network World has published another masterpiece last week: [*FAQ: What is OpenFlow and why is it needed?*](https://www.networkworld.com/article/2202144/data-center-faq-what-is-openflow-and-why-is-it-needed.html) Following the [physics-changing promises made during the Open Network Foundation launch](/2011/03/open-networking-foundation-fabric.html), one would hope to get some straight facts; obviously things don't work that way. Let's walk through some of the points. While most of them might not be too incorrect from an oversimplified perspective, they do over-hype a potentially useful technology way out of proportions.

NW: "*OpenFlow is a programmable network protocol designed to manage and direct traffic among routers and switches from various vendors.*" This one is just a tad misleading. OpenFlow is actually a [protocol that allows a controller to download forwarding tables into one or more switches](/2011/04/what-is-openflow.html). Whether that manages or directs traffic depends on what controller is programmed to do.
<!--more-->
NW: "*The technology consists of three parts: \[\...\] and a proprietary OpenFlow protocol for the controller to talk securely with switches.*" Please do decide what you think *proprietary* means. All parts of the OpenFlow technology are defined in publicly available documents [under BSD-like license](http://www.openflow.org/wp/legal/).

NW: "*OpenFlow is designed to provide consistency in traffic management and engineering by making this control function independent of the hardware it\'s intended to control.*" How can a low-level flow-table-control API provide what this statement claims it does? It all depends on the controller implementation.

NW: "*The programmability of the MPLS capabilities of a particular vendor\'s platform is specific to that vendor.*" And the OpenFlow-related capabilities of individual switches will depend on specific implementations by specific vendors. Likewise, the capabilities of an OpenFlow controller will be specific to that vendor. What exactly is the fundamental change?

NW: "*MPLS is a Layer 3 technique while OpenFlow is a Layer 2 method*" Do I need to elaborate on this gem? Let's just point out that OpenFlow works with MAC addresses, IP subnets, IP flow 5-tuples, VLANs or MPLS labels. Whatever a switch can do, OpenFlow can control it.

But wait... OpenFlow has no provision for IPv6 at all[^OFv6]. Maybe Network World is so futuristic they consider a technology without IPv6 support a layer-2 technology.

[^OFv6]: IPv6 support was added to version 1.2 of OpenFlow protocol, and improved in version 1.3.

### Prefer Facts over Fiction?

You'll get a hefty dose of real-life facts and skepticism [ipSpace.net SDN webinars](https://www.ipspace.net/SDN) (available with [standard subscription](https://www.ipspace.net/Subscription)).

### Revision History

2022-07-06
: Fixed the link to Network World article and added IPv6 footnote.