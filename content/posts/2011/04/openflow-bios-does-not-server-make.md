---
cdate: 2022-07-19
comment: 'The blog post was written in 2011, when the shortcomings of OpenFlow weren’t
  well understood, and some people still thought that just mentioning OpenFlow will
  magically bring the related controller software to life.


  A decade later, [OpenFlow remains a niche protocol](/2022/05/openflow-still-kicking/),
  and while we have a few controllers (commercial and open-source), no major vendor
  got interested enough in OpenFlow to launch OpenFlow-based switches or develop an
  OpenFlow controller (paying a few developers to work on Open DayLight does not count).

  '
date: 2011-04-08 17:15:00.003000+02:00
openflow_101_tag: ugly
series:
- openflow_101
series_weight: 160
tags:
- SDN
- data center
- OpenFlow
title: 'OpenFlow: BIOS Does Not a Server Make'
url: /2011/04/openflow-bios-does-not-server-make/
---
Last week Greg (\@etherealmind) Ferro invited me to the [OpenFlow Packet Pushers podcast](http://packetpushers.net/show-40-upending-networking/) with Matt Davey. I was pleasantly surprised by Matt's realistic attitude (you should really [listen to the whole podcast](http://packetpushers.net/show-40-upending-networking/)), it was nice to hear that they're running a country-wide pilot with OpenFlow-enabled switches deployed at several universities, and some of the applications he mentioned (for example, the capability to download ACLs into the switch from your customized application) definitely tickled my inner geek. However, I'm even more convinced that the brouhaha surrounding [Open Networking Foundation](http://www.opennetworkingfoundation.org/) has [little grounds in the realities of OpenFlow](/2011/03/open-networking-foundation-fabric/).
<!--more-->
Remember: [OpenFlow is an API allowing controlling software to download forwarding table entries into one or more switches](/2011/04/what-is-openflow/) (which can be L2, L3 or LSR switches). Any OpenFlow-based solution requires two components: the switching hardware with OpenFlow-capable firmware and the controlling software using the OpenFlow API.

The OpenFlow API will definitely enable many copycat vendors to buy merchant silicon, put it together and start selling their product with little investment in R&D (like the PC motherboard manufacturers are doing today). I am also positive the silicon manufacturers (like Broadcom) will have "*How to build OpenFlow Switch with Our Chipset*" application notes available as soon as they find OpenFlow commercially viable. Hopefully we'll see another Dell (or HP) emerge, producing low-cost reasonable-quality products in the low-end to mid-range market... but all these switches will still need networking software controlling them.

If you're old enough to remember the original PCs from IBM, you'll easily recognize the parallels. IBM documented PC hardware architecture and BIOS API (you even got BIOS source code), allowing numerous third-party vendors to build adapter cards (and later PC clones), but all those machines had to run an operating system, and most of them used MS-DOS (and later Windows). Almost three decades later, vast majority of PCs still run on Microsoft's operating systems.

Some people think that the potential adoption of OpenFlow API will magically materialize open-source software to control the OpenFlow switches, breaking the bonds of proprietary networking solutions. In reality, the companies that invested heavily in networking software (Cisco, Juniper, HP and a few others) might be the big winners if they figure out fast enough that they should morph into software-focused companies.

Cisco has clearly realized the winds are changing and started talking about inclusion of OpenFlow in NX-OS operating system. I would bet their first OpenFlow implementation won't be an OpenFlow-enabled Nexus switch.
