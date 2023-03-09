---
date: 2019-01-07 08:31:00+01:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- bridging
- network management
- high availability
title: Large Layer-2 Domains Strike Again…
url: /2019/01/large-layer-2-domains-strike-again.html
---
I started January 2018 blogging with a [major service provider failure](https://blog.ipspace.net/2018/01/fat-fingers-strike-again.html). Why should 2019 be any different? Here's what [Century Link claimed was causing two-day outage](https://twitter.com/briankrebs/status/1079135599309791235) ([more comments here](https://twitter.com/GossiTheDog/status/1079144491238469638)).

Supposedly it was a [problem with the management network used by their optical gear](https://twitter.com/stubarea51/status/1079423228437823488), but it looks a lot like a [layer-2 network spanning 15 data centers](https://twitter.com/cmsirbu/status/1079173861940387840) and no control-plane policing on the managed devices... proving yet again that large-scale layer-2 networks are a really bad idea.
<!--more-->
Please note that it doesn't matter whether they had problems with a stretched Ethernet segment or something else. According to their explanation a single device broadcasting packets was able to affect devices across multiple locations -- as I'm trying to explain for years (not that many people would listen and/or care), a [single broadcast domain is a single failure domain](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html) no matter what \$vendor PowerPoints or whitepapers claim, and it's not a question of *whether* the concoction will fail but *when*. Keep that in mind the next time your \$vendor rep brings dancing unicorns into the room.

{{<note>}}On a tangential note, cloud providers that know what they're doing don't support anything else but unicast routing for a really good reason -- check out the details in [AWS Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar.{{</note>}}

Finally, just in case you think failures like this one are a black swan event, check the [list of post-mortems](https://github.com/danluu/post-mortems) and [associated lessons learned](http://danluu.com/postmortem-lessons/) collected by [Dan Luu](https://danluu.com/about/)... keeping in mind that most of the failures are never reported.
