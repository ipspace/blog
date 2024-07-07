---
date: 2007-06-27 06:37:00+02:00
ospf_tag: default
tags:
- OSPF
title: Inserting Default Route Into OSPF
url: /2007/06/inserting-default-route-into-ospf/
---
Another Cisco IOS OSPF implementation trivia: if you're redistributing a default route into OSPF (for example, you have a static default route configured with **ip route 0.0.0.0 0.0.0.0 ...** and you use **redistribute static subnets** within the OSPF process), the default route will not be entered into the OSPF database unless you configure **default-information originate** within the router ospf configuration.

Similarly, if you configure **default-information originate always**, the router will inject the type 5 LSA for the default route into the OSPF topology database even if the router itself does not have a default route (or gateway of last resort).
