---
date: 2020-05-27 07:17:00+00:00
ha-cloud_tag: design
series_weight: 900
series:
- ha-cloud
tags:
- Azure
- cloud
- switching
title: Azure Networking 101
---
A few weeks ago I [described the basics of AWS networking](/2020/05/aws-networking-101/), now it's time to describe how different Azure is. 

As always, it would be best to watch my [Azure Networking webinar](https://www.ipspace.net/Microsoft_Azure_Networking) to get the details. This blog post is the abridged CliffsNotes version of the webinar (and [here](https://twitter.com/cloud_opinion/status/1261368141231173633?s=11)'s the reason I won't write a similar blog post for other public clouds ;).
<!--more-->
## High-Level Perspective

* Azure virtual networking is implemented with isolated Virtual Networks (**VNets**) that are always connected to outside world through Internet gateways.
* A VNet can also be connected to another VNet through VNet peering or VPN connection.
* You can use Virtual Network Gateway (VNG) to connect a VNet (or a bunch of peered VNets) to the rest of your network through VPN- or ExpressRoute (leased line) connections.
* VNet is limited to an **Azure region**.
* Every VNet has one or more **subnets**. Subnets can span **availability zones** (major difference with AWS), making it a bit harder to create [application swimlanes](https://my.ipspace.net/bin/list?id=AADesign#SOLUTIONS).

{{<figure src="/2020/05/Azure-VNet-Peering.png" caption="Some Azure VNet external connectivity options" >}}

## VNet Packet Forwarding Overview

Even though public cloud networking is just networking, it's usually different from what you'd expect, and Azure is definitely going into the _quite different_ direction.

* VNets supports unicast IPv4 and IPv6 packet forwarding. IP multicast is not supported.
* VM IP and MAC addresses are controlled by the orchestration system. 
* MAC address is passed to a VM as a (virtual) hardware parameter, 
* DHCP is used to pass IPv4 and IPv6 addresses configured in the orchestration system to the VMs.
* Packets are forwarded _exclusively based on IPv4/IPv6 addresses_. There is no L2 forwarding in Azure (major difference with AWS).
* Even though packets to- and from VM instances look like Ethernet packets, forwarding based on destination MAC address does not work.
* ARP requests return meaningless data - all hosts in the same subnet seem to have the same MAC address (MAC address of Azure virtual router).
* Packet forwarding is _based on the IP addresses configured in the orchestration system_ and can be influenced with per-subnet **route tables**
* Route tables are attached to individual subnets and can contain any prefix (including intra-VNet prefixes - major difference with AWS).
* The next hop in a route table entry could be _Internet_, _None_ (drop it), _Virtual Network Gateway_, _Virtual Appliance_ (an IP address of a VM - difference with AWS), or _VnetLocal_ (send directly to destination instance).
* Route tables can be populated through the orchestration system or via **external** (VPN or ExpressRoute) BGP sessions.

{{<figure src="/2020/05/Azure-Router.png" caption="VM NICs are connected straight to Azure router" >}}

Consequences:

* More-specific prefixes in route tables allow you to influence intra-VNet packet delivery. It's relatively easy (and confusing) to use route tables to set up service chaining to insert virtual network appliances in the packet forwarding path.
* Changing an IP or a MAC address in a VM usually results in a disconnected VM.
* First-hop routing protocols like HSRP or VRRP don't work. Changing a MAC address of a VM will just disconnect it.
* The only way to pass an IP address from one VM to another is through an orchestration system call. The usual GARP tricks don't work.
* Taking over an IP address of a failed instance probably changes packet forwarding behavior, but don't expect it to be fast. The only way to get decently-fast failover is to use an Azure load balancer.
* You cannot run a routing protocol between your instance and Azure router. You could either use orchestration system to modify the subnet route table(s) based on VM instance route tables, or run BGP with a VPN gateway in another VNet (see the corresponding section of [AWS Networking 101](/2020/05/aws-networking-101/) blog post for details).
* You could use a unicast-based routing protocol between VMs in the same subnet, but the routes derived from the routing protocol would be ignored by the Azure router, so packet forwarding wouldn't work anyway. The only way to enable routing between virtual appliances is to create a tunnel and run routing protocol and packet forwarding across that tunnel... but even there you'd hit a snag: Azure router forwards only TCP, UDP, and ICMP traffic, so you'd have to use a VXLAN tunnel.

{{<note note>}}Many thanks to [Remi Locherer](https://ngworx.ag/en/about-us/team/remi-locherer/) for pointing out the need for VXLAN tunnel.{{</note>}}

Need more details? I already told you [where to find them](https://www.ipspace.net/Microsoft_Azure_Networking), and we covered [numerous BYOA (Bring Your Own Appliance) designs](https://my.ipspace.net/bin/list?id=PubCloud&module=7#M9S20) in [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.

<!-- Disclosure: Companies presenting at CFD7 covered the event costs. Apart from the opportunity to ask questions, and getting to meet friends in a Zoom call I got nothing material or immaterial out of that event. -->