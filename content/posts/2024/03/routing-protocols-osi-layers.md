---
title: "OSI Layers in Routing Protocols"
date: 2024-03-26 06:53:00+0100
tags: [ networking fundamentals ]
---
Now and then, someone [rediscovers that IS-IS does not run on top of CLNP or IP](https://blog.ipspace.net/2009/06/is-is-is-not-running-over-clnp.html) and claims that, therefore, it must be a layer-2 protocol. Even [vendors' documentation](https://www.juniper.net/documentation/us/en/software/junos/is-is/topics/concept/isis-layer2-mapping.html) is not immune.

Interestingly, most routing protocols span the whole seven layers of the OSI stack, with some layers implemented internally and others offloaded to other standardized protocols.
<!--more-->
No routing protocol reinvents **physical** or **data link** layers. If it did, you couldn't run it inline (on the same links as the user traffic).

IS-IS uses its own **network** layer. OSPF, EIGRP, RIP, and BGP run on top of IP[^ARCNET].

[^ARCNET]: That's why you can run OSPF but not IS-IS over [ARCNET](https://www.rfc-editor.org/rfc/rfc1201.html).

{{<note info>}}That does not make IS-IS a layer-2 protocol. If anything, you could call it a layer-3 protocol, OSPF a layer-4 protocol, and BGP a layer-5 protocol. But seriously, whatever.{{</note>}}

OSPF and EIGRP use their own **transport** layers to implement reliable packet delivery. RIP uses UDP and hopes for the best, and BGP uses TCP because you can't fool around when dealing with a million table entries.

Most routing protocols have a **[session](https://en.wikipedia.org/wiki/Session_layer)** layer. The session layer provides mechanisms for managing sessions between applications, synchronization points, and resynchronization. The HELLO messages and keepalives clearly belong to this layer. You might even claim that the OSPF database exchange phase provides a resynchronization service.

Every single routing protocol defines data structures that are exchanged between adjacent routers. Somehow, these data structures have to be sent over the transport layer connection, and at least those protocols using TLVs have a **[presentation](https://en.wikipedia.org/wiki/Presentation_layer)** layer. Even the convention that the bytes of the IP addresses are sent in *[network order](https://en.wikipedia.org/wiki/Endianness#Networking)* is a presentation-layer convention.

Finally, we're getting to the **application** layer -- a distributed database of reachability information that the routers can use to build their forwarding tables.

Want to know more? Explore [routing protocols](https://my.ipspace.net/bin/list?id=Net101#ROUTING) section of the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.