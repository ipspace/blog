---
anycast_tag: use
date: 2013-06-10 07:02:00+02:00
high-availability_tag: external
series:
- anycast
tags:
- data center
- overlay networks
- virtualization
- high availability
title: Dynamic Routing with Virtual Appliances
url: /2013/06/dynamic-routing-with-virtual-appliances/
---
Meeting Brad Hedlund in person was definitely one of the highlights of my Interop 2013 week. We had an awesome conversation and quickly realized how closely aligned our views of [VLANs](/2013/04/vlans-are-wrong-abstraction-for-virtual/), [overlay networks](/2011/12/decouple-virtual-networking-from/) and [virtual appliances](/2013/05/simplify-your-disaster-recovery-with/) are.

Not surprisingly, Brad quickly improved my ideas with a radical proposal: running BGP between the virtual and the physical world.
<!--more-->
Let's revisit the application stack I used in the [disaster recovery with virtual appliances](/2013/05/simplify-your-disaster-recovery-with/) post. One of the points connecting the virtual application stack with the physical world was the outside IP address of the firewall (or load balancer if you're using bump-in-the-wire firewall).

{{<figure src="/2013/06/s1600-VA_Interaction_Points.png" caption="Virtual appliance interaction points">}}

Now imagine inserting a router between the firewall and the outside world, allocating a prefix to the application stack (it could be a single /32 IPv4 prefix, a single /64 IPv6 prefix, or something larger), and advertising that prefix from the virtual router to the physical world via BGP.

{{<figure src="/2013/06/s1600-VA_External_BGP.png" caption="Virtual appliance running BGP with the adjacent switch">}}

{{<note info>}}Before you start writing a comment complaining how three virtual appliances in sequence reduce performance and introduce unnecessary network traversals: as most virtual appliances these days use Linux, it isn't that hard to add a few more daemons to the same VM -- the approach used by VMware NSX-T. The three boxes in the picture could be a single VM if you prefer performance optimization over flexibility.{{</note>}}

You could easily preconfigure the ToR switches (or core switches -- depending on your data center design) with BGP peer templates, allowing them to accept BGP connections from a range of directly connected IP addresses, assign outside IP address to the virtual routers via DHCP (potentially running on the same ToR switch), and use MD5 authentication to provide some baseline security.

An even better solution would be a central BGP route server where you could do some serious authentication and route filtering. Also, you could [anycast](/series/anycast/) the same IP address in multiple data centers, making it easier for the edge virtual router to find its BGP neighbor even after the whole application stack has been migrated to a different location.

This twist on the original idea makes the virtual application stack totally portable between compatible infrastructures. It doesn't matter what VLAN the target data center is using, it doesn't matter what IP subnet is configured on that VLAN, when you move the application stack the client-facing router gets an outside address, establishes a BGP session with someone, and starts advertising the public-facing address range of the application.

### More information

I described the basics of overlay networks in [Cloud Computing Networking](http://www.ipspace.net/Cloud_Computing_Networking) and [Overlay Virtual Networking](https://www.ipspace.net/Overlay_Virtual_Networking)_ webinars.

For vendor-specific information, please watch [VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) and [Cisco ACI Deep Dive](https://www.ipspace.net/Cisco_ACI_Deep_Dive) webinars.

### Revision History

2023-02-01
: * Removed a few obsolete mentions
  * Added links to webinars created after the original publication date
  * Added an NSX-T reference
