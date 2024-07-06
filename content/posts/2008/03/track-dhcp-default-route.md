---
date: 2008-03-29 07:04:00.004000+01:00
tags:
- DHCP
- IP routing
title: Track the DHCP Default Route
url: /2008/03/track-dhcp-default-route.html
---
Cisco has published a series of documents describing [how you can connect a SOHO site to two ISPs](http://www.cisco.com/en/US/products/sw/secursw/ps1018/products_configuration_example09186a00809454c7.shtml).

Their configuration also includes a nice trick: the **ip dhcp client route track *number*** command is a convenient replacement for a static default route with the **track** option if one of the upstream interfaces uses DHCP and the router generates the [default route based on DHCP replies](/2007/08/dhcp-based-static-routes.html).
