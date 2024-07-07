---
cdate: 2022-07-09
comment: 'Numerous marketers and SDN/OpenFlow pundits keep repeating how they’ll save
  the (networking) world and bring true nirvana to the network operations with their
  flashy new gadgets. Nothing can be further from the truth because we cannot get
  rid of the legacy permeating the whole TCP/IP stack, as I explained in this post
  written in July 2013.


  Note: Joe was obliquely touting the benefits of what became Cisco ACI versus the
  "more traditional" implementations like [VMware NSX](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive).
  While [Cisco ACI does have an interesting architecture](https://www.ipspace.net/Cisco_ACI_Deep_Dive),
  that architecture is too complex for many deployments, and ACI often gets used as
  a centralized VLAN provisioning tool.

  '
date: 2013-07-23 07:52:00+02:00
sdn_hype_tag: clueless
series:
- sdn_hype
tags:
- data center
- overlay networks
- virtualization
title: Where’s the Revolutionary Networking Innovation?
url: /2013/07/wheres-revolutionary-networking/
---
In his [recent blog post](https://web.archive.org/web/20161224170304/http://www.definethecloud.net/its-our-time-down-here-underlays/) [Joe Onisick](http://www.linkedin.com/in/jonisick) wrote "*What network virtualization doesn't provide, in any form, is a change to the model we use to deploy networks and support applications. \[\...\] All of the same broken or misused methodologies are carried forward. \[\...\] Faithful replication of today's networking challenges as virtual machines with encapsulation tunnels doesn't move the bar for deploying applications.*"
<!--more-->
Much as I agree with him, we can't change much on planet Earth due to the fact that VMs use Ethernet NICs (so we need some form of VLANs to cater to [infinite creativity of some people](/2012/02/microsoft-network-load-balancing-behind/)), IP addresses (so we need [L3 forwarding](/2010/07/bridging-and-routing-is-there/)), [broken TCP stack](/2009/08/what-went-wrong-tcpip-lacks-session/) (requiring load balancers to fix it), and obviously can't be relied upon to be sufficiently protected (so we need external firewalls). Furthermore, unless we manage to [stop shifting the problems around](/2012/07/virtualized-squashed-complexity-sausage/), the [networking as a whole won't get simpler](/2013/04/this-is-what-makes-networking-so-complex/).

What overlay network virtualization does bring us is a [decoupling](/2011/12/decouple-virtual-networking-from/) that makes [physical infrastructure less complex](/2013/07/smart-fabrics-versus-overlay-virtual/) so it can focus on packet forwarding instead of zillions of customer-specific features preferably baked in custom ASICs. Obviously that's not a good thing for everyone out there.

It could also be that the company Joe is currently working for[^JO] has some truly revolutionary ideas (or so their web page claims), and I would love to be proven wrong, but the [first glimpses weren't exactly encouraging](https://www.networkcomputing.com/data-centers/cisco-insieme-itll-do-stuff-we-wont-tell-you).

[^JO]: Joe was working in Insieme marketing at that time. Insieme was acquired by Cisco, and their product became the first version of Cisco ACI.
