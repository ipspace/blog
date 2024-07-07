---
date: 2020-05-06 07:07:00+00:00
ha-cloud_tag: design
series_weight: 950
series:
- ha-cloud
tags:
- AWS
- cloud
- switching
title: AWS Networking 101
---
There was an obvious invisible elephant in the [virtual Cloud Field Day 7](https://techfieldday.com/event/cfd7/) (CFD7v) event I attended in late April 2020. Most everyone was talking about AWS, how their [stuff runs on AWS](https://techfieldday.com/appearance/vmware-cloud-on-aws-onboarding-dc-extension-and-cloud-migration-at-cloud-field-day-7/), how it [integrates with AWS](https://techfieldday.com/appearance/vmware-cloud-on-aws-horizon-7-vdi-kubernetes-aws-services-and-marketplace-at-cloud-field-day-7/), or how it will [help others leapfrog AWS](https://techfieldday.com/video/pensando-distributed-services-platforms-at-work/) (yeah, sure...).

Although you [REALLY SHOULD](https://tools.ietf.org/html/rfc6919) watch my [AWS Networking webinar](https://www.ipspace.net/Amazon_Web_Services_Networking) (or something equivalent) to understand what problems vendors like VMWare or Pensando are facing or solving, I'm pretty sure a lot of people think they can get away with CliffsNotes version of it, so here they are ;)
<!--more-->
## High-Level Perspective

* AWS virtual networking is implemented with isolated Virtual Private Clouds (**VPC**) that can be connected to outside world through Internet gateway, VPC-to-VPC peering, VPN gateways, Transit Gateways, or Direct Connect (leased lines) gateways.
* VPC is limited to an **AWS region**.
* Every VPC has one or more **subnets**. Each subnet is limited to an **AWS Availability zone**

{{<figure src="/2020/05/AWS-VPC-Peering.png" caption="Some AWS VPC external connectivity options" >}}

## VPC Packet Forwarding Overview

Even though AWS networking is just networking (as my [friend Nicola Arnoldi wrote a few days ago](https://toolr.io/2020/05/02/my-journey-into-cloud-networking/)), it's different enough from what you'd expect to make you feel like [Alice in Wonderland](/2019/10/master-alternate-public-cloud/).

A few speculations first:

* AWS is using an overlay virtual networking. We don't know what encapsulation protocol (GRE, VXLAN, ...) or what control plane they use... but we can be pretty sure it's not a centralized control plane or EVPN because those wouldn't scale to AWS size.
* We know they do VPC packet processing (checking, forwarding...) in ingress and egress hypervisors (source: [AWS re:Invent video](https://www.youtube.com/watch?v=8gc2DgBqo9U)).

Now for a few hard facts (if you don't trust me [go and test them yourself](/2018/10/figuring-out-aws-networking/)):

* AWS VPC supports unicast IPv4 and IPv6 packet forwarding.
* IPv4 multicast is supported on **Transit Gateway** (I'm guessing they're using transit gateway as a head-end replicator).
* VM IP and MAC addresses are controlled by the orchestration system. 
* MAC address is passed to a VM as a (virtual) hardware parameter, 
* DHCP is used to pass IPv4 and IPv6 addresses configured in the orchestration system to the VMs.
* Packets with destinations within the VPC address range are delivered directly from ingress vNIC (virtual Network Interface Card) to egress vNIC _based on the IP addresses configured in the orchestration system_
* Route tables are used to influence traffic forwarding toward external destinations. Next hops in route tables are AWS instances (VM, NIC, Internet gateway, VPN gateway, VPC peering...) not IP addresses.
* Even though the whole VPC behaves like a single forwarding domain (VRF), each subnet could have a different route table.
* A separate route table can be used for _ingress_ VPC traffic to implement service insertion... but it only applies to traffic _entering a VPC_ through an Internet- or VPN gateway.
* Route tables cannot contain prefixes within the VPC address range, the only exception being the _ingress_ route table attached to a gateway.
* Route tables can be populated through the orchestration system or via **external** (VPN or DirectConnect) BGP sessions.

{{<figure src="/2020/05/AWS-VPC-Route-Table.png" caption="Sample AWS VPC route table scenario" >}}

Consequences:

* There's no way you can influence intra-VPC packet delivery (apart from a gotcha explained below).
* Changing an IP or a MAC address in a VM usually results in a disconnected VM.
* First-hop routing protocols like HSRP or VRRP don't work. Changing a MAC address of a VM will just disconnect it.
* The only way to pass an IP address from one VM to another is through an orchestration system call. The usual GARP tricks don't work.
* Taking over an IP address of a failed instance doesn't change packet forwarding behavior. To do a proper HA failover you have to either change the route table (through orchestration system) or move an elastic NIC (the next hop) to another VM instance.
* You cannot run a routing protocol between your instance and AWS VPC router. You could either use orchestration system to modify the subnet route table(s) based on VM instance route tables, or run BGP with a VPN gateway. Cisco [used that approach with CSR1000v to implement hub-and-spoke VPC peering](/2018/09/using-csr1000v-in-aws-instead-of/) (and AWS took away that bonanza with Transit Gateway), and VMware [still has to do that to connect multiple VMware-on-AWS instances together](https://techfieldday.com/video/vmware-cloud-on-aws-network-connectivity-deep-dive/).

## It's Not That Simple

Even though the "common wisdom" is that AWS uses VPC router for packet forwarding, it really uses a mix of L2 and L3 forwarding:

* Within a subnet, packet forwarding is done on destination MAC address, but it is still [unicast routing not transparent bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH). Layer-2 tricks like BUM flooding **do not work**.
* Across subnets, packet forwarding is done on destination IP address.

Consequences:

* ARP caches contain meaningful MAC addresses (unlike Azure)
* You can use static routes with intra-subnet next hops _within VMs_ to change the _VM egress traffic flow_... but they have to be configured _inside the VM_ and only work if the next hop is in the same subnet.
* The moment you want to send the traffic to another subnet that trick stops working, AWS VPC router takes over, and the traffic is delivered directly to destination vNIC.
* You could use a routing protocol between VMs in the same subnet, and use routes derived from the routing protocol for packet forwarding **across the shared subnet**... as long as the routing protocol uses only unicast IP traffic. BGP FTW ;)

Need more details? I already told you [where to find them](https://www.ipspace.net/Amazon_Web_Services_Networking), and we covered [numerous BYOA (Bring Your Own Appliance) designs](https://my.ipspace.net/bin/list?id=PubCloud&module=7#M9S20) in [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.

<!-- Disclosure: Companies presenting at CFD7 covered the event costs. Apart from the opportunity to ask questions, and getting to meet friends in a Zoom call I got nothing material or immaterial out of that event. -->