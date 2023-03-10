---
date: 2008-05-20 07:20:00.001000+02:00
lastmod: 2020-12-04 17:41:00
multihoming_tag: bgp
series:
- multihoming
tags:
- BGP
title: Multihoming to a Single ISP
url: /2008/05/multihoming-to-single-isp.html
---
*Multihoming to a single ISP* is a design scenario in which a customer uses multiple Internet connections to the same Internet Service Provider. This design provides resilience against link and device failures, but does not provide protection against major outages within the Service Provider network.

There are three major decisions to be made when designing multihoming to single ISP:

* Will the customer use provider-assigned or provider-independent address space?
* Should the customer use static or dynamic routing with the ISP?
* When using dynamic routing with BGP, does the customer need its own public autonomous system?
<!--more-->
{{<figure src="MH_1ISP_Scenario.png" caption="Multihoming to single ISP">}}

## Addressing

A customer multi-homed to a single ISP could use [provider-independent (PI) addresses](http://en.wikipedia.org/wiki/Provider_Independent_Address_Space) and advertise its IP prefix to the Internet, or [provider-aggregatable (PA) addresses](http://www.ripn.net:8080/nic/ripe-docs/ripe-127.txt) assigned by its ISP.

Using PA addresses helps reduce the overall size of the Internet routing tables, but it's hard to migrate to another ISP if you use them. If the customer wants to have the options of switching service providers or connecting to multiple ISPs in the future, they should go for PI addresses.

{{<note>}}Although the examples in this blog post use IPv4 addresses, the same reasoning applies to IPv6. Also note that it's becoming harder and harder to get IPv4 PI addresses.{{</note>}}

## Routing

Static routing could be used between the customer and the ISP, but it’s highly recommended to use BGP on the PE-CE links. A dynamic routing protocol is much better than tricks like _reliable static routes_ in detecting link and adjacent router failure, and if one wants to use a routing protocol between a customer and a service provider, BGP is the only reasonable option.

[Full Internet routing](http://en.wikipedia.org/wiki/Default-free_zone) could be sent to the customer’s routers, but this is usually unnecessary. Default route propagated from the ISP via BGP is sufficient to establish correct upstream routing; BGP prefixes of the ISP and its other customers should be advertised to optimize local routing. The IP prefixes assigned to the customer (PI or PA prefixes) should always be advertised from the customer’s (CE) routers via BGP to ensure link/device failure detection.

If the customer already owns an Autonomous System (AS) number, it should be used from the start. Otherwise, a private AS number could be configured on the customer site.

For more details, watch the [Surviving the Internet Default Free Zone](https://www.ipspace.net/Surviving_the_Internet_Default_Free_Zone) webinar.

### BGP Routing with PA Addresses

In _multihoming to single ISP_ scenarios there's no need to propagate PA prefixes assigned to a customer beyond the provider’s AS. It’s therefore irrelevant whether the customer uses private or registered AS number, as the paths originated by the customer are never propagated into the Internet. The filtering of the customer’s IP prefixes is the ISP’s responsibility.

The ISP could use a variety of mechanisms to filter customer’s PA prefixes, for example:

-   If the ISP propagates BGP communities within its AS, it could mark all PA prefixes received from the customers with the **no-export** community, which will ensure that they are never propagated beyond the ISP’s AS.
-   The ISP could filter outbound updates sent toward its peering partners removing all small PA prefixes (for example, all prefixes smaller than /20), or all prefixes with a private AS number.

{{<figure src="MH_1ISP_NoExport.png" caption="Using no-export community to filter customer prefixes">}}

The following printout shows a typical PE-router configuration. The PE-router advertises the default route and the local prefixes to the customer’s router and marks all inbound routes with the **no-export** community. Inbound **prefix-list** filter ensures that the customer cannot insert unauthorized prefixes into the provider’s AS.

```
router bgp 123
 template peer-policy Private_MH
  filter-list 100 out
  default-originate
 exit-peer-policy
 !
 template peer-policy Private_MH_PA
  route-map Private_MH_PA in
  inherit peer-policy Private_MH 1
 exit-peer-policy
 !
 neighbor 192.168.1.2 remote-as 65000
 neighbor 192.168.1.2 prefix-list Customer_A in
 neighbor 192.168.1.2 inherit peer-policy Private_MH_PA 
!
ip prefix-list Customer_A seq 5 permit 10.0.1.0/24
!
ip as-path access-list 100 permit ^$
!
route-map Private_MH_PA permit 10
 set community no-export additive
```

### BGP Routing with PI Addresses and Private AS Number

If a customer already owns provider-independent addresses but does not have a registered AS number, it can use a private AS number to establish BGP peering with the ISP to which it’s multi-homed. The ISP should remove the private AS number of the customer on all other EBGP sessions with the **neighbor remove-private-as** option, making the customer’s PI prefix appear as if it’s originated from within the ISP’s AS.

{{<note warn>}}When deploying RPKI, make sure that the public ROA records announce the customer prefix as belonging to the provider AS number.{{</note>}}

{{<figure src="MH_1ISP_RemovePrivateAS.png" caption="Removing private AS numbers on peering connections">}}

The configuration of the customer-facing PE-router is very similar to the one described in the previous section (the inbound route-map is removed as the PI prefixes should not be marked with the **no-export** community).

```
router bgp 123
 template peer-policy Private_MH
  filter-list 100 out
  default-originate
 exit-peer-policy
 !
 neighbor 192.168.1.2 remote-as 65000
 neighbor 192.168.1.2 prefix-list Customer_A in
 neighbor 192.168.1.2 inherit peer-policy Private_MH
!
ip prefix-list Customer_A seq 5 permit 10.0.1.0/24
!
ip as-path access-list 100 permit ^$
```

If an ISP allows its customers to use private AS numbers for BGP peering, the **remove-private-as** option has to be configured on all EBGP peers throughout the ISP’s network (or, at the very minimum, on the EBGP sessions with other ISPs). A sample router configuration from an IXP router is included in the following printout:

```
router bgp 123
 neighbor 192.168.2.2 remote-as 456
 neighbor 192.168.2.2 remove-private-as
```

Using this setup, an IP prefix with a private AS number advertised from the customer appears as originating from the provider’s AS (AS 123) on the EBGP peer

{{<cc>}}Customer advertising 10.0.1.0/24 with a private AS{{</cc>}}
```
E1#show ip bgp neighbor 192.168.2.2 advertised-routes | begin Network
Network        Next Hop   Metric LocPrf Weight Path
*>i10.0.1.0/24 192.168.1.2     0    100      0 65000i
```

{{<cc>}}Outside of ISP network, prefix 10.0.1.0/24 seems to belong to provider AS{{</cc>}}
```
X1#show ip bgp regexp 123
Network        Next Hop    Metric LocPrf Weight Path
*> 10.0.1.0/24 192.168.2.1                    0 123i
```

### BGP routing with PI addresses and registered AS number

This is a classic multi-homed scenario and will not be described any further.

### More Information

[Surviving the Internet Default Free Zone](https://www.ipspace.net/Surviving_the_Internet_Default_Free_Zone) webinar describes these related topics:

* Acquiring IP addresses and AS number
* Transit connection to the Internet
* Peering and Filtering
* Connecting to an Internet Exchange Point (IXP)



