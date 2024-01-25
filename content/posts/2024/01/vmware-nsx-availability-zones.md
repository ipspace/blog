---
title: "Availability Zones in VMware NSX-Based Cloud"
date: 2024-01-25 09:48:00+0100
tags: [ NSX, design ]
---
One of the ipSpace.net subscribers sent me this question:

>  How could I use NSX to create a cloud-like software network layer enabling a VMware enterprise to create a public cloud-like availability zone concept within a data center (something like Oracle Cloud does)?

That's easy: stop believing in [VMware marketing shenanigans](https://blog.ipspace.net/2020/09/disaster-recovery-vendor-marketing.html).
<!--more-->
An [availability zone](https://blog.ipspace.net/2021/02/public-cloud-regions-availability-zones.html) should be an independent failure domain and as isolated as possible from other availability zones (but less so than regions). What that means depends on the [network virtualization implementation details](https://blog.ipspace.net/2021/02/vpc-subnets-aws-azure-gcp.html), but no sane public cloud supports bridging or stretched VLANs.

**Rule#1**: [A VLAN is a single failure domain](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html). Keep VLANs within a single availability zone. Stretching a VLAN will not create a disaster recovery solution; it will [create a single failure domain](https://blog.ipspace.net/2019/12/disaster-recover-and-failure-domains.html) and [potentially a disaster](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html).

**Next question:** How will you connect subnets from different availability zones? We're entering a gray area full of "it depends" twisting rabbit trails, starting with "_do we want independent data-plane failure domains, or do we also want independent control-plane failure domains?_"

If you're okay with a shared control plane running across all availability zones, do what all public cloud providers do and deploy NSX Tier-1 gateways (distributed routers). If you want independent network virtualization control planes, you'll have to get the traffic out to the physical network and deal with VRFs (or EVPN) in the physical network. However, the physical network is a loosely coupled collection of autonomous control planes, so you just pushed the problem around (proving RFC 1925 Rule 6). I would probably stay with the distributed routers forwarding traffic between availability zones and rely on the physical network to transport the customer traffic between regions.

An NSX instance is also a single management plane[^NC], which makes everything managed by that instance a single management-plane failure domain. That's good enough for public cloud providers; it might be good enough for your needs *assuming you go one step further and create multiple regions*. A single NSX management instance controlling your mission-critical workload is like running your servers in multiple availability zones in the AWS US-East-1 region. We know [how well that ends](https://aws.amazon.com/message/65648/).

Finally, remember that the network is only one of the components of a cloud infrastructure. At the very minimum, you also need the compute and storage infrastructure, and stretching a VSAN cluster across availability zones (or even across locations) is as bad as stretching VLANs.

[^NC]: Don't tell me it has three nodes in a cluster. High-availability clusters can cope with failures of underlying infrastructure but rarely with internal data corruption.