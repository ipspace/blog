---
date: 2012-10-29 09:19:00.002000+01:00
tags:
- DHCP
title: Coping with Holiday Traffic – Secondary DHCP Subnets
url: /2012/10/coping-with-holiday-traffic-secondary/
---
Years ago the IT of the organization I worked for assigned a /28 to my home office. It seemed enough; after all, who would ever have more than \~10 IP hosts at home (or [more than four computers at a site](https://video.arnes.si/portal/asset.zul?id=K1ETXpmORoMQkDeokYR8ZtNu)).

When the number of Linux hosts and iGadgets started to grow, I occasionally ran out of IPv4 addresses, but managed to kludge my way around the problem by reducing DHCP lease time. However, when the start of school holidays coincided with the first snow storm of the season (so all the kids used their gadgets simultaneously) it was time to act.
<!--more-->
{{<figure src="/2012/10/s1600-Slika0133.jpg" caption="This is what \~20 cm (8 inches) of snow look like">}}

Before you tell me IPv6 would be a solution -- I know that, but none of my ISPs managed to configure IPv6 on my uplinks yet, and tunnels are so last millennium.

### Reducing lease time

Some battery-powered gadgets turn off after a while... but the IPv4 address they acquired is still leased to them, preventing some other gadget from getting Internet connectivity. Reducing lease time to a very short interval (30 seconds, for example) solves that problem... as long as the number of *concurrently active* gadgets doesn't exceed the threshold.

This is the relevant DHCP configuration from my home router:

{{<cc>}}Short DHCP lease time{{</cc>}}
``` {.code}
ip dhcp pool DHCP
   network 192.168.200.192 255.255.255.240
   default-router 192.168.200.193
   domain-name example.com
   dns-server 192.168.200.193
   lease 0 0 30
```

#### Adding a secondary subnet

With the older kids bringing all sorts of fruity gadgets home, and having their smart phones connected to WiFi all the time, the reduced lease time trick collapsed... and you probably know how nervous teenagers might get when they can't connect to Facebook. It was time to add a secondary subnet.

Fortunately, Cisco introduced secondary DHCP subnets in 12.4T -- I had to add only three lines to my router configuration to add the second subnet to my home network:

{{<cc>}}Secondary DHCP subnet{{</cc>}}
``` {.code}
interface Vlan1
 ip address 10.217.233.1 255.255.255.0 secondary
!
ip dhcp pool DHCP
   network 192.168.200.192 255.255.255.240
   network 10.217.233.0 255.255.255.0 secondary
     override default-router 10.217.233.1
   default-router 192.168.200.193
   domain-name example.com
   dns-server 192.168.200.193
   lease 0 0 30
```

The secondary DHCP subnet functionality is exactly what I needed:

-   You don't have to create a second DHCP pool with duplicate set of DHCP parameter;
-   You can still modify the default router value;
-   [Addresses are assigned from the secondary pool only if the primary pool is exhausted](http://www.cisco.com/en/US/docs/ios/12_4t/ip_addr/configuration/guide/htdhcpsv.html#wp1151571) (so all my devices will get addresses from the primary pool once the kids go back to school).

Addressing problem solved... now I have to find that second WiFi access point somewhere deep in my drawers.
