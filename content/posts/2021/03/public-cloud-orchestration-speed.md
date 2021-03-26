---
title: "Relative Speed of Public Cloud Orchestration Systems"
date: 2021-03-25 07:15:00
tags: [ cloud, Azure, AWS ]
---
When I was [complaining about the speed (or lack thereof) of Azure orchestration system](https://twitter.com/ioshints/status/1371731265024618499), someone replied "*I tried to do $somethingComplicated on AWS and it also took forever*"

Following the "*opinions are great, data is better*" mantra (as opposed to "*never let facts get in the way of a good story*" supposedly practiced by some podcasters), I decided to do a short experiment: create a very similar environment with Azure and AWS.

I took simple Terraform deployment configuration for [AWS](https://github.com/ipspace/pubcloud/tree/master/Deployment/AWS/Terraform) and [Azure](https://github.com/ipspace/pubcloud/tree/master/Deployment/Azure/Terraform). Both included a virtual network, two subnets, a route table, a packet filter, and a VM with public IP address. Here are the observed times:
<!--more-->
{{<cc>}}AWS response times by Terraform resource type (creation/destruction){{</cc>}}
```
aws_vpc: 18s/1s
aws_route_table: 2s/2s
aws_subnet: 2s/1s
aws_internet_gateway: 3s/24s
aws_route: 2s/0s
aws_security_group: 5s/1s
aws_subnet: 14s
ec2instance: 37s/32s
```

{{<cc>}}Azure response times by Terraform resource type (creation/destruction){{</cc>}}
```
azurerm_resource_group: 1s/46s
azurerm_route_table: 22s/11s
azurerm_virtual_network: 35s/11s
azurerm_network_security_group: 35s/11s
azurerm_subnet: 4-7s/10-11s
azurerm_subnet_route_table_association: 4s
azurerm_public_ip: 1m0s/1m40s
azurerm_network_interface: 1s/21s
azurerm_virtual_machine.tf_vm: 21s/1m42s
```

Azure is markedly slower (apart from VM creation), and the real showstopper seems to be the public IP address. Admittedly I was looking for a ballpark figure and did a single **apply**/**destroy** cycle on each public cloud; if you feel like conducting a proper experiment spread across multiple times-of-day in multiple availability zones I'd love to see your results.

What worries me way more than the response time difference is the extreme variability of Azure response times. This is what I've observed when setting up and tearing down Azure Virtual Hub components (which I did do multiple times on several days in several regions):

{{<long-quote>}}
* 15 – 25 minutes to create a virtual hub
* 3 – 15 minutes to create a virtual network connection
* 2.5 – 10 minutes to modify VNet connection route propagation parameters
* 5 – 15 minutes to destroy a virtual network connection
{{</long-quote>}}

{{<note>}}Supposedly it takes that long to create an Azure Virtual Hub, Virtual Network Gateway, or Route Server because they're running on Windows servers. Maybe it's time for Azure development teams to stop singing "*leveraging the investment*" and "*doing more with less*" incantations and use a faster platform?{{</note>}}

To make matters even worse, the large variance in response times was observed *on parallel requests made by Terraform in the same Azure region*. One virtual network connection would be created or destroyed in a few minutes, the other one (started at the same time) would take more than 10 minutes. Worst-case scenario I've heard of: 17 minutes to change an entry in a route table.

Does the difference matter? It does to me when I'm trying to figure out how things work. It might not matter if you're making changes to your public cloud infrastructure every third blue moon... or you might care a lot if you plan to use Azure REST API for real-time dynamic modifications of your infrastructure like changing the next hop of user-defined route. 

Interestingly, I got mixed messages on that last use case, from someone claiming it works great, to someone else saying he'd rather rely on the complex load balancing architecture than Azure API response times. Any further real-life experience would be highly appreciated.

### History of Changes

2021-03-25
: Added a sample real-life UDR worst-case scenario
