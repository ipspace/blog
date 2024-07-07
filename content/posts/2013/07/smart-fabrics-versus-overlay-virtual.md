---
date: 2013-07-15 07:46:00+02:00
tags:
- data center
- workshop
- cloud
- overlay networks
title: Smart Fabrics Versus Overlay Virtual Networks
url: /2013/07/smart-fabrics-versus-overlay-virtual/
---
With the recent plethora of overlay networking startups and Cisco Live [Dynamic Fabric Architecture](http://ccie31104.wordpress.com/2013/06/27/cisco-dfa-dynamic-fabic-architecture-aka-vinci/) announcements it's time to revisit a blog post I wrote a bit more than a year ago, [comparing virtual networks and voice technologies](/2012/05/virtual-networks-skype-analogy/).

They say a picture is worth a thousand words -- here are a few slides from my Interop 2013 [Overlay Virtual Networking Explained](http://www.interop.com/lasvegas/conference/networking.php?session_id=51) presentation.
<!--more-->
This is how most enterprise data centers provision virtual networks these days (if you're working for a cloud provider and still doing something similar, run away as fast as you can).

{{<figure src="http://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Offutt_Air_Force_Base_operator.jpg/315px-Offutt_Air_Force_Base_operator.jpg" caption="Good morning! To which VLAN would you like to connect today?">}}

The networking industry would love to keep the complexity (and related margins) in the network, keeping the edge (hypervisors) approximately as smart as the following device:

{{<figure src="http://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Telefon_BW_2012-02-18_13-44-32.JPG/305px-Telefon_BW_2012-02-18_13-44-32.JPG" caption="Which VLAN would you like to dial today?">}}

With the edge being mostly stupid (and 802.1Qbg playing the role of rotary dialing), you need loads of technologies in the network to compensate for the edge stupidity, just like the voice exchanges needed more and more complex technologies and protocols to establish voice circuits.

{{<figure src="/2013/07/s500-Networking+Industry+-+1.jpg" caption="Don't worry, we have a solution for all your problems">}}

The details have changed a bit (Cisco [seems to be embracing L3 forwarding at the ToR switches](http://ccie31104.wordpress.com/2013/06/27/cisco-dfa-dynamic-fabic-architecture-aka-vinci/)), but the architectural options haven't -- you have to have the complex stuff somewhere and it will be either in the end systems (hypervisors) or in the network.

{{<figure src="/2013/07/s500-Networking+Industry+-+2.jpg" caption="JBOT: Just a Bunch of Technologies">}}

We all know how the voice saga ended -- you [can't sell a mobile phone if it doesn't support Skype](/2013/04/464xlat-explained/), and while there are still plenty of loose ends when you have to connect the old and the new worlds, more or less everyone essentially gave up and started using VoIP for new deployments. Yes, it took us more than a decade to get there, and the road was bumpy, but I don't think you could persuade anyone to invest money in a PBX-with-SS7 startup these days.

{{<figure src="/2013/07/s500-Overlay+=+Skype.jpg">}}

We'll probably see the same game played out twenty years later in the virtual networking space (one can only hope the remains of the past won't hinder us as long as they are in the VoIP world) -- the established networking vendors selling us smarter and smarter exchanges (switches) and the virtualization vendors and startups selling us end-system solutions running on top of IP. It's easy to predict the final outcome; it's just the question of how long it will take to get there (and don't forget that Alcatel, Lucent and Nortel made plenty of money selling PBXes to legacy enterprises while Cisco and others tried to boost low VoIP adoption).

### More Blog Posts You Should Read

-   [Virtual networks: the Skype analogy](/2012/05/virtual-networks-skype-analogy/)
-   [Decouple virtual networking from the physical world](/2011/12/decouple-virtual-networking-from/)
-   [Which Virtual Networking technology should I use?](/2011/12/which-virtual-networking-technology/)
-   [Network virtualization and spaghetti wall](/2013/06/network-virtualization-and-spaghetti/)
-   [Network virtualization and ToR switches? Makes as much sense as IP-over-APPN](/2013/06/network-virtualization-at-tor-switches/)
-   [What is Network Virtualization?](/2013/06/what-is-network-virtualization/)
-   [Virtual networking is more than VMs and VLAN duct tape](/2012/04/virtual-networking-is-more-than-vms-and/)
