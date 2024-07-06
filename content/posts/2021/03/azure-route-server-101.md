---
date: 2021-03-10 07:50:00+00:00
sd-wan_tag: cloud
series:
- azure-rs
tags:
- Azure
- cloud
- SD-WAN
title: 'Azure Route Server: The Challenge'
---
Imagine you decided to deploy an SD-WAN (or DMVPN) network and make an Azure region one of the sites in the new network because you already deployed some workloads in that region and would like to replace the VPN connectivity you're using today with the new shiny expensive gadget.

Everyone told you to deploy two SD-WAN instances in the public cloud virtual network to be redundant, so this is what you deploy:

{{<figure src="/2021/03/azure-rs-initial-design.png">}}
<!--more-->
In the next moment, you'll likely experience an extremely painful collision with reality, shattering most PowerPoint fairy  tales. The gray box labeled *Azure VNet* is really a router (see [Azure Networking 101](/2020/05/azure-networking-101.html) for details), and a router won't forward packets unless it has *routes to the destinations* ([details](/2021/03/video-path-discovery-bridging-routing.html)).

{{<figure src="/2021/03/azure-rs-virtual-router.png">}}

To make your design work, you'd have to run a routing protocol between your SD-WAN appliances and the Azure virtual router (ignoring for the moment the *[we don't need routing protocols in SD-WAN](/2015/06/software-defined-wanwell-orchestrated.html)* stupidities)... but you can't. 

There are two ways to influence Azure VNet routing:

* You're using a VPN connection to the VNet, and run BGP over it;
* You configure static routes (called *user-defined routes*).

Cisco hyped the first solution a while ago: deploy two CSR instances in a separate virtual network, and establish VPN tunnels with the target virtual networks. [Clumsy, slow, and expensive](/2018/09/using-csr1000v-in-aws-instead-of.html). This time you can have all three.

An alternative solution would be to run a custom script on the virtual appliances. That custom script would monitor the IP routing table on the appliance and execute cloud orchestration API calls when the routing table changes. Cisco built that functionality into CSR, and I'm positive other vendors did something similar. I know people who wrote their own Python scripts to do the same.

Next challenge: a user-defined route cannot have more than one next hop per prefix. You cannot do load balancing between your Networking Virtual Appliance (NVA) instances. One of them has to be *primary*, the other one has to be *backup*, and you have to use orchestration system API calls to switch from primary to backup. Did I tell you [how slow Azure orchestration system is](/2019/06/how-microsoft-azure-orchestration.html)? A manually operated railroad switch is faster than that (including the time it takes the operator to run to the switch and move it).

There are ways around this challenge, and they are complex enough to guarantee perpetual job security. Deploy Azure Network Load Balancer configured just right, make sure forward and return paths match, use just the right amount of user-defined routes and it just might work. This is how [Microsoft envisions it to work](https://docs.microsoft.com/en-us/azure/load-balancer/load-balancer-ha-ports-overview). We truly don't need networking engineers when moving to public clouds, right?

{{<figure src="https://docs.microsoft.com/en-us/azure/load-balancer/media/load-balancer-ha-ports-overview/nvaha.png">}}

Recently launched [Azure Route Server](https://docs.microsoft.com/en-us/azure/route-server/overview) is a Microsoft-managed version of the NVA routing madness. It provides two BGP-speaking control-plane instances that your VM can peer with and send them routes to be installed in the Azure routing system. It doesn't use User Defined Routes (and UDR API calls) but looks like a [Virtual Hub](https://docs.microsoft.com/en-us/azure/virtual-wan/about-virtual-hub-routing). It clearly uses a different control-plane path into the bowels of Azure routing, allowing it to create multiple equal-cost routes to the same destination. There's also some hope it can update the Azure virtual router forwarding tables in near-real-time. 

Next time: Route Server behind the scenes.

### More Details

* Start with [Azure Networking 101](/2020/05/azure-networking-101.html) blog post.
* For more details, watch [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinar, which already includes [Azure Route Server video](https://my.ipspace.net/bin/get/AzureNet/4.4%20-%20Azure%20Route%20Server.mp4?doccode=AzureNet).
* We covered [BYOA (Bring Your Own Appliance) scenarios](https://my.ipspace.net/bin/list?id=PubCloud&module=7#M9S20) in [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.
* If you want to take Azure Route Server for a spin, you might want to start with [my test setup](https://github.com/ipspace/pubcloud/tree/master/Azure/route-server).