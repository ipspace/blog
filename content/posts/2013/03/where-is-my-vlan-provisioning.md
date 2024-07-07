---
date: 2013-03-28 06:56:00+01:00
tags:
- data center
- LAN
- virtualization
title: Where Is my VLAN Provisioning Application?
url: /2013/03/where-is-my-vlan-provisioning/
---
Yesterday I wrote that [it's pretty easy to develop a VLAN provisioning application](/2013/03/what-did-you-do-to-get-rid-of-manual/) (integrating it with vCenter or System Center earns you bonus points, but even that's not too hard), so based on the frequent "I hate using CLI to provision VLANs" rants you might wonder where all the startups developing those applications are. Simple answer: there's no [reasonably-sized market](http://telecomoccasionally.wordpress.com/2012/02/20/mid-market-innovators-dilemma/). How would I know that? We've been there.
<!--more-->
When I was working at a system integrator we wrote numerous network configuration/provisioning applications, starting with provisioning of Internet customers on our dial-up servers and routers in 1993 to MPLS/VPN provisioning for a major MPLS/VPN-over-IPsec-over-IP-over-MPLS/VPN customer. Needless to say, we also had to fully automate our remote labs and cloud services (and both required frequent reconfiguration of numerous networking elements).

Could we productize those applications? Hardly. In most cases, we had to tailor the provisioning application to the actual hardware (we've learned the hard way how to abstract that part in our remote labs) and network topology -- many networking architects and designers proudly create one unique network after another, each one of them a masterpiece of architecture and engineering, never considering the impact of their efforts on other elements in the food chain.

![](/2013/03/s480-UniqueNotUseful.jpg)

If you've ever been involved in an ERP system rollout, you probably know the tradeoffs you'd face when choosing a data center (or cloud) orchestration/provisioning platform. If you buy a mid-range ERP platform (Navision), you're forced to adapt your business to its limitations, or you could choose a high-end platform (SAP) and be forever joined at the hip to an army of consultants constantly tweaking SAP to the nuances of your business.

The situation is no different in data center (or service provider or cloud) environment -- you could easily find a framework platform that will cost you an arm and a leg (prices in 6-to-7 figure range) not including the customization and adaptation services, and large ISPs and cloud providers invested in developing their own solutions. You have to be big enough to justify spending that much money just to get a provisioning platform; most of us are not in that category.

On the other hand, it would be hard to find a SolarWinds of VLAN provisioning. Why? We're not building data centers with standard architecture and components that would require minimum customization, and it's close to impossible to write a low-priced application that will work well with millions of totally unique networks. I don't understand why anyone expects SDN to change that, but please do feel free to write a comment if you disagree.
