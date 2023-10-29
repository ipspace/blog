---
title: "Video: Hacking BGP for Fun and Profit"
date: 2023-11-03 07:16:00
tags: [ BGP, security, video ]
---
At least some people learn from others' mistakes: using the concepts proven by some [well-publicized BGP leaks](https://blog.ipspace.net/2023/10/video-history-bgp-route-leaks.html), malicious actors quickly figured out how to [hijack BGP prefixes for fun and profit](https://my.ipspace.net/bin/get/Net101/NS5.2%20-%20Hacking%20BGP%20for%20Fun%20and%20Profit.mp4?doccode=Net101).

Fortunately, those shenanigans wouldn't spread as far today as they did in the past -- according to [RoVista](https://rovista.netsecurelab.org/), most of the largest networks block the prefixes Route Origin Validation (ROV) marks as invalid.

**Notes:**

* ROV cannot stop all the hijacks, but it can identify more-specific-prefixes hijacks (assuming the [origin AS did their job right](https://datatracker.ietf.org/doc/html/rfc9319)).
* You'll find more [Network Security Fallacies videos](https://my.ipspace.net/bin/list?id=Net101#NETSEC) in the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.

{{<jump>}}[Watch the video](https://my.ipspace.net/bin/get/Net101/NS5.2%20-%20Hacking%20BGP%20for%20Fun%20and%20Profit.mp4?doccode=Net101){{</jump>}}
{{<note free>}}You need at least [free ipSpace.net subscription](https://www.ipspace.net/Subscription/Free) to watch videos in this webinar.{{</note>}}
