---
title: "Renumbering Public Cloud Address Space"
date: 2020-11-05 07:47:00
tags: [ cloud, Azure ]
---
Got this question from one of the networking engineers "blessed" with [rampant clueless-rush-to-the-cloud](/2020/10/dont-lift-and-shift-into-cloud/).

> I plan to peer multiple VNet from different regions. The problem is that there is not any consistent deployment in regards to the private IP subnets used on each VNet to the point I found several of them using public IP blocks as private IP ranges.  As far as I recall, in Azure we can’t re-ip the VNets as the resource will be deleted so I don’t see any other option than use NAT from offending VNet subnets to use my internal RFC1918 IPv4 range. Do you have a better idea?

The way I understand Azure, while you COULD have any address range configured as VNet CIDR block, you MUST have non-overlapping address ranges for VNet peering.
<!--more-->
{{<note info>}}You could have overlapping address ranges in peered AWS VPCs. That doesn't make it a good idea though.{{</note>}}

Furthermore, Azure built-in NAT only works on Internet connections, so you’d have to go to public WAN and back to hit NAT. Obviously you could use NAT appliance within a VNet, and send traffic through that appliance, but even then you wouldn’t solve the challenges of VNet peering (see above) - you’d have to send the traffic from offending VNet through an IPsec tunnel to a VPN gateway in the hub VNet of the peered VNet conglomerate.

In any case, I don’t think it’s a problem worth solving. It’s high time to drop out of MacGyver mode, and tell the teams that set up Azure subscriptions without any coordinated planning to renumber or stay on their own. Set the rules they have to conform to if they want to be part of supported infrastructure, and if they are unable or unwilling to comply, wish them luck running their own stuff. 

Of course there's a better way to do it: it’s easy(er) to renumber if you do things right and use infrastructure-as-code tools. That's why I keep telling people who are willing to listen not to use GUI to provision their public cloud environments.

In case you're interested in the IaC idea: we [covered it extensively](https://my.ipspace.net/bin/list?id=PubCloud&module=2) in our [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course, and our [public cloud examples](https://github.com/ipspace/pubcloud) GitHub repository contains Ansible, Terraform, CloudFormation and Resource Manager templates for typical AWS and Azure networking deployments.
