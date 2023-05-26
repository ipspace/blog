---
kb_section: ScalablePolicyRouting
minimal_sidebar: true
pre_scroll: true
title: Policy Routing to the Servers
url: /kb/Internet/ScalablePolicyRouting/30-pbr-to-server.html
---
Whenever you want to implement policy routing in a network, you have to consider both traffic flow directions independently. For example, changes you make to force the traffic from remote sites to use a particular link toward a specific server usually do not influence the traffic flowing in the other direction, potentially resulting in asymmetrical traffic.

{{<note warn>}}Asymmetrical traffic flow should be avoided, as it could introduce unwanted jitter and subsequently reduce the overall throughput.{{</note>}}

In this section, we’ll focus on the traffic flow from remote sites toward the servers; the next section will deal with return traffic.

To influence the traffic flow toward the servers, remote site routers have to prefer IP prefixes for the legacy servers received from the *CoreFR* router over those received from the *CoreInet* router. You could use a variety of BGP mechanisms, but the only one that requires no configuration changes on remote sites (and this is crucial to achieve scalability) is the Multi-Exit Discriminator (MED) attribute, which can be set on the central site routers and accepted by the remote sites.

The following MED values are used in the sample network:

* MED=200 is set on all IP prefixes advertised from the *CoreInet* router to the remote sites.
*	MED=300 is set on IP prefixes advertised from the *CoreFR* router to the remote sites to ensure the backup path is only used when the primary link fails (lower MED values are preferred)

{{<figure src="corenet-preferred-web.jpg" caption="CoreInet router is preferred for the Web LAN">}}

*	MED=100 is set on IP prefixes of the legacy servers when they are advertised from the *CoreFR* router, making them more preferred over the slower link.

{{<figure src="corefr-preferred-legacy.jpg" caption="CoreFR router is preferred for the Legacy LAN">}}

You can use the **show ip bgp _prefix_** command on the remote site router to see the impact of the MED settings:

{{<cc>}}BGP paths toward the Web LAN on the Site-A router (best route through *CoreInet*){{</cc>}}
```
Site-A#show ip bgp 10.0.21.0
BGP routing table entry for 10.0.21.0/24, version 22
Paths: (2 available, best #1, table Default-IP-Routing-Table)
  65000
    10.0.11.1 from 10.0.11.1 (10.0.1.2)
      metric 200, localpref 100, valid, external, best
  65000
    10.0.8.1 from 10.0.8.1 (10.0.1.3)
      metric 300, localpref 100, valid, external
```

{{<cc>}}BGP paths toward the Legacy LAN on the Site-A router (best route through *CoreFR*){{</cc>}}
```
Site-A#show ip bgp 10.0.20.0
BGP routing table entry for 10.0.20.0/24, version 13
Paths: (2 available, best #2, table Default-IP-Routing-Table)
  65000
    10.0.11.1 from 10.0.11.1 (10.0.1.2)
      metric 200, localpref 100, valid, external
      Community: 65000:100
  65000
    10.0.8.1 from 10.0.8.1 (10.0.1.3)
      metric 100, localpref 100, valid, external, best
      Community: 65000:100
```

You could set the MED with an access-list or a prefix-list on the *CoreFR* router, but a more scalable approach would use BGP communities:

* The originating router (the *Legacy* router in our network) would set a BGP community (65000:100 is used in the sample network) to indicate that the IP prefix belongs to the legacy servers
* The *CoreFR* router would use the community to set the MED values. 

{{<figure src="legacy-route-propagation.jpg" caption="BGP route propagation from the Legacy router to the Site router">}}

<!-- end -->
