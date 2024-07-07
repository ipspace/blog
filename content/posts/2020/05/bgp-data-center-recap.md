---
title: "Explore: BGP in Data Center Fabrics"
date: 2020-05-04 06:58:00
tags: [ BGP, data center, design ]
---
Got mentioned in [this tweet](https://twitter.com/vpackets/status/1253371082788220929?s=11) a while ago:

> Watching @ApstraInc youtube stream regarding BGP in the DC with @doyleassoc and @jtantsura.Maybe BGP is getting bigger and bigger traction from big enterprise data centers but I still see an IGP being used frequently. I am eager to have @ioshints opinion on that hot subject.

Maybe I've missed some breaking news, but assuming I haven't my opinion on that subject hasn't changed.
<!--more-->
I've been writing, talking, and teaching about various aspects of using BGP in data center fabrics (including "_do we really need it_") for almost a decade, and I know it's hard to collect all that information, so I did it for you in ipSpace.net [BGP in Data Center Fabrics resource page](/series/dcbgp/).

As for the hotness of the topic: 

* It was hot when [Petr Lapukhov presented the first idea at NANOG](https://archive.nanog.org/sites/default/files/wed.general.brainslug.lapukhov.20.pdf) in 2013 or [described how to build scalable data centers with BGP in May 2016](https://www.youtube.com/watch?v=yJbqnOdD3cg), but maybe not when a startup decides to use it to promote their product in 2020.
* It turned into a lemming run with many data center switching vendor [promoting it as the best thing invented since sliced bread](/2017/11/bgp-as-better-igp-when-and-where/).
* When [combined with EVPN on an old BGP code base](/2020/02/the-evpnbgp-saga-continues/) it usually gets so complex that you need an automation solution on top of it to stay sane (notable exception: FRRouting).

No wonder Apstra sees BGP-only data centers as a gift from networking gods ;)

{{<jump>}}[BGP in Data Center Fabrics](/series/dcbgp/){{</jump>}}