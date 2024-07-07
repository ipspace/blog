---
date: 2014-03-17 07:36:00+01:00
dmvpn_tag: routing
tags:
- DMVPN
- BGP
title: Scaling BGP-Based DMVPN Networks
url: /2014/03/scaling-bgp-based-dmvpn-networks/
---
Cristiano sent me an interesting question:

> I saw that to configure BGP as the routing protocol running over DMVPN I have to configure BGP neighbors on the hub site router. Do I really have to configure all the neighbors on the hub site? How many neighbors could I configure? How can I scale that?

According to Cisco Live presentations, [BGP-over-DMVPN](/2011/01/using-bgp-in-phase-1-dmvpn-network/) scales to several thousand spoke sites (per hub router), so you shouldn't be too worried about the protocol scalability. Configuring all those neighbors is a different issue.
<!--more-->
Fortunately, anonymous BGP neighbors (which were banned from Cisco IOS years ago) reappeared in a different disguise ([dynamic BGP neighbors](http://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/15-mt/irg-15-mt-book/irg-dynamic-neighbor.html)) in IOS release 15.1T -- you can configure an access list which defines whether the remote IP address is a valid BGP neighbor, and accept all incoming TCP requests on port 179 matched by the ACL. The "only" drawback: dynamic neighbors matched by a single **bgp listen peer-group** command must share the same neighbor parameters, including an AS number.

{{<note>}}You can list several AS numbers in the **neighbor** ***peer-group*** **remote-as** command, but that doesn't exactly help you if you have 500 remote sites.{{</note>}}

Faced with the requirement to have the same AS number on all remote sites you could use one of these two designs:

**Running IBGP across DMVPN**. While you *could* make it work (even easier now that Cisco [tweaked its BGP route reflector behavior](/2014/04/changes-in-ibgp-next-hop-processing/)), I wouldn't recommend doing that unless you're a BGP guru. [IBGP was not designed to be used without IGP](/2011/08/ibgp-or-ebgp-in-enterprise-network/), and there are simply too many things that can bite you if you're trying to run IBGP without an underlying IGP. You probably don't want to run an IGP across a large DMVPN network or you wouldn't be reading this blog post.

**Running EBGP across DMVPN** with all spoke sites being in the same autonomous system. This design works great for Phase 1 or Phase 3 DMVPN: spoke sites will ignore routes advertised by other spoke sites (due to BGP loop prevention logic), and a default route advertised by the hub router will take care of the inter-site traffic flow.

Phase 2 DMVPN is trickier; every spoke site should have routes from all other spoke sites (with correct BGP next hops) if you want spoke sites to communicate directly. You can disable BGP loop prevention logic on spoke sites (using **neighbor allowas-in**) or play dirty tricks with the AS path like **neighbor remove-private-as** or **neighbor as-override** on the hub router (not recommended).

### More Information

-   [*BGP routing in DMVPN Access Networks*](http://www.ipspace.net/BGP_Routing_in_DMVPN_Access_Network) case study;
-   DMVPN webinars: [buy them individually](http://www.ipspace.net/Roadmap/VPN_webinars), or [in a bundle](http://www.ipspace.net/DMVPN_trilogy).
