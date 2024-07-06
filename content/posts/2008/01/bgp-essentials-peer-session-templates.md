---
date: 2008-01-29 07:02:00+01:00
tags:
- BGP
title: 'BGP Peer Session and Policy Templates'
lastmod: 2020-11-20 15:27:00
url: /2008/01/bgp-essentials-peer-session-templates.html
series: bgp-essentials
---
Configuring a large number of similar BGP peers on a router and ensuring that the changes in your routing policy or BGP design are applied to all of them can be a management nightmare. BGP peer groups were the only scalability tool available on Cisco IOS until the IOS release 12.3T and they had significant limitations as they were also used as a [performance improvement tool](/2006/10/bgp-peer-groups-no-longer-performance.html).

IOS releases 12.0S and 12.3T introduced *peer templates*, a scalable hierarchical way of configuring BGP session parameters and inbound/outbound policies. For example, to configure the *session parameters* for all your IBGP sessions, use the following session template:

```
router bgp 65001
 template peer-session IBGP
  remote-as 65001
  description IBGP peers
  password s3cr3t
  update-source Loopback0
```

{{<note info>}}Session template includes parameters that apply to a BGP _session_, including remote AS number, local AS number, MD5 password, and the source IP address of the BGP session. Parameters specific to individual address families are defined in a _policy template_.{{</note>}}

After the session template has been configured, adding a new IBGP peer takes just a single configuration command (two if you want to add neighbor description):

```
router bgp 65001
 neighbor 10.0.1.2 inherit peer-session IBGP
 neighbor 10.0.1.2 description R2
```

*Policy templates* are similar to *session templates*, and contain neighbor parameters that influence processing of prefixes of an individual BGP address family (example: filtering of inbound updates).

Continuing the IBGP example, you might want to group route reflector clients in a policy template, and ensure the route reflector propagating all BGP communities to them:

```
router bgp 65001
 template peer-policy Internal
  route-reflector-client
  send-community both
 exit-peer-policy
```

After defining a policy template, you can apply it to multiple address families, for example:

```
router bgp 65001
 neighbor 10.0.1.2 inherit peer-session IBGP
 neighbor 10.0.1.2 description R2
!
 address-family ipv4
  neighbor 10.0.1.2 activate
  neighbor 10.0.1.2 inherit peer-policy Internal
 exit-address-family
 !
 address-family vpnv4
  neighbor 10.0.1.2 activate
  neighbor 10.0.1.2 inherit peer-policy Internal
```
