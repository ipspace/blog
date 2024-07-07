---
date: 2009-10-09 07:00:00.003000+02:00
tags:
- ARP
- IP routing
title: 'My Stupid Moments: Interface Default Route'
url: /2009/10/my-stupid-moments-interface-default/
---
Years ago I was faced with an interesting challenge: an Internet customer was connected to our PE router with an Ethernet link and I did not want to include the PE router's IP address in the default route on the CE router.

{{<note>}}The latest IOS release in those days was probably somewhere around 11.x; none of the [DHCP goodies](/2007/06/dhcp-response-sets-default-route/) were available.{{</note>}}

After pondering the problem for a while, I got a "brilliant" idea: if I would use an interface default route, proxy-ARP would solve all my problems. This is the configuration I've deployed on the CE-router:
<!--more-->
```
interface Ethernet 0
 description Uplink to the ISP
 ip address 10.0.1.2 255.255.255.0
!
ip route 0.0.0.0 0.0.0.0 ethernet 0
```

We tested this configuration in the middle of the night and it worked as expected. What do you think happened in the morning?

