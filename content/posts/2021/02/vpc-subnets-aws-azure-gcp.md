---
date: 2021-02-23 07:52:00+00:00
high-availability_tag: cloud
series:
- cloud-subnets
tags:
- cloud
- IP routing
- high availability
title: Virtual Networks and Subnets in AWS, Azure, and GCP
---
Now that we know what [regions and availability zones are](/2021/02/public-cloud-regions-availability-zones.html), let's go back to Daniel Dib's question:

> As I understand it, subnets in Azure span availability zones. Do you see any drawback to this? Does subnet matter if your VMs are in different AZs?

Wait, what? A subnet is stretched across multiple failure domains? Didn't Ivan claim that's [ridiculous](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html)?

**TL&DR**: What I claimed was that *a single layer-2 network is a single failure domain*. Things are a bit more complex in public clouds. Keep reading and you'll find out why.
<!--more-->
Each humongous public cloud provider has a different approach to virtual networks and subnets, and how they map into availability zones and regions. Let's start with their differences.

### Amazon Web Services

AWS Virtual Private Cloud (VRF if you wish) is limited to a single region. It can have many subnets, each subnet limited to a single availability zone. AWS is obviously enforcing very strict fault isolation.

{{<figure src="aws-vpc-subnet.png" caption="VPCs and subnets in AWS">}}

Traffic between subnets within a region flows without limitations (apart from security rules), but of course [AWS charges you for the privilege](https://www.lastweekinaws.com/blog/aws-cross-az-data-transfer-costs-more-than-aws-says). To build a network across multiple regions you have to use VPC peering or a Transit Gateway.

AWS uses an [interesting mix of L2- and L3-forwarding within a subnet](https://blog.ipspace.net/2020/05/aws-networking-101.html), but it's deterministic and unicast, so no harm done, and it's all within a single failure domain anyway.

### Azure

Like AWS VPCs, Azure Virtual Networks (VNet) are limited to a single region, but each subnet spans all availability zones. 

{{<figure src="azure-vpc-subnet.png" caption="VPCs and subnets in Azure">}}

It looks like the fault isolation just went out the window, but it's not as bad as it looks. Layer-2 segments in Azure are extremely short -- they exist only between a virtual machine and the adjacent hypervisor virtual switch. Each virtual switch is a full-blown IP router using host routes to reach other hosts within the same subnet.

{{<figure src="azure-packet-forwarding.png" caption="Azure packet forwarding behind the scenes">}}

Considering intra-subnet routing, it really makes no difference from the fault isolation perspective whether a subnet spans one or multiple availability zones, but it does have an impact on the ease of application deployment -- more about that in the next installment. 

With end-to-end IP routing, Azure subnets became a configuration convenience; all VMs connected to the same subnet share the same *Network Security Group* and the same *User-Defined Route Table* (in reality these two objects get inserted between a VM and the adjacent virtual switch).

### Google Cloud Platform

GCP went one step further. VPCs are *global resources* (spanning multiple regions), while subnets are *regional resources* (spanning availability zones). IIRC from the last time I studied GCP while preparing for a customer workshop they also do pure IP routing within a VPC, but this is approximately as far as I could be bothered with GCP today (their documentation is great, but I [have my reservations](https://blog.ipspace.net/2020/08/selecting-public-cloud.html), and [I'm not the only one](https://medium.com/@steve.yegge/dear-google-cloud-your-deprecation-policy-is-killing-you-ee7525dc05dc)).

{{<figure src="gcp-vpc-subnet.png" caption="GCP VPCs and subnets">}}

### More to Explore

If you need more details about AWS and Azure networking you'll find them in these webinars:

* [AWS Networking](https://www.ipspace.net/Amazon_Web_Services_Networking)
* [Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking)
