---
date: 2008-05-28 07:09:00.002000+02:00
tags:
- BGP
title: Conditional BGP Route Origination
url: /2008/05/conditional-bgp-route-origination/
lastmod: 2020-12-28 07:58:00
---
[Sebastian Majewski](https://www.linkedin.com/in/ccie18643/) has found an interesting feature: if you use the **network route-map** BGP configuration command to originate BGP prefixes and use the **match** conditions within the **route-map**, BGP inserts the IP prefix in the BGP table only if the source route in the IP routing table satisfies the **route-map** conditions.

{{<ct3_rescue>}}
<!--more-->
### More Details

The **network _a.b.c.d_ mask _e.f.g.h_ route-map _name_** BGP router configuration command is used to set attributes of the BGP prefix inserted in the BGP table when the corresponding IP prefix is installed in the IP routing table. Common usages include setting BGP communities, BGP local-preference or Multi-Exit Discriminator (MED).

{{<note>}}Unless configured in a **route-map**, MED is copied from the metric of the original route, local-preference is set to the value of the **bgp** **default local-preference** (or left empty) and BGP communities are not set.{{</note>}}

The **route-map** used in the **network** command can also match some attributes of the route in the *IP routing table* (but not in original routing protocol database). In this case, the BGP prefix will be inserted only if the original route matches the requirements of the **route-map**.

### Example

In a network using floating static routes for backup purposes, you might want to advertise the IP prefixes into BGP only if the subnets are reachable via a routing protocol, not via a floating static route.

The **match source-protocol** configuration command within a **route-map** does not work when used with the **network** command, so you have to use route tagging:

-   Floating static route is marked with a tag;
-   Routes received through routing protocols don’t have tags;
-   A **match tag** condition is used within a **route-map deny** statement to prevent the static route from being inserted into the BGP table.

The relevant parts of the router configuration that conditionally originates the IP prefix 10.3.1.0/24 are displayed in the following printout:

```
router bgp 65000
 network 10.3.1.0 mask 255.255.255.0 route-map NoStatic
!
ip route 10.3.1.0 255.255.255.0 Serial1/0 250 tag 250
!
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0
!
route-map NoStatic deny 10
 match tag 250
!
route-map NoStatic permit 20
```
