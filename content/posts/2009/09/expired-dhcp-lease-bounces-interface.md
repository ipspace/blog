---
date: 2009-09-16 07:25:00.001000+02:00
tags:
- DHCP
title: Expired DHCP Lease Bounces the Interface
url: /2009/09/expired-dhcp-lease-bounces-interface/
---
You would think that an expired DHCP lease is not a big deal for a DHCP client. Although the interface IP address is lost, you can always try to get a new address from the DHCP server.

IOS has a different opinion: when the DHCP lease expires on a router configured with **ip address dhcp** interface configuration command, the interface is administratively shut down and re-enabled. Here's a sample printout taken from a router running 15.6(1)T software:
<!--more-->
``` {.code}
%DHCP-5-RESTART: Interface GigabitEthernet0/1 is being restarted by DHCP
%LINK-5-CHANGED: Interface GigabitEthernet0/1, changed state to administratively down
%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down
%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to up
%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to up
%DHCP-6-ADDRESS_ASSIGN: Interface GigabitEthernet0/1 assigned DHCP address 10.0.0.4, ↲
mask 255.255.255.0, hostname c2
```

You might wonder how you could ever end up with an expired lease when there's a working DHCP server on the network. It's simple if your DHCP server runs on IOS: when you clear the DHCP bindings on a router running a DHCP server, it stops responding to lease extension requests (DHCPREQUEST packets) from unknown clients.
