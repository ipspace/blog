---
cdate: 2022-07-10
comment: 'It’s reasonably easy to add automation and orchestration on top of existing
  network implementation. Throwing away decades of field experience and replacing
  existing solutions with an OpenFlow-based controller is a totally different story
  as I explained in May 2013.


  In the meantime, most projects trying to implement centralized  control plane turned
  into abandonware -- it turns out it''s too hard to reinvent all the wheels even
  if you''re a networking vendor or VC-funded startup -- and [Open Daylight got nowhere](/2017/05/is-anyone-using-open-daylight/).

  '
date: 2013-05-23 07:07:00+02:00
sdn_101_tag: extra
series:
- sdn_101
series_weight: 100
tags:
- SDN
- OpenFlow
title: OpenFlow and SDN – Do You Want to Build Your Own Racing Car?
url: /2013/05/openflow-and-sdn-do-you-want-to-build/
---
The OpenFlow zealots are quick to point out the beauties of the centralized control plane, and the huge savings you can expect from using commodity hardware and open-source software. What they usually forget to tell you is that you also have to reinvent all the wheels the networking industry has invented in the last 30 years.
<!--more-->
Imagine you want to build your own F1 racing car \... but the only component you got is a super-duper racing engine from Mercedes Benz[^MB]. You\'re left with the \"easy\" task of designing the car body, suspension, gears, wheels, brakes and a few other choice bits and pieces. You can definitely do all that if you\'re [Google](/2012/05/openflow-google-brilliant-but-not/) or [McLaren team](http://en.wikipedia.org/wiki/McLaren), but not if you\'re a Sunday hobbyist mechanic. No wonder some open-source OpenFlow controllers look like [Red Bull Flugtag contestants](https://www.redbull.com/us-en/tags/flugtag).

[^MB]: Forgetting for the moment how badly Mercedes cars performed in the 2022 F1 season ;)

Does that mean we should ignore OpenFlow? Absolutely not, but unless you want to become really fluent in real-time event-driven programming (which might look great on your resume), you should join me watching from the sidelines until there\'s a solid controller (maybe we\'ll get it with [Open Daylight](/2013/04/the-first-glimpse-of-open-daylight/), [Floodlight](/2012/08/openstackquantum-sdn-based-virtual/) definitely doesn\'t fit the bill) and some application architecture blueprints.

Till then, it might make sense to focus on [more down-to-earth technologies](/2013/04/the-many-paths-to-sdn/); after all, you don\'t exactly need [OpenFlow and a central controller](https://web.archive.org/web/20131103030052/http://jedelman.com/1/post/2013/04/goldman-sachs-is-deploying-sdn-are-you.html) to solve real-life problems, like Tail-f clearly demonstrated with their [NCS software](/2013/05/tail-f-network-control-system-first/).
