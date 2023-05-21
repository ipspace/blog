---
title: "Modifying BGP Behavior with xBGP API"
date: 2023-05-09 06:49:00
tags: [ BGP ]
---
When I reposted a link to *[xBGP: Faster Innovation in Routing Protocols](https://nsg.ee.ethz.ch/fileadmin/user_upload/publications/xbgp_nsdi23spring-final.pdf)* paper, someone immediately replied

> Quite interesting, but it feels like this could become the proverbial 15th standard. 

xBGP is an API that allows BGP users to implement routing policies (route selection, filtering, or propagation) that use attributes or mechanisms defined in newer IETF RFCs or drafts, so the [proverbial 15th standard](https://xkcd.com/927/) is not that far off the mark. However, we must remember that what we call BGP is more than just a set of competing standards.
<!--more-->
We have the session management and transport protocol at the lowest layer of the BGP application stack. We could compare them to a relational database synchronization protocol[^BD] (more precisely, log shipping, as the changes made to the local data structures get propagated after the local BGP speaker has evaluated them). That part of the BGP protocol stack is pretty mature[^PMT] and rarely changes.

[^BD]: Apart from the "delete all information you received from a neighbor when the session with that neighbor fails" bit. There's also "actually, don't do that, let's wait for that neighbor to recover" gotcha, better known as Graceful Restart.

[^PMT]: Apart from "minor" fixes like "don't throw away a million routes the moment you get a weird incoming update."

BGP routers store incoming information in a BGP table. Like individual tables in a relational database, the BGP table could have numerous address families[^PK]. RFCs describing new address families are more common than those changing the transport protocol, but even there, we get a new address family every decade or so.

[^PK]: The unique primary key for an address family is the NLRI + remote router ID. BGP implementations could also use NLRI as the secondary index to speed up the lookups.

Like every table in a relational database has columns, BGP prefixes stored in a BGP table have attributes. Some of those are well-known and static; many RFCs and drafts define optional attributes. Dealing with new optional attributes is one of the main strengths of xBGP: using eBPF bytecode running in an eBPF virtual machine, you can specify how to use them in routing policies.

The ultimate goal of BGP is to select the best paths toward all destinations in a BGP address family -- you could compare that to a `SELECT DISTINCT` SQL query with a convoluted `MAX` function or `ORDER BY` clause. xBGP allows you to modify that function and use the optional BGP attributes not supported by the underlying BGP daemon to modify route selection rules.

Will we see xBGP in production networks? I hope so, and the BIRD and FRR implementations already allow daring operators to implement novel routing policies on route reflectors running open-source software. Want to test it in a lab? [netlab](https://netlab.tools/) supports FRR containers, but you'll have to find a custom container image running FRR with the xBGP hooks.
