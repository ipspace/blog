---
date: 2009-03-02 06:47:00.001000+01:00
tags:
- BGP
title: 'BGP AS-Path Prepending: Technical Details'
series: bgp-essentials
url: /2009/03/as-path-prepending-technical-details/
Lastmod: 2020-12-07 11:12:00
---
I thought I knew all there is to know about the AS-path prepending before the [February 2009 incident](/2009/02/root-cause-analysis-oversized-as-paths/), which prompted me to focus on this particular Cisco IOS feature.

For example, did you know you could do *inbound* AS-path prepending? I didn't, until Rodney Dunn from Cisco mentioned it in an e-mail exchange. Did you ever wonder whether the AS-path prepending affects inbound or outbound AS-path filters? I had a hunch it doesn't, but was never sure. Time to figure out all the gory details...
<!--more-->
{{<ct3_rescue>}}
### AS Path Prepending 101

*AS-path prepending* is the manipulation of the BGP AS-path attribute beyond the insertion of local AS number on outgoing EBGP updates. Extra AS-numbers are inserted (*prepended*) at the beginning of AS-path, just after the local AS-number.

Cisco IOS supports *inbound* and *outbound* AS-path prepending on EBGP sessions. AS-path prepending does not work on IBGP sessions.

Outbound AS-path prepending can be used as the last-resort mechanism to influence global BGP routing policies in BGP multi-homing scenarios where all other methods (*Multi-exit Discriminator* or *Local preference* manipulation through BGP communities) don’t work due to lack of upstream ISP’s support or due to the wide difference in upstream ISP’s connectivity to the internet core.

Only *a few* copies of the *local* AS-number should be prepended to the AS-path when you use AS-path prepending to influence the BGP routing policies. If your problem cannot be solved by prepending less than 10 copies of the local AS-number, you should use other mechanisms (see also the [prepending statistics](https://labs.apnic.net/?p=1264) by Geoff Huston).

{{<note warn>}}You should not prepend long AS-path segments, modify inbound updates with inbound AS-path prepending or prepend non-local AS numbers outside of a lab environment. Never prepend long AS-path segments in the Internet.{{</note>}}

## Test Network Diagram

Throughout the article, the following test network will be used to generate router printouts. The initial router configurations are summarized in the *Initial router configuration* section. The routers were running Cisco IOS release 15.6(1)T.

{{<figure src="/2009/03/AS-Path-Lab.png" caption="Diagram of the lab network">}}

### Cisco IOS Configuration

BGP AS-path prepending is configured with the **set as-path prepend** statement within a **route-map**. The **route-map** can then be applied to inbound or outbound updates received or sent to an EBGP peer.

The AS-path prepending does not work on IBGP sessions or when the **route-map** is used in a **network** statement. In both cases, the **set as-path prepend** route map command is ignored without an error message.

### Outbound AS-Path Prepending

For example, to prepend two extra copies of the local AS-number to the outbound BGP updates sent from E1 to R1, you could use the following configuration on E1:

{{<cc>}}Outbound AS-path prepending on E1{{</cc>}}
```
router bgp 65000
 bgp log-neighbor-changes
 network 192.168.0.1 mask 255.255.255.255
 neighbor 10.0.0.2 remote-as 64800
 neighbor 10.0.0.2 description BGP sesssion to r1
 neighbor 10.0.0.2 next-hop-self
 neighbor 10.0.0.2 route-map prepend out
!
route-map prepend permit 10
 set as-path prepend 65000 65000
```

The AS-path prepending is applied to EBGP updates *when they are sent or received*. A change in the **route-map** configuration or BGP routing protocol configuration does not generate the outbound BGP updates, although they _might_ be generated at the next BGP scanner run (default value: 60 seconds). To force the change in the BGP routing policy after a **route-map** has been updated, use the **clear ip bgp _neighbor_ soft out** command.

{{<note info>}}Old Cisco IOS releases never sent BGP updates to BGP neighbors after a change in an outbound route-map. IOS release 15.6(1)T consistently generated an outbound update at the next BGP generic scan after a route map changed.{{</note>}}

After the changed BGP updates have been received by R1, its BGP table reflects the modified AS-path sent by E1. Due to longer AS-path on prefixes received over the E1-R1 link, R1 prefers IBGP paths received from R2; you’ve turned the link between E1 and R1 into a backup link.

```
r1#show ip bgp
BGP table version is 9, local router ID is 192.168.0.2
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>i 192.168.0.1/32   10.0.0.3                 0    100      0 65000 i
 *                    10.0.0.1                 0             0 65000 65000 65000 i
 *>  192.168.0.2/32   0.0.0.0                  0         32768 i
 *>i 192.168.0.3/32   10.0.0.3                 0    100      0 i
 ```

### Inbound AS-Path Prepending

You can use **set as-path prepend** command in an *inbound* route map. For example, to add an extra copy of the remote AS number to inbound updates received from E1, use the following configuration on R2:

```
router bgp 64800
 bgp log-neighbor-changes
 network 192.168.0.3 mask 255.255.255.255
 neighbor 10.0.0.1 remote-as 65000
 neighbor 10.0.0.1 description BGP sesssion to e1
 neighbor 10.0.0.1 next-hop-self
 neighbor 10.0.0.1 route-map prependIn in
!
route-map prependIn permit 10
 set as-path prepend last-as 1
```

The **set as-path prepend last-as** prepends the first AS in the AS-path (neighbor’s AS). You can use this command in an inbound **route-map** to simplify your configuration and make the **route-map** independent of the neighbor’s AS number.

{{<note warn>}}Do not use **set as-path prepend last-as** in an outbound route-map. The **set** statement would be executed *before* the local AS number is prepended to the AS-path, resulting in an "interesting" behavior.{{</note>}}

After R2 receives new EBGP update from E1 (for example, triggered by the **clear ip bgp _neighbor_ soft in** command or by a reset of the BGP session), the AS-path stored in the BGP table on R2 contains two copies of AS 65000:

```
r2#sh ip bgp
BGP table version is 10, local router ID is 192.168.0.3
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>  192.168.0.1/32   10.0.0.1                 0             0 65000 65000 i
 *>i 192.168.0.2/32   10.0.0.2                 0    100      0 i
 *>  192.168.0.3/32   0.0.0.0                  0         32768 i
 ```

## Troubleshooting AS-path Prepending

Outbound AS-path prepending can be reliably observed only in the BGP table of the EBGP peers. The **show ip bgp neighbor _address_ advertised-routes** command does not display the results of the outbound route-map; it displays the routes in the local BGP table that are advertised to the specified neighbor.

For example, the **show ip bgp neighbor 10.0.0.2 advertised** command executed on E1 displays empty AS-path even though two copies of AS65000 are prepended to the AS-path in the outgoing EBGP updates.

```
e1#sh ip bgp nei 10.0.0.2 advertised-routes
BGP table version is 6, local router ID is 192.168.0.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>  192.168.0.1/32   0.0.0.0                  0         32768 i
```

The **debug ip bgp updates** command is also useless, as it displays the contents of the local BGP table, not the output of the outbound **route-map**.

## AS-path Prepending and AS-path Filters

The prepended portion of the AS-path is not used in inbound or outbound AS-path filters; either in the **match as-path** conditions or in the per-neighbor filter lists. The AS-path filters always match the actual AS-path received from the BGP neighbor (when applied in the inbound direction) or the AS-path of the entry in the BGP table (when applied in the outbound direction).

### Outbound Prepending and AS-path Tests within the Route Map

The AS-path prepending does not influence the AS-path filters used within the **route-map** in the **match as-path** command. These filters are always matched against the original BGP entry in the BGP table. AS numbers specified with the **set as-path prepend** commands are accumulated and prepended to the AS-path attribute after the route map processing is completed.

To test the IOS behavior, we’ll modify the outbound *prepend* route map on E1 to include an AS-path filter. The **continue 20** statement in the first part of the route map ensures that the whole route map is executed.

{{<cc>}}Testing whether route map **match** statements use prepended AS-path{{</cc>}}
```
ip as-path access-list 100 permit ^$
!
route-map prepend permit 10
 set as-path prepend 10
 continue 20
!
route-map prepend permit 20
 match as-path 100
 set as-path prepend 20
```

If the AS-path filters would match the prepended AS-path, the **match as-path 100** test in the **route-map prepend permit 20** statement would not succeed and only a single AS-number would be prepended to the AS-path. However, the display of BGP table on R1 verifies that E1 prepended both AS-numbers to the AS-path:

```
r1#sh ip bgp
BGP table version is 10, local router ID is 192.168.0.2
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>i 192.168.0.1/32   10.0.0.3                 0    100      0 65000 65000 i
 *                    10.0.0.1                 0             0 65000 20 10 i
 *>  192.168.0.2/32   0.0.0.0                  0         32768 i
 *>i 192.168.0.3/32   10.0.0.3                 0    100      0 i
 ```

### Outbound Prepending and Outbound Neighbor Filter Lists

The outbound AS-path prepending does affect the operation of outbound filter lists. The AS-path access list specified in the **filter-list out** BGP neighbor option matches AS-paths in the BGP table, not the prepended paths generated by outbound route map.

If we modify the BGP router configuration on E1 to include an outbound **filter-list** on neighbor 10.0.1.6, E1 still sends the same prefix to R1, proving that the outbound **filter-list** does not test the prepended path.

{{<cc>}}Combination of AS-path prepending and outbound filter-list on E1{{</cc>}}
```
router bgp 65000
 bgp log-neighbor-changes
 network 192.168.0.1 mask 255.255.255.255
 neighbor 10.0.0.2 remote-as 64800
 neighbor 10.0.0.2 description BGP sesssion to r1
 neighbor 10.0.0.2 next-hop-self
 neighbor 10.0.0.2 route-map prepend out
 neighbor 10.0.0.2 filter-list 100 out
!
ip as-path access-list 100 permit ^$
!
route-map prepend permit 10
 set as-path prepend 65000 65000 65000 
```

{{<cc>}}Outbound updates are still sent to R2{{</cc>}}
```
e1#debug ip bgp updates 10.0.0.2 out
BGP updates debugging is on for neighbor 10.0.0.2 (outbound) ↲ 
for address family: IPv4 Unicast
e1#clear ip bgp * soft out
e1#
BGP(0): 10.0.0.2 NEXT_HOP is set to self for net 192.168.0.1/32,
BGP(0): (base) 10.0.0.2 send UPDATE (format) 192.168.0.1/32, ↲
next 10.0.0.1, metric 0, path Local
```

### Inbound Prepending and Inbound Neighbor Filter Lists

The inbound AS-path **filter-list** is applied before the inbound **route-map**. The AS-path attribute tested by the inbound AS-path access-list is thus the original AS-path sent by the EBGP neighbor, not the AS-path modified by inbound prepending.

You can use modified configuration of R2 to test this behavior.

```
router bgp 64800
 bgp log-neighbor-changes
 network 192.168.0.3 mask 255.255.255.255
 neighbor 10.0.0.1 remote-as 65000
 neighbor 10.0.0.1 description BGP sesssion to e1
 neighbor 10.0.0.1 next-hop-self
 neighbor 10.0.0.1 route-map prependIn in
 neighbor 10.0.0.1 filter-list 100 in
!
ip as-path access-list 100 permit ^65000$
!
route-map prependIn permit 10
 set as-path prepend last-as 2
```

The inbound **filter-list** matches the expected AS-path (65000) and the BGP debugging confirms the inbound EBGP update is accepted.

```
r2#debug ip bgp upd 10.0.0.1 in
BGP updates debugging is on for neighbor 10.0.0.1 (inbound) ↲
for address family: IPv4 Unicast
r2#clear ip bgp * soft in
r2#
...
BGP(0): 10.0.0.1 rcvd UPDATE w/ attr: nexthop 10.0.0.1, ↲
origin i, metric 0, merged path 65000, AS_PATH
```

The AS-path in the BGP table on R1 contains the received AS-path as well as the results of the inbound prepending:

```
r2#show ip bgp
BGP table version is 10, local router ID is 192.168.0.3
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 * i 192.168.0.1/32   10.0.0.2                 0    100      0 65000 20 i
 *>                   10.0.0.1                 0             0 65000 65000 i
 *>i 192.168.0.2/32   10.0.0.2                 0    100      0 i
 *>  192.168.0.3/32   0.0.0.0                  0         32768 i
 ```
