---
date: 2011-10-19 07:15:00+02:00
series:
- bgp-essentials
tags:
- BGP
title: BGP and Route Maps
url: /2011/10/bgp-and-route-maps/
---
This is a nice email I got from an engineer struggling with multi-homing BGP setup:

> We faced a problem with our internet routers a few days back. The engineer who configured them earlier used the syntax: **network x.x.x.x mask y.y.y.y route-map PREPEND** to influence the incoming traffic over two service-providers.

\... and of course it didn't work.
<!--more-->
> We weren\'t getting the desired results so I changed the configuration from up above to: **neighbor x.x.x.x route-map PREPEND** and to my surprise everything started working fine as before. Is there a difference between to the two sets of configuration?

The **network route-map** command uses a route map to change the attributes of an IP prefix as it's inserted in the BGP table. On Cisco IOS you can use that route map to set BGP communities and change MED, local preference and next hop (I wouldn't change the next hop), but not AS-path. If the **route-map** doesn't match the IP prefix, the attributes are not changed (but I wouldn't use a route-map with a match statement in the network command anyway).

**Neighbor route-map** **in\|out** command applies a route map to BGP updates received or sent to a neighbor. It's not just an attribute modifying tool, it's also a filter -- if the route map doesn't match a BGP prefix, the inbound update gets dropped before it's inserted in the BGP table, or the BGP prefix never gets sent to the BGP neighbor.

Route map applied to a BGP neighbor can change most BGP attributes that make sense (example: you cannot change local preference if the neighbor is not in the same AS) and prepend AS numbers to the AS path (you're not allowed to modify AS path directly, as that might bypass BGP loop prevention mechanisms).

On top of obvious sanity checks, the router applies the usual [BGP route reflector safeguards](/2008/08/bgp-route-reflector-details/): if the neighbor is a route reflector client, you cannot change any attributes of reflected routes with an outbound route-map (but you can change attributes of routes you've received from EBGP neighbors). 

If you want to change attributes of IBGP prefixes sent to route reflector clients, you have to modify them as you receive them from other neighbors with inbound route-maps.

{{<figure src="/2011/10/s1600-note.png" caption="A quick summary of how BGP uses route maps">}}

{{<note warn>}}Later versions of Cisco IOS slightly modified that behavior; do at least a quick lab test before relying on border cases in your network design.{{</note>}}
