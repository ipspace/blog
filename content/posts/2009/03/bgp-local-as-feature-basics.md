---
date: 2009-03-18 07:02:00+01:00
tags:
- BGP
title: 'Network Migration with BGP Local-AS Feature'
url: /2009/03/bgp-local-as-feature-basics/
lastmod: 2025-04-13 09:05:00+02:00
---
The Cisco IOS *BGP Local-AS* feature allows a BGP-speaking router to impersonate an autonomous system different from the one configured with the **router bgp** global configuration command. Its primary use facilitated seamless AS mergers; later additions made it applicable to AS renumbering scenarios. In the meantime, most other network operating systems implemented equivalent features ([_netlab_](https://netlab.tools/) can configure *local AS* functionality on [over a dozen platforms](https://netlab.tools/module/bgp/#platform-support))

The BGP Local-AS feature is usually configured with the **neighbor *IP-address* local-as _AS-number_** router configuration command. Subsequent IOS releases added the **no-prepend** keyword to clean up the AS path, as well as **replace-as** and **dual-as** keywords to support AS renumbering.
<!--more-->
## Typical Network Migration Usage Scenario

The BGP Local-AS functionality was designed to ease network migration in ISP merger/acquisition scenarios. For example, assume that ISP B (AS 64510) is merging with ISP A (AS 64500):

{{<figure src="/2009/03/localas-initial.png" caption="Testbed diagram and addressing">}}

When the routers in AS 64510 are moved into AS 64500, the EBGP peering sessions with the customers must be reconfigured on the customer’s side, requiring significant coordination and planning efforts. The Local-AS feature allows the migrated PE routers to participate in AS 64500 while impersonating AS 64510 toward the customers’ CE routers:

{{<figure src="/2009/03/localas-migrate.png" caption="R1 and R2 impersonate AS 64510 toward CE routers">}}

The routers using the Local-AS feature retain the information that the BGP routes have passed the *local* AS in the AS path. They prepend *local-AS* in inbound EBGP updates and prepend both the actual AS number and the *local-AS* number in outbound EBGP updates.

{{<figure src="/2009/03/localas-aspath.png" caption="AS-path processing in the migrated network">}}

{{<note>}}
The _[netlab](https://netlab.tools/)_ topologies needed to recreate the scenario described in the blog post are [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/BGP/LocalAS-Migration), as are the [complete device configurations](https://github.com/ipspace/netlab-examples/tree/master/BGP/LocalAS-Migration/initial).
{{</note>}}

## Sample Network Migration and Monitoring

The migration of our test network is performed in these steps:

1.  OSPF is established between ISPA, R1 and R2.
2.  The EBGP session between ISPA and R1 is changed into an IBGP session.
3.  Complete BGP configuration has to be removed and reconfigured on R1 and R2 (it’s impossible to change the BGP AS number once the BGP routing process has started).

{{<note info>}}
Changes in BGP configuration on R1 and R2 might also involve changes in inbound AS-path filters.
{{</note>}}

4.  A new IBGP session structure must be established between old and new members of AS 64500. In the test network, R1 will be configured as a route reflector and ISPA and R2 as its clients, resulting in no extra IBGP sessions and minimal configuration changes. You can expect significantly more changes in an actual production network.

### BGP Topology before Network Migration

The following printouts contain the state of the BGP routing tables (RIB) on all test network routers before the network migration. You can use these tables to compare the initial network state with the migration results.

{{<cc>}}BGP routing table on ISPA{{</cc>}}
```
ispa#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      0.0.0.0                  0         32768 i
 *>   10.8.8.0/24      10.1.0.2                               0 64510 65000 i
 *>   10.9.9.0/24      10.1.0.2                               0 64510 65100 i
```

{{<cc>}}BGP routing table on R1{{</cc>}}
```
r1#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.1                 0             0 64500 i
 *>   10.8.8.0/24      10.1.0.9                 0             0 65000 i
 *>i  10.9.9.0/24      10.0.0.3                 0    100      0 65100 i
```

{{<cc>}}BGP routing table on R2{{</cc>}}
```
r2#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>i  10.6.6.0/24      10.0.0.2                 0    100      0 64500 i
 *>i  10.8.8.0/24      10.0.0.2                 0    100      0 65000 i
 *>   10.9.9.0/24      10.1.0.13                0             0 65100 i
```

{{<cc>}}BGP routing table on CustA{{</cc>}}
```
custA#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.10                              0 64510 64500 i
 *>   10.8.8.0/24      0.0.0.0                  0         32768 i
 *>   10.9.9.0/24      10.1.0.10                              0 64510 65100 i
```

{{<cc>}}BGP routing table on CustB{{</cc>}}
```
custB#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.14                              0 64510 64500 i
 *>   10.8.8.0/24      10.1.0.14                              0 64510 65000 i
 *>   10.9.9.0/24      0.0.0.0                  0         32768 i
```

### Router Configuration Changes

We have to start the OSPF process on ISPA and run OSPF on the WAN link between ISPA and R1. Furthermore, the EBGP session between ISPA and R1 must be converted into an IBGP session established between the loopback interfaces of ISPA and R1:

{{<note info>}}The following printouts include only the essential changes to router configurations; complete configurations are [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/BGP/LocalAS-Migration/migrated).{{</note>}}

{{<cc>}}Configuration changes on ISPA{{</cc>}}
```
interface Ethernet0/1
 description ispa -> r1
 ip ospf network point-to-point
 ip ospf 1 area 0.0.0.0
!
router ospf 1
 router-id 10.0.0.1
!
router bgp 64500
 no neighbor 10.1.0.2
 neighbor 10.0.0.2 remote-as 64500
 neighbor 10.0.0.2 description r1
 neighbor 10.0.0.2 update-source Loopback0
 !
 address-family ipv4
  neighbor 10.0.0.2 activate
  neighbor 10.0.0.2 next-hop-self
 exit-address-family
```

More extensive changes are needed on R2: the whole BGP configuration has to be removed, and a new BGP process with a different AS number has to be started. *Local AS* is configured on customer EBGP sessions to avoid configuration changes on the customer’s end.

{{<cc>}}Configuration changes on R2{{</cc>}}
```
no router bgp 64510
!
router bgp 64500
 bgp router-id 10.0.0.3
 neighbor 10.0.0.2 remote-as 64500
 neighbor 10.0.0.2 description r1
 neighbor 10.0.0.2 update-source Loopback0
 neighbor 10.1.0.13 remote-as 65100
 neighbor 10.1.0.13 local-as 64510
 neighbor 10.1.0.13 description custb
```

R1 requires changes in OSPF and BGP configuration. OSPF has to be enabled on the WAN link between R1 and ISPA. The EBGP configuration has to be reentered with a different AS number. Customer EBGP sessions need a *local AS* number, and the IBGP sessions are configured as route reflector server-to-client sessions.

{{<cc>}}Configuration changes on R1{{</cc>}}
```
interface Ethernet0/1
 description r1 -> ispa
 ip ospf network point-to-point
 ip ospf 1 area 0.0.0.0
!
no router bgp 64510
!
router bgp 64500
 neighbor 10.0.0.1 remote-as 64500
 neighbor 10.0.0.1 description ispa
 neighbor 10.0.0.1 update-source Loopback0
 neighbor 10.0.0.1 route-reflector-client
 neighbor 10.0.0.1 next-hop-self
!
 neighbor 10.0.0.3 remote-as 64500
 neighbor 10.0.0.3 description r2
 neighbor 10.0.0.3 update-source Loopback0
 neighbor 10.0.0.3 route-reflector-client
 neighbor 10.0.0.3 next-hop-self
!
 neighbor 10.1.0.9 remote-as 65000
 neighbor 10.1.0.9 local-as 64510
 neighbor 10.1.0.9 description custa
```

No configuration changes are needed on the customers’ CE routers.

### BGP Topology after the Network Migration

BGP tables on ISPA are the least affected by the network migration. The only noticeable change is a different next-hop for routes received from CustB via R2. Previously, the next-hop was changed by the EBGP session between ISPA and R1; now, it’s propagated unchanged across AS 64500. The AS paths for IP prefixes received from the customers are also unchanged: they look like they would still pass through AS 64510 due to inbound prepending of the BGP *Local AS*.

{{<cc>}}BGP routing table on ISPA (after migration){{</cc>}}
```
ispa#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      0.0.0.0                  0         32768 i
 *>i  10.8.8.0/24      10.0.0.2                 0    100      0 64510 65000 i
 *>i  10.9.9.0/24      10.0.0.3                 0    100      0 64510 65100 i
```

The changes on R1 and R2 are also minor – as they belong to the same AS as ISPA, the IP prefix advertised by ISPA has become an internal BGP route with an empty AS path:

{{<cc>}}BGP routing table on R1 (after migration){{</cc>}}
```
r1#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>i  10.6.6.0/24      10.0.0.1                 0    100      0 i
 *>   10.8.8.0/24      10.1.0.9                 0             0 64510 65000 i
 *>i  10.9.9.0/24      10.0.0.3                 0    100      0 64510 65100 i
```

{{<cc>}}BGP routing table on R2 (after migration){{</cc>}}
```
r2#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>i  10.6.6.0/24      10.0.0.1                 0    100      0 i
 *>i  10.8.8.0/24      10.0.0.2                 0    100      0 64510 65000 i
 *>   10.9.9.0/24      10.1.0.13                0             0 64510 65100 i
```

The migration effects on the customer routers are more dramatic. The AS paths of prefixes originated in AS 64500 (and any network beyond AS 64500) are unchanged, but the paths to other customers of ISPB have changed significantly. Before the migration, the path between CustA and CustB passed only through AS 64510. Now, it looks like it passes through two copies of AS 64510 (due to inbound and outbound prepending of *Local AS*) as well as through the AS 64500 (the actual AS of ISPA).

{{<cc>}}Modified BGP routing table on CustA{{</cc>}}
```
custa#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.10                              0 64510 64500 i
 *>   10.8.8.0/24      0.0.0.0                  0         32768 i
 *>   10.9.9.0/24      10.1.0.10                              0 64510 64500 64510 65100 i
```

{{<cc>}}Modified BGP routing table on CustB{{</cc>}}
```
custb#show ip bgp | begin Network
     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.6.6.0/24      10.1.0.14                              0 64510 64500 i
 *>   10.8.8.0/24      10.1.0.14                              0 64510 64500 64510 65000 i
 *>   10.9.9.0/24      0.0.0.0                  0         32768 i
```

{{<note warn>}}
The longer AS paths observed by the customer routers might affect their outbound route selection (if they do load balancing based on the AS path lengths) or even route availability if the customers use inbound AS path filters.
{{</note>}}

## Revision History

2025-04-13
: * Migrated an [archived copy](https://web.archive.org/web/20171012143846/http://wiki.nil.com/Network_migration_or_merger_with_BGP_Local-AS_feature) of a long-gone article to ipSpace.net blog
  * Created a corresponding _netlab_ topology to help readers reproduce the scenario
  * Printouts were recreated on Cisco IOS XE devices.
