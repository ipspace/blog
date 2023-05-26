---
date: 2009-08-03 06:39:00+02:00
tags:
- OSPF
title: 'Router LSA Quiz: The Results'
url: /2009/08/router-lsa-quiz-results.html
---
The [Friday's OSPF quiz](https://blog.ipspace.net/2009/07/quick-quiz-ospf-lsa-generation.html) has generated numerous answers ... unfortunately many of them incorrect. Some readers (probably those that recently attended a Cisco certification exam) thought I was asking a trick question, as I've forgotten to include the IP addresses in the sample configuration, which only proves how hard it is to write good bulletproof questions.

Those that assumed the IP addresses would have to be configured on the interfaces made two common errors:

-   Some assumed a type-2 LSA would be generated for the LAN interface. Wrong: type-2 LSA is generated only if needed (there is more than one router attached to the LAN interface).
-   Others thought the router would generate a type-1 LSA per interface. Wrong: an OSPF router generates only a single type-1 LSA per area.

To clarify these issues, I wrote an article [documenting how the type-1 (router) LSA describes various interface types and inter-router links](/kb/tag/OSPF/Type-1-LSA.html).

{{<jump>}}[Keep reading](/kb/tag/OSPF/Type-1-LSA.html){{</jump>}}
