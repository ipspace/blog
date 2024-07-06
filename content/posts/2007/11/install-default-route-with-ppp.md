---
date: 2007-11-21 07:45:00+01:00
tags:
- PPP
- WAN
- ADSL
title: Install default route with PPP
url: /2007/11/install-default-route-with-ppp.html
---
In my home office, I\'m using DSL access to the Internet with ISDN backup to another ISP, as shown on the next figure:

{{<figure src="/2007/11/homeSetup.jpg">}}

Obviously, I would like the ISDN backup to kick in whenever the primary connection goes down; two static default routes and [reliable static routing on the primary default](/2007/02/reliable-static-routing.html) seem like a perfect solution.
<!--more-->
However, as I\'m using PPP encapsulation on the primary connection, there\'s another option: PPP can insert a dynamic default route whenever IPCP negotiations succeed (and remove it when the line protocol goes down). To configure this feature (introduced in IOS releases 12.3(11)T and 12.4), use the **ppp ipcp route default** interface configuration command on the primary dialer interface.

``` {.code}
GW#show ip route | begin Gateway
Gateway of last resort is 10.0.0.33 to network 0.0.0.0
 
     10.0.0.0/32 is subnetted, 2 subnets
C 10.0.0.34 is directly connected, Serial1/0
C 10.0.0.33 is directly connected, Serial1/0
     192.168.0.0/28 is subnetted, 1 subnets
C 192.168.0.0 is directly connected, FastEthernet0/0
S* 0.0.0.0/0 [1/0] via 10.0.0.33
```

Contrary to the [DHCP-installed default route](/2007/06/dhcp-response-sets-default-route.html), the PPP-installed default route has administrative distance 1 (and is thus impossible to override)
