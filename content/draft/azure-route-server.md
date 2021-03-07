---
title: "X"
date: 2021-03-06 16:25:00
draft: true
tags:
---


```
real    15m58.042s
user    0m1.239s
sys     0m0.136s
```

Timing:
* Create route server: 16 minutes (15m58.042s / 15m48.928s)
* Create peering: 1.5 minutes (1m22.357s / 1m22.756s / 1m23.296s)
* Delete peering: 1.5 minutes (1m22.188s)
* Delete route server: 3 minutes (2m54.015s / 2m53.859s)
* Show NIC effective route table: 12 seconds (0m12.370s)

{
  "addressPrefix": null,
  "allowBranchToBranchTraffic": false,
  "azureFirewall": null,
  "bgpConnections": null,
  "etag": "W/\"d3bdfc17-ff3f-46d3-aace-f4eb8b6843a7\"",
  "expressRouteGateway": null,
  "id": "/subscriptions/256508dc-15f0-46e9-81d8-31f3ea003be5/resourceGroups/rt/providers/Microsoft.Network/virtualHubs/RouteServer",
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

$ time az network routeserver peering list-learned-routes \
>   --resource-group rt \
>   --routeserver RouteServer \
>   --name Web_BGP_Peering
{- Finished ..
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

real    0m12.045s
user    0m0.782s
sys     0m0.041s

```
$ az network nic show-effective-route-table \
  --resource-group rt --name DBVMNic -o table
Source                 State    Address Prefix    Next Hop Type          Next Hop IP
---------------------  -------  ----------------  ---------------------  -------------
Default                Active   172.16.0.0/16     VnetLocal
VirtualNetworkGateway  Active   172.22.2.0/24     VirtualNetworkGateway  172.16.1.4
Default                Invalid  0.0.0.0/0         Internet
Default                Active   10.0.0.0/8        None
Default                Active   100.64.0.0/10     None
Default                Active   192.168.0.0/16    None
Default                Active   25.33.80.0/20     None
Default                Active   25.41.3.0/25      None
User                   Active   0.0.0.0/0         None
```

```
$ az network nic show-effective-route-table   --resource-group RouteServer --name BackendVMNic -o table
Source                 State    Address Prefix    Next Hop Type          Next Hop IP
---------------------  -------  ----------------  ---------------------  -------------
Default                Active   172.16.0.0/16     VnetLocal
VirtualNetworkGateway  Active   172.22.2.0/24     VirtualNetworkGateway  172.16.1.4
VirtualNetworkGateway  Active   172.22.2.0/24     VirtualNetworkGateway  172.16.1.5
Default                Invalid  0.0.0.0/0         Internet
Default                Active   10.0.0.0/8        None
Default                Active   100.64.0.0/10     None
Default                Active   192.168.0.0/16    None
Default                Active   25.33.80.0/20     None
Default                Active   25.41.3.0/25      None
User                   Active   0.0.0.0/0         None
```
