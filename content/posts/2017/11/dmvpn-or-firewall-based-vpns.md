---
date: 2017-11-08 10:27:00+01:00
dmvpn_tag: alternative
tags:
- design
- firewall
- DMVPN
- VPN
title: DMVPN or Firewall-Based VPNs?
url: /2017/11/dmvpn-or-firewall-based-vpns.html
---
One of my readers sent me this question:

> I\'m having an internal debate whether to use firewall-based VPNs or DMVPN to connect several sites if our MPLS connection goes down. How would you handle it? Do you have specific courses answering this question?

As always, the correct answer is *it depends*, in this case on:
<!--more-->
**How much spoke-to-spoke traffic you have** and whether you're OK with that traffic passing through the central site.

Traditional IPsec-based VPN implementations use point-to-point tunnels to implement a hub-and-spoke connectivity model in which all the traffic between remote sites (spokes) passes through a central site (hub).

Most MPLS/VPN and DMVPN implementations use any-to-any connectivity model in which any two spokes can communicate directly without the traffic passing through the hub node.

{{<note info>}}Some firewall vendors support ADVPN, a standard alternative to DMVPN. However, while the point-to-point IPsec VPNs are ubiquitous, the ADVPN implementations are not so common. Instead of choosing between firewall-based VPN or DMVPN, you have to choose between many-vendor point-to-point or one-or-few-vendor multipoint solution.{{</note>}}

Migrating from any-to-any connectivity to hub-and-spoke connectivity introduces additional latency, and increases the bandwidth requirements of the central site -- the firewall terminating point-to-point hub-to-spoke tunnels has to handle all spoke-to-spoke traffic.

**How easy it is to set up additional VPN tunnels** and how many spokes you have.

Some VPN implementations require additional configuration for every spoke. Other implementations support dynamic VPN tunnels created from configuration templates.

If you have to configure each VPN tunnel on your firewall and have a significant number of spokes, I'd highly recommend automating the firewall configuration management by creating VPN configurations from a VPN data model and configuration templates. Numerous students of my [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course decide to do that as one of their homework assignments.

{{<note>}}Of course it's always possible to use a [single-pane-of-broken-glass](http://etherealmind.com/poster-make-single-pane-glass/) solution from your preferred \$vendor.{{</note>}}

On the other hand, you can make DMVPN configuration almost spoke-neutral -- adding a new spoke does not require any changes on the hub routers.

**Dynamic load balancing**. It's reasonably easy to perform application-based policy-based routing (assuming your device supports it) if you terminate VPN tunnels and MPLS connections on the same devices (regardless of whether you call them routers or firewalls), and if you believe in IWAN you could get some sort of centralized policy with PfRv3 (or through an orchestration system like [Gluware](http://gluware.com/)). Getting the same results in a firewall(VPN)+router(MPLS) combo is interestingly complex.

{{<note>}}This problem can also be solved with yet another layer of abstraction called [SD-WAN](https://blog.ipspace.net/2015/06/software-defined-wanwell-orchestrated.html).{{</note>}}

### The Relevant Webinars

Some of the basic differences between various VPN solutions are covered in the *[Choosing the optimal VPN service](http://www.ipspace.net/Choose_the_optimal_VPN_service)* webinar, and DMVPN is covered in great details in various [DMVPN webinars](http://www.ipspace.net/DMVPN3).

If you want to become fluent in network automation, there's probably no better solution than the [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course. If you want to start small go for the [Ansible for Networking Engineers](http://www.ipspace.net/Ansible_for_Networking_Engineers) online course.
