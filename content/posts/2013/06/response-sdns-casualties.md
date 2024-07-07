---
cdate: 2022-07-10
comment: "Every now and then, someone generates clickbait content recycling the \"\
  _networking engineers are a dying breed_\" hype. \n\nHere's what I wrote as a response\
  \ to a particular instance of that stupidity in 2013. Not surprisingly, networking\
  \ engineers are doing well in 2022, marketing VPs are still generating nonsense,\
  \ and the author of that article probably still keeps spreading it.\n\nIn related\
  \ news (from July 2022 perspective):\n\n* NEC ProgrammableFlow disappeared\n* [So-called\
  \ SDN controllers are everywhere](/2022/05/sdn-controller-taxonomy/) (including\
  \ campus and wireless), but they are mostly just another layer of complexity on\
  \ top of the networking infrastructure. We called those things \"network management\
  \ systems\" before SDN was cool.\n* We're still dealing with VLANs\n"
date: 2013-06-12 07:20:00+02:00
sdn_101_tag: extra
series:
- sdn_101
series_weight: 80
tags:
- SDN
title: 'Response: SDN’s Casualties'
url: /2013/06/response-sdns-casualties/
---
An individual focused more on sensationalism than content deemed it appropriate to [publish an article](http://www.theregister.co.uk/2013/05/24/network_configuration_automation/) declaring networking engineers an endangered species on an industry press web site that I considered somewhat reliable in the past.

The resulting flurry of expected blog posts included an [interesting one from Steven Iveson](http://packetpushers.net/youve-changed-sdns-casualties/) in which he made a good point: it's easy for the *cream-of-the-crop* not to be concerned, but what about others lower down the pile. As always, it makes sense to do a bit of reality check.
<!--more-->
-   While everyone talks about SDN, the products are scarce, and it will take years before they'll appear in a typical enterprise network. Apart from NEC's Programmable Flow and overlay networks, most other SDN-washed things I've seen are still point products.
-   Overlay virtual networks seem to be the killer app of the moment. They are extremely useful and versatile \... if you're not bound to VLANs by physical appliances. We'll have to wait for at least another refresh cycle before we get rid of them.
-   Data center networking is hot and sexy, but it's only a part of what *networking* is. I haven't seen a commercial SDN app for enterprise WAN, campus or wireless (I'm positive I'm wrong -- write a comment to correct me), because that's not where the VCs are looking at the moment.

Also, consider that the *my job will be lost to technology* sentiments [started approximately 200 years ago](http://en.wikipedia.org/wiki/Swing_Riots) and yet the population has increased by [almost an order of magnitude](http://en.wikipedia.org/wiki/World_population_estimates) in the meantime, there are obviously way more jobs now (in absolute terms) than there were in those days, and nobody in his right mind wants to do the menial chores that the technology took over.

Obviously you should be worried if you're a VLAN provisioning technician. However, with everyone writing about SDN you know what's coming down the pipe, and you have a few years to adapt, expand the scope of your knowledge, and figure out where it makes sense to move (and don't forget to focus on where you can add value, not what job openings you see today). If you don't do any of the above, don't blame SDN when the VLANs (finally) join the dinosaurs and you have nothing left to configure.

Finally, I'm positive there will be places using VLANs 20 years from now. After all, [AS/400s and APPN are still kicking](http://it20.info/2012/09/cloud-and-the-three-it-geographies-silicon-valley-us-and-rest-of-the-world/) and people are still fixing COBOL apps (that [IBM made sexier with XML and Enterprise JavaBeans integration](https://www.computerworld.com/article/2564558/ibm-looks-to-modernize-cobol.html)).
