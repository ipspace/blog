---
title: "Worth Reading: Another BGP Session Reset Bug"
date: 2023-07-02 06:24:00
tags: [ worth reading, BGP ]
---
[Emile Aben](https://labs.ripe.net/author/emileaben/) is [describing an interesting behavior](https://labs.ripe.net/author/emileaben/unknown-attribute-28-a-source-of-entropy-in-interdomain-routing/) observed in the Wild West of the global Internet: someone started announcing BGP paths with an unknown attribute, which (regardless of [RFC 7606](https://www.rfc-editor.org/rfc/rfc7606)) triggered some BGP session resets. 

One would have hoped we learned something from the [August 2010 incident](https://labs.ripe.net/author/erik/ripe-ncc-and-duke-university-bgp-experiment/) ([supposedly caused by a friend of mine](/2023/03/chatgpt-bgp-routing-security/) 😜), but it looks like some things never change. For more details, watch the [Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC) and [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar.