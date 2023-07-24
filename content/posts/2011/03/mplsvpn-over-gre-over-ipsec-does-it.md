---
date: 2011-03-28 06:52:00.001000+02:00
dmvpn_tag: deploy
tags:
- DMVPN
- IPsec
- MPLS VPN
- GRE
title: 'MPLS/VPN-over-GRE-over-IPSec: Does It Really Work?'
url: /2011/03/mplsvpn-over-gre-over-ipsec-does-it.html
---
**Short answer**: yes, it does.

During the geeky chat we had just after we'd finished recording the [Data Center Fabric Packet Pushers](http://packetpushers.net/show-38-comparing-switch-fabrics-juniper-brocade-cisco/) podcast, Kurt (\@networkjanitor) Bales asked me whether the MPLS/VPN-over-DMVPN scenarios I'm describing in [Enterprise MPLS/VPN Deployment](http://www.ipspace.net/EnterpriseMPLS) webinar really work (they do seem a bit complex).

I always test the router configurations I use in my webinars and I usually share them with the attendees. [Enterprise MPLS/VPN Deployment](http://www.ipspace.net/EnterpriseMPLS) webinar includes a complete sets of router configurations covering 10 scenarios, including five different MPLS/VPN-over-DMVPN designs, so you can easily test them in your lab and verify that they do work. But what about a live deployment?
<!--more-->
To be honest, we don't have a large-scale MPLS/VPN-over-DMVPN live deployment yet (if you do, please share as much as you can in the comments), but Phase 1 DMVPN is not much different from MPLS/VPN-over-(P2P)GRE-over-IPSec \... and we've built a 1500+ site network using that solution for one of our customers.

It all started pretty innocently: the customer wanted to reduce costs by replacing their Frame Relay/ATM core with MPLS/VPN WAN services offered by the local service providers. They have to keep different departments using their network strictly separate and MPLS/VPN was the only scalable solution (you don't want to hear about the design I did for them 15+ years ago).

None of the service providers that they could use was able to provider Carrier's Carrier services; some of them were severely limited in their routing options (BGP? What BGP? How do you spell that?). As the customer wanted to be totally provider-independent, GRE tunnels were the only option -- if you use connected interfaces as tunnel sources, you don't have to exchange any routing information with the WAN connectivity provider. By building multiple parallel GRE infrastructures (one over each SP network), our customer got total WAN independence and is able to mix-and-match service providers on as-needed basis (they only have to make sure critical sites are connected to at least two providers for redundancy reasons). It's amazing how that ability helps you in the negotiation process.

Transporting sensitive data across IP infrastructure operated by the service providers was never an option, so we had to add IPsec to the mix, resulting in the stack mentioned in the article title.

Was it easy? Definitely not. Most of the problems were caused by the scale of the project: if you want to run IPsec at gigabit speeds, you need hardware encryption. When we were building the network, Catalyst 6500 was the only reasonable option \... but while it can easily handle MPLS/VPN or GRE or IPsec, it hiccups when you try to do all three things on a single packet. In the end, we had to deploy dual tier architecture similar to [this design](http://www.cisco.com/en/US/docs/solutions/Enterprise/WAN_and_MAN/DMVPN_2_Phase2.html#wp37393).

Device configuration was also a challenge: when adding a new site, you have to add bits-and-pieces of configuration to multiple boxes (including the firewalls I haven't even mentioned yet) and relying on manual configuration process would quickly result in a total mess. Solution: configuration builder, a custom-developed tool that accepts a few parameters describing a new site (or modified parameters of an already deployed site) and generates the configuration snippets that are then downloaded to the network devices.
