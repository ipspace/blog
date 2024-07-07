---
date: 2007-08-16 07:38:00.001000+02:00
tags:
- DHCP
title: Import DHCP options from an upstream DHCP server
url: /2007/08/import-dhcp-options-from-upstream-dhcp/
---
If your router gets its IP address from an upstream DHCP server, it can automatically import the other DHCP options (DNS server, WINS server, domain prefix etc.) into its DHCP pools. For example, if you use a router to connect to a cable or MAN Ethernet ISP (see the following figure), you can use the DHCP option import to minimize your router configuration (and make it fail safe from any changes in the ISP network).

{{<figure src="/2007/08/DHCPImport.jpg">}}

To configure the DHCP option import, use the **import all** DHCP pool configuration command. You cannot select which options you want to import, but you can override them with other DHCP pool configuration commands.
<!--more-->
{{<note>}}The import only happens when a DHCP reply is received. To force an immediate import, use the **renew dhcp *interface*** exec-level command.{{</note>}}

The sample configuration for the above network topology is included below:

``` {.code}
ip dhcp pool LAN
 import all
 network 10.0.0.0 255.255.255.0
 default-router 10.0.0.1
!
interface FastEthernet0/0
 description *** Internal LAN ***
 ip address 10.0.0.1 255.255.255.0
!
interface FastEthernet0/1
 description *** Public LAN interface ***
 ip address dhcp client-id FastEthernet0/1
```
