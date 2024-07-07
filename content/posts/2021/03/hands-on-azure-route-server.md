---
date: 2021-03-24 06:25:00+00:00
series:
- azure-rs
tags:
- cloud
- Azure
title: 'Hands-On: Azure Route Server'
---
**TL&DR**: Azure Route Server works as advertised. Setting it up is excruciatingly slow. You might want to start the process just before taking a long lunch break.

I decided to take [Azure Route Server](/2021/03/azure-route-server-behind-the-scenes/) for a ride. Simple setup, two Networking Virtual Appliance (NVA) instances running Quagga to advertise a single prefix (just to see how multipathing works).

Here's the diagram of what I set up:
<!--more-->
{{<figure src="/2021/03/azure-rs-test-setup.png">}}

In a nutshell:

* Three subnets -- NVA subnet, internal subnet (with a web server) and route server subnet
* A separate route table with disabled default route for the internal subnet
* Two NVA instances -- Ubuntu boxes running Quagga and advertising a single prefix (172.22.2.0/24)
* A route server instance peering with both NVA instances

**TL&DR**: It works. I didn't test the route propagation delays, you could [grab my setup](https://github.com/ipspace/pubcloud/tree/master/Azure/route-server) and run those tests if you feel so inclined.

Now for some more details

### It's Excruciatingly Slow

Decades ago I complained to our IT guy that logging into a Windows domain takes too long when I do it from home (spoiler alert: VPN-and-login chicken-and-egg problem). His response: "*Yeah, I know, I have the same problem. Just go fix yourself a sandwich in the meantime like I do.*"

Microsoft is still using the same mentality, but now I could throw together a decent lunch in the time it takes to deploy my setup. Here's how long just the route server operations took (actual times measured with **time az network routeserver** commands in brackets):

* Create route server: 16 minutes (15m58.042s / 15m48.928s)
* Create BGP peering: 1.5 minutes (1m22.357s / 1m22.756s / 1m23.296s)
* Delete BGP peering: 1.5 minutes (1m22.188s)
* Delete route server: 3 minutes (2m54.015s / 2m53.859s)

I did the tests over a weekend. I don't want to think about how long it would take on a Monday morning. 

Random thoughts:

* It's interesting how consistent those times are.
* Why does it take 80+ seconds to configure a BGP neighbor?
* Even more interesting: why is the BGP session established a few seconds after the command is executed, and what's going on for another minute?

### It's Just a Virtual Hub in Disguise

Looks like the route server is just a virtual hub deployed within a single VNet. Here's the JSON printout produced after the route server has been created. Please note the **id** attribute and the many Virtual Wan-related attributes.

```
{
  "addressPrefix": null,
  "allowBranchToBranchTraffic": false,
  "azureFirewall": null,
  "bgpConnections": null,
  "etag": "W/\"d3bdfc17-ff3f-46d3-aace-f4eb8b6843a7\"",
  "expressRouteGateway": null,
  "id": "/subscriptions/256508dc-15f0-46e9-81d8-31f3ea003be5/
    resourceGroups/rt/providers/Microsoft.Network/
    virtualHubs/RouteServer",
  "ipConfigurations": null,
  "location": "eastus",
  "name": "RouteServer",
  "p2SVpnGateway": null,
  "provisioningState": "Succeeded",
  "resourceGroup": "rt",
  "routeTable": {
    "routes": []
  },
  "routingState": "Provisioned",
  "securityPartnerProvider": null,
  "securityProviderName": null,
  "sku": "Standard",
  "tags": null,
  "type": "Microsoft.Network/virtualHubs",
  "virtualHubRouteTableV2S": [],
  "virtualRouterAsn": 65515,
  "virtualRouterIps": [
    "172.16.3.4",
    "172.16.3.5"
  ],
  "virtualWan": null,
  "vpnGateway": null
}
```

### BGP Table and Routing Table

Once the route server is up and running you can execute **show ip bgp** on it. Just kidding, it's **az network routeserver show**:

```
$ az network routeserver peering list-learned-routes \
>   --resource-group rt \
>   --routeserver RouteServer \
>   --name Web_BGP_Peering
{
  "RouteServiceRole_IN_0": [
    {
      "asPath": "65000",
      "localAddress": "172.16.3.4",
      "network": "172.22.2.0/24",
      "nextHop": "172.16.1.4",
      "origin": "EBgp",
      "sourcePeer": "172.16.1.4",
      "weight": 32768
    }
  ],
  "RouteServiceRole_IN_1": [
    {
      "asPath": "65000",
      "localAddress": "172.16.3.5",
      "network": "172.22.2.0/24",
      "nextHop": "172.16.1.4",
      "origin": "EBgp",
      "sourcePeer": "172.16.1.4",
      "weight": 32768
    }
  ],
  "value": null
}
```

Oh, and it takes 12 seconds to return the results.

Azure has no command to inspect the route table(s). The only related thing I found is *effective route table* of a VM NIC. Here's how the route table for a VM attached to *Internal* subnet looks like after the BGP sessions have been established (note two next hops for the 172.22.2.0/24 prefix):

```
$ az network nic show-effective-route-table \
   --resource-group RouteServer \
   --name BackendVMNic -o table
Source                 State    Address Prefix Next Hop Type          Next Hop IP
---------------------  -------  --------------  ---------------------  -------------
Default                Active   172.16.0.0/16  VnetLocal
VirtualNetworkGateway  Active   172.22.2.0/24  VirtualNetworkGateway  172.16.1.4
VirtualNetworkGateway  Active   172.22.2.0/24  VirtualNetworkGateway  172.16.1.5
Default                Invalid  0.0.0.0/0      Internet
Default                Active   10.0.0.0/8     None
Default                Active   100.64.0.0/10  None
Default                Active   192.168.0.0/16 None
Default                Active   25.33.80.0/20  None
Default                Active   25.41.3.0/25   None
User                   Active   0.0.0.0/0      None
```

Yeah, it takes another 12 seconds to get this printout.

Interestingly, the Route Server looks like a Virtual Network Gateway from the route table perspective, which also means that the routes received over BGP from NVA instances are propagated into all route tables. I looked at NVA VM NIC (default route table) and backend VM NIC (custom route table) and they both contained the same set of NVA -advertised prefixes.

I didn't test what happens when you disable BGP route propagation for a route table. It might even work.

### The Quirks

I know the whole thing is in preview, but nonetheless:

* Why do I have to use subnet ID instead of subnet name when creating the route server? The beauty of Azure API was the ability to use object names instead of the crazy AWS dance of "_let's get the object ID based on a tag that happens to be named **name**_"
* Why do I create a route server within a resource group, but it doesn't disappear when I destroy the resource group?
* Why is there a delete button next to a route server in Azure portal, but it doesn't do a thing?

To make things even more interesting: because the VMs that constitute a route server attach to a subnet, and because the route server attaches to route tables, removing a resource group fails without removing route tables and virtual networks. Not a problem, we're not charged for those, but keeping a running route server hurts.

The only way I found to remove a route server was to use **az network routeserver delete** command.

### Long Story Short

Azure Route Server is definitely an interesting concept, and I'm positive a lot of people focused on transporting enterprise \*\*\*\* into a public cloud will find it very homey... but like with all preview stuff, I wouldn't use it in production for at least a few months.

### More Details

You'll find more Azure networking goodies in the [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinar, which already includes [Azure Route Server video](https://my.ipspace.net/bin/get/AzureNet/4.4%20-%20Azure%20Route%20Server.mp4?doccode=AzureNet).
