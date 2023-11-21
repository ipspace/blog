---
title: "Why Do We Need BGP Identifiers?"
date: 2023-11-22 07:29:00
tags: [ BGP ]
---
A friend of mine sent me an interesting question along these lines:

> We all know that in OSPF, the router ID is any 32-bit number, not necessarily an IP address of an interface. The only requirement is that it must be unique throughout the OSPF domain. However, I've always wondered what the role of BGP router ID is. RFC 4271 says it should be set to an IP address assigned to that BGP speaker, but where do we use it?

Also, he observed somewhat confusing behavior in the wild:

> Take two routers and configure the same BGP identifier on both. Cisco IOS will not establish a session, while IOS XR and Junos will.

I decided to take the challenge and dug deep into the bowels of [RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271) and [RFC 6286](https://datatracker.ietf.org/doc/html/rfc6286). Here's what I brought back from that rabbit hole:
<!--more-->
* RFC 4271 defines the _BGP identifier_ as "an IP address assigned to the router," but RFC 6286 [modifies its meaning](https://datatracker.ietf.org/doc/html/rfc6286#section-2.1) as "a 4-octet unsigned non-zero integer that should be unique within an AS," nicely bypassing the question "_What should BGP identifier be on an IPv6-only network?_" 
* RFC 4271 uses BGP identifier solely to figure out [which TCP session](https://datatracker.ietf.org/doc/html/rfc4271#section-6.8) to tear down when a pair of BGP routers simultaneously try to establish a TCP session *between the same IP addresses*. The session collision mechanism *is not used* for BGP sessions over parallel links.

RFC 6286 describes [other uses of BGP identifier](https://datatracker.ietf.org/doc/html/rfc6286#section-3):

* It is used to document who aggregated a prefix (the AGGREGATOR attribute)
* BGP route reflectors use it to document who brought the route into the autonomous system (ORIGINATOR_ID) and who reflected it (CLUSTER_LIST).

{{<note warn>}}Having duplicate BGP identifiers within an autonomous system using route reflectors might result in an interesting troubleshooting exercise.{{</note>}}

As for the "_routers allow duplicate BGP identifiers on a BGP session_" claim:

* RFC 4271 assumes a certain amount of common sense and does not address this corner case.
* The authors of RFC 6286 dropped that _people building networks should have some common sense_ assumption. The RFC requires the BGP identifiers to be unique _within the autonomous system._ An IBGP session between routers with the same BGP identifier should be rejected, while an EBGP session is perfectly OK.
* RFC 6286 also describes the [tie-breaker in case you have an EBGP session between devices with the same BGP identifier](https://datatracker.ietf.org/doc/html/rfc6286#section-2.3): the session initiated by the router with the higher AS number is preserved.

Now that you know how things should work, set up a small lab using [this topology](https://github.com/ipspace/netlab-examples/blob/master/BGP/Sessions/router_id.yml) and run the tests for devices you care about. Although all three routers have the same BGP identifier, the EBGP session should come up, and the IBGP session should be reset with the "Bad BGP ID" notification.

I ran the test with Arista cEOS, Cisco IOSv, Cisco IOS-XE (CSR 1000v), and FRR. Arista cEOS and FRR follow RFC 6286; Cisco IOSv and IOS XE are too edgy and reject an EBGP session from a peer with a duplicate BGP identifier.

