---
date: 2008-04-17 07:08:00.001000+02:00
tags:
- IPv6
- OSPF
title: IPv4 Forever?
url: /2008/04/ipv4-forever.html
---
One of the obscure facts of IPv6 OSPF (OSPFv3) is that it uses a 32-bit router ID like OSPFv2. It\'s a reasonable choice, I haven\'t seen an OSPF network with more than a billion routers yet. However, could you guess how this requirement is implemented in Cisco IOS? [OSPFv3 searches for an IPv4 address](https://blog.ipspace.net/2007/10/ospf-router-id-does-not-change-when.html) (effectively the same algorithm used by OSPFv2) to get the router ID for the IPv6 routing process. Neat, isn\'t it?

You might wonder what happens if you want to configure an IPv6-only router. OSPF won\'t start unless you configure the router ID manually. And, no, you cannot enter a number (which would be the expected format, as the router ID is just a number in the IPv6 world), you have to enter an IPv4 address. Long live IPv4 :))
<!--more-->
Here is a sample printout from a router. First, let\'s check the interface status:

``` {.code}
Site-D(config)#do show ip interface brief
Interface           IP-Address      OK? Method Status    Protocol
FastEthernet0/0     unassigned      YES manual up        up      
FastEthernet0/1     unassigned      YES manual up        up      
Loopback0           unassigned      YES manual up        up
```

No IPv4 running anywhere. Good. Let\'s continue and configure IPv6:

``` {.code}
Site-D(config)#ipv6 unicast
Site-D(config)#ipv6 router ospf 1
Site-D(config-rtr)#
*Mar  1 01:18:46.423: %OSPFv3-4-NORTRID: OSPFv3 process 1 could not pick a router-id,
please configure manually
```

Oops, IPv6 OSPF won\'t start if the router doesn\'t have an IPv4 address. Let\'s configure the router ID:

``` {.code}
Site-D(config-rtr)#router-id ?
  A.B.C.D  OSPF router-id in IP address format

Site-D(config-rtr)#router-id 10.0.1.8
Site-D(config-rtr)#
```
