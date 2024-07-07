---
date: 2007-06-05 09:04:00+02:00
tags:
- DHCP
- IP routing
title: DHCP Response Sets the Default Route
pre_scroll: True
url: /2007/06/dhcp-response-sets-default-route/
---
It makes perfect sense in hindsight, but I was nonetheless pleasantly surprised: when the router acting as a DHCP client (configured with the **ip address dhcp** interface configuration command) receives the DHCP reply packet containing the default gateway option (option #3), it installs a static default route toward that next-hop.

Even better, the default route is installed with the administrative distance 254 (floating static route), making sure that the default route you've configured manually or the default route received via a routing protocol are not overwritten.
<!--more-->
To add icing on the cake, starting with IOS release 12.3(8)T you can disable this behavior with the **no ip dhcp client request router** interface-configuration command.

The following listing contains a sample debugging session documenting this behavior:

``` code
DHCP: Received a BOOTREP pkt
DHCP: Scan: Message type: DHCP Ack
DHCP: Scan: Server ID Option: 192.168.0.1 = C0A80001
DHCP: Scan: Lease Time: 86400
DHCP: Scan: Renewal time: 43200
DHCP: Scan: Rebind time: 75600
DHCP: Scan: Host Name: r4.company.com.
DHCP: Scan: Subnet Address Option: 255.255.255.240
DHCP: Scan: Router Option: 192.168.0.1

... deleted ...

DHCP: Server ID Option: 192.168.0.1
DHCP Host Name Option: r4.company.com.
DHCP: Releasing ipl options:
DHCP: Applying DHCP options:
  Setting default_gateway to 192.168.0.1
  Adding default route 192.168.0.1
Allocated IP address = 192.168.0.6  255.255.255.240

%DHCP-6-ADDRESS_ASSIGN: Interface FastEthernet0/0 assigned DHCP address 192.168.0.6, mask 255.255.255.240, hostname r4

r4#show ip route 0.0.0.0
Routing entry for 0.0.0.0 0.0.0.0, supernet
  Known via "static", distance 254, metric 0, candidate default path
  Routing Descriptor Blocks:
  * 192.168.0.1
      Route metric is 0, traffic share count is 1
```
