---
date: 2018-04-20 08:36:00+02:00
dcbgp_tag: newrp
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_89-OpenFabric.mp3
series:
- dcbgp
series_title: OpenFabric with Russ White
series_weight: 850
tags:
- podcast
- data center
- fabric
- IP routing
- Software Gone Wild
title: OpenFabric with Russ White on Software Gone Wild
url: /2018/04/openfabric-with-russ-white-on-software.html
---
Continuing the series of [data center routing protocol podcasts](/2018/03/data-center-routing-with-rift-on.html), we sat down with Russ White (of the CCDE fame), author of another proposal: [OpenFabric](https://tools.ietf.org/html/draft-white-openfabric-05).

As always, we started with the "*what's wrong with what we have right now, like using BGP as a better IGP*" question, resulting in "*BGP is becoming the trash can of the Internet*".
<!--more-->
You can probably guess the next set of intro questions: \"*Do we need policies and traffic engineering in a high-speed data center fabric?*"

Finally, we got to discussing OpenFabric, starting with how OpenFabric uses link-state database to modify IS-IS flooding behavior and thus reduces the total amount of flooding in a data center fabric. Next step: how do you know where it's safe to reduce flooding? You have to figure out whether you're a leaf or spine, and there are two ways in OpenFabric to solve that challenge.

Of course, we couldn't possibly stay on track, so there was a brief diversion into virtual aggregation, application-level IP address huggers and local area IP address mobility with ARP... but quickly got back to more OpenFabric goodness including how it uses [Segment Routing](http://www.ipspace.net/Segment_Routing_Introduction).

Interested? Listen to [Episode 89](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_89-OpenFabric.mp3) of [Software Gone Wild](http://www.ipspace.net/Podcast/Software_Gone_Wild).

{{<jump>}}
[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_89-OpenFabric.mp3)
{{</jump>}}

More to explore:

-   [OpenFabric IETF draft](https://tools.ietf.org/html/draft-white-openfabric-05)
-   [Related IS-IS extensions](https://tools.ietf.org/html/draft-shen-isis-spine-leaf-ext-05)
-   [Leaf-and-spine fabric architectures and designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)
-   [Designing and building Data Center fabrics](http://www.ipspace.net/Designing_and_Building_Data_Center_Fabrics)
