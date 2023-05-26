---
kb_section: ScalablePolicyRouting
minimal_sidebar: true
pre_scroll: true
title: Configure Policy Routing on the Core Routers
url: /kb/Internet/ScalablePolicyRouting/40-pbr-core-routers.html
---
BGP configuration on the *Legacy* router changes only slightly: a route-map is attached to the network statement advertising the IP prefixes of the legacy servers:

{{<cc>}}Changes in the BGP configuration of the *Legacy* router{{</cc>}}
```
router bgp 65000
 network 10.0.20.0 mask 255.255.255.0 route-map FRBest
!
route-map FRBest permit 10
 set community 65000:100
```

The *RemoteSite* peer policy template is changed on the *CoreInet* router to set the MED to 200 on all outgoing updates:

{{<cc>}}BGP configuration changes on the *CoreInet* router{{</cc>}}
```
router bgp 65000
 template peer-policy RemoteSite
  route-map InetMED out
!
route-map InetMED permit 10
 set metric 200
```

The changes on the *CoreFR* router are a bit more extensive: 

* An **ip community-list** is defined to match the target BGP community (65000:100).
* A **route-map** is used to match BGP prefixes with the target BGP community and change their MED to 100. The MED of all other BGP prefixes is set to 300.
* The *RemoteSite* peer policy template is modified to include an outgoing **route-map**.

{{<cc>}}BGP configuration changes on the *CoreFR* router{{</cc>}}
```
router bgp 65000
 template peer-policy RemoteSite
  route-map FRMED out
!
ip community-list standard FRBest permit 65000:100
!
route-map FRMED permit 10
 match community FRBest
 set metric 100
!
route-map FRMED permit 20
 set metric 300
```

<!-- end -->
