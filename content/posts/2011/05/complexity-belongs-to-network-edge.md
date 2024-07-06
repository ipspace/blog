---
date: 2011-05-09 07:13:00+02:00
tags:
- data center
- virtualization
title: Complexity Belongs to the Network Edge
url: /2011/05/complexity-belongs-to-network-edge.html
---
Whenever I write about vCloud Director Networking Infrastructure (vCDNI), be it a [rant](/2010/11/vcloud-director-hand-network-over-to.html) or a [more technical post](/2011/04/vcloud-director-networking.html), I get comments along the lines of "What are the network guys going to do once the infrastructure has been provisioned? With vCDNI there is no need to keep network admins full time."

Once we have a scalable solution that will be able to stand on its own in a large data center, most smart network admins will be more than happy to get away from provisioning VLANs and focus on other problems. After all, most companies have other networking problems beyond data center switching.
<!--more-->
{{<note update>}}More than a decade after the blog post has been written, we're still provisioning VLANs to support VMware ESXi hosts even though we could have used overlay networks with VMware NSX for years. It turns out that everyone loves to push the problems down the stack.{{</note>}}

As for disappearing work, we've seen the demise of DECnet, IPX, SNA, DLSw and multi-protocol networks (which are coming back with IPv6) without our jobs getting any simpler, so I'm not worried about the jobless network admin. I am worried, however, about the stability of the networks we are building, and that's the only reason I'm ranting about the emerging flat-earth architectures.

{{<figure src="http://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Universum.jpg/600px-Universum.jpg" caption="Middle Ages view of flat earth. Not much has changed in the meantime (via [Wikimedia Commons](http://commons.wikimedia.org/wiki/File:Universum.jpg))">}}

In 2002 IETF published an interesting RFC: [Some Internet Architectural Guidelines and Philosophy (RFC 3439)](http://tools.ietf.org/html/rfc3439) that should be a mandatory reading for anyone claiming to be an architect of solutions that involve networking (you know who you are). In the *End-to-End Argument and Simplicity* section the RFC clearly states: "In short, the complexity of the Internet belongs at the edges, and the IP layer of the Internet should remain as simple as possible."

We should use the same approach when dealing with virtualized networking: the complexity belongs to the edges (hypervisor switches) with the intervening network providing the minimum set of required services. I don't care if the networking infrastructure uses layer-2 (MAC) addresses or layer-3 (IP) addresses as long as it scales. [Bridging does not scale](/2010/07/bridging-and-routing-is-there.html) as it emulates a logical thick coax cable. Either get rid of most bridging properties (like packet flooding) and implement proper MAC-address-based routing without flooding, or use IP as the transport. I truly don't care.

Reading RFC 3439 a bit further, the next paragraphs explain the [*Non-Linearity and Network Complexity*](http://tools.ietf.org/html/rfc3439#section-2.2). To quote the RFC: "_In particular, the largest networks exhibit, both in theory and in practice, architecture, design, and engineering non-linearities which are not exhibited at smaller scale._" Allow me to paraphrase this for some vendors out there: "_just because it works in your lab does not mean it will work at Amazon or Google scale._"

The current state of affairs is just the opposite of what a reasonable architecture would be: VMware has a [barebones layer-2 switch](/2019/10/the-cost-of-disruptiveness-and.html) (although it does have [a few interesting features](/2010/11/vmware-virtual-switch-no-need-for-stp.html)) with [another non-scalable layer](/2011/04/vcloud-director-networking.html) (vCDNI) on top of (or below) it. The networking vendors are inventing all sorts of kludges of increasing complexity to cope with that, from VN-Link/port extenders and EVB/VEPA to large-scale L2 solutions like TRILL, Fabric Path, VCS Fabric or 802.1aq, and L2 data center interconnects based on VPLS, OTV or BGP MAC VPN.

{{<note update>}}In the meantime, [all the proprietary fabric solutions have died](/2022/05/cisco-fabric-path-and-friends.html), and networking vendors are pushing another overly-complex architecture: EVPN control plane with VXLAN encapsulation. VMware still makes their lives easy by insisting on having the same MAC/IP addresses on all server uplinks.{{</note>}}

I don't expect the situation to change on its own. VMware knows server virtualization is just a stepping stone and is already [investing in PaaS solutions](http://www.cloudfoundry.com/); the networking vendors are more than happy to sell you all the extra proprietary features you need just because VMware never implemented a more scalable solution, increasing their revenues and lock-in. It almost feels like the more "network is in my way" complaints we hear, the happier everyone is: virtualization vendors because the blame is landing somewhere else, the networking industry because these complaints give them a door opener to sell their next-generation magic (this time using a term borrowed from the textile industry).

Imagine for a second that VMware or Citrix would actually implement a virtualized networking solution using IP transport between hypervisor hosts. The need for new fancy boxes supporting TRILL or 802.1aq would be gone, all you would need in your data center would be high-speed simple L2/L3 switches. Clearly not a rosy scenario for the flat-fabric-promoting networking vendors, is it?

{{<note update>}}VMware did just that with VMware NSX, and set the license prices so high that it's rarely used. Even worse, VMware NSX requires all server uplinks to be in the same VLAN, so it [cannot run over a simple layer-3-only data center network](/2020/02/do-we-need-complex-data-center-switches.html).{{</note>}}

Is there anything you can do? Probably not much, but at least you can try. Sit down with the virtualization engineers, discuss the challenges and figure out the best way to solve problems both teams are facing. Engage the application teams. If you can persuade them to start writing scale-out applications that can use proper load balancing, most of the issues bothering you will disappear on their own: there will be no need for large stretched VLANs and no need for L2 data center interconnects. After all, if you have a scale-out application behind a load balancer, nobody cares if you have to shut down a VM and start it in a new IP subnet.

### Revision History

2022-11-12
: Added a few notes on virtual network evolution between 2011 and 2022.

