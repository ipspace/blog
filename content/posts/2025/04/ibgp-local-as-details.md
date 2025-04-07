---
title: "iBGP Local-AS Details"
date: 2025-04-08 08:08:00+0200
tags: [ BGP ]
---
Did you know you could use the **neighbor local-as** BGP functionality to fake an iBGP session between different autonomous systems? I knew Cisco IOS supported that monstrosity for ages (supposedly "_to merge two ISPs that have different AS numbers_") and added the appropriate tweaks[^HNUI] into _[netlab](https://netlab.tools/)_ when I added the [BGP **local-as** support](https://github.com/ipspace/netlab/commit/0943d5fe5686adf1766fc1062313ef2ed55f50e3) in release 1.3.1. Someone couldn't resist [pushing us down that slippery slope](https://github.com/ipspace/netlab/issues/368), and we ended with IBGP local-as implemented on [18 platforms](https://netlab.tools/module/bgp/#platform-support) (almost a dozen network operating systems).

I even wrote a [related integration test](https://github.com/ipspace/netlab/blob/release_1.9.5/tests/integration/bgp/08-ibgp-localas.yml), and all our implementations passed it until I asked myself a simple question: "But does it work?" and the number of correct implementations that passed the test without warnings dropped to zero.
<!--more-->
[^HNUI]: Together with "I hope no one uses it," rephrased as "viability of IBGP local-as is not checked yet." in the commit message.

{{<figure src="/2025/04/local-as-initial.png" caption="Topology of the original integration test">}}

{{<long-quote>}}
This series of blog posts is a _thinking-out-loud_ exercise and should document most of the caveats you might encounter if you decide to use this feature.

**Before you start:** Just because you could does not mean you should. You've been warned.
{{</long-quote>}}

Here's what I've been checking in that integration test:

* Are the BGP sessions established?
* Are the BGP prefixes originated by the device under test (DUT) propagated to X1 and X2?
* Are the BGP prefixes propagated between X1 and X2?

Once we got the basics right, the answer to all three questions was **yes** for every platform we tested. For example, X2 receives the prefix originated by X1 when DUT is running Arista EOS with the following BGP configuration ([lab topology](https://github.com/ipspace/netlab-examples/blob/master/BGP/IBGP-local-AS/initial.yml), [full configurations](https://github.com/ipspace/netlab-examples/tree/master/BGP/IBGP-local-AS/initial)):

{{<cc>}}Relevant parts of BGP configuration on Arista EOS{{</cc>}}
```
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor 10.1.0.2 remote-as 65100
   neighbor 10.1.0.2 local-as 65002 no-prepend replace-as
   neighbor 10.1.0.2 description x1
   neighbor 10.1.0.2 send-community standard large
   neighbor 10.1.0.6 remote-as 65101
   neighbor 10.1.0.6 next-hop-peer
   neighbor 10.1.0.6 local-as 65101 no-prepend replace-as
   neighbor 10.1.0.6 description x2
   neighbor 10.1.0.6 send-community standard extended large
   !
   address-family ipv4
      neighbor 10.1.0.2 activate
      neighbor 10.1.0.6 activate
```

{{<cc>}}BGP table on X2{{</cc>}}
```
x2# show ip bgp
BGP table version is 3, local router ID is 172.42.2.1, vrf id 0
Default local pref 100, local AS 65101
Status codes:  s suppressed, d damped, h history, u unsorted, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>i 10.0.0.1/32      10.1.0.5                      100      0 i
   i 172.42.1.0/24    10.1.0.2                 0    100      0 65100 i
 *>  172.42.2.0/24    0.0.0.0(x2)              0         32768 i
 *>i 172.42.42.0/24   10.1.0.5                      100      0 ?
```

However, X2 is not using the 172.42.1.0/24 prefix advertised by X1 through DUT *because the next hop is not reachable*:

{{<cc>}}X1 BGP prefix advertised by DUT to X2{{</cc>}}
```
x2# show ip bgp 172.42.1.0
BGP routing table entry for 172.42.1.0/24, version 0
Paths: (1 available, no best path)
  Not advertised to any peer
  65100
    10.1.0.2 (inaccessible, import-check enabled) from 10.1.0.5 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, invalid, internal
      Last update: Mon Apr  7 06:23:18 2025
```

Here's the problem: according to the standard [BGP next-hop processing rules](https://blog.ipspace.net/2011/08/bgp-next-hop-processing), the [BGP next-hop is not changed on an IBGP session](https://blog.ipspace.net/2011/08/bgp-next-hop-processing/#bgp-next-hop-is-not-changed-on-ibgp-sessions) because the protocol designers assumed the subnets connecting a BGP router to its EBGP peers would be advertised in the IGP.

However, we're faking an IBGP session between two autonomous systems *with no underlying IGP*. Unless DUT advertises the X1-DUT subnet *into BGP* (bad idea), X2 has no information about the advertised next hop (X1 IP address 10.1.0.2).

**Conclusion:** One **MUST** use **neighbor next-hop-self** to change the next hop on an iBGP local-as session.

{{<next-in-series page="/posts/2025/04/xxx.md">}}
But wait, there's more. We've only scratched the surface of the iBGP local-as complexity. In a few days, we'll explore what happens if you use this abhorrent mechanism to connect two large autonomous systems.
{{</next-in-series>}}
