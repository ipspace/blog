---
comment: 'After the initial OpenFlow-related blog posts, the OpenFlow pundits quickly
  labeled me an OpenFlow hater, but I was just my grumpy old self ;) Here’s the blog
  post (from May 2011) that tried to set the record straight (not that such things
  would ever work).


  In the meantime, the whole argument became moot -- OpenFlow is mostly dead and forgotten
  -- but the "_don''t expect miracles_" message is as relevant today as it''s ever
  been.

  '
date: 2011-05-27 06:03:00+00:00
lastmod: 2022-07-06 14:40:00
sdn_hype_tag: initial
series:
- sdn_hype
tags:
- OpenFlow
title: 'For the Record: I Am Not Against OpenFlow ...'
url: /2011/05/for-record-i-am-not-against-openflow.html
---
... as some of its supporters seem to believe every now and then (I do get severe allergic reaction when someone claims it will [change the laws of physics](/2011/03/open-networking-foundation-fabric.html) or when I'm faced with [technical inaccuracies peddled by an Instant Expert](https://web.archive.org/web/20111018065642/https://www.networkworld.com/news/2011/052511-openflow-expert.html) not to mention [knee-jerking financial experts](https://www.barrons.com/articles/BL-TB-32802)). Even more, assuming it can [cross the adoption gap](http://etherealmind.com/openflow-why-it-can-cross-the-adoption-gap/)[^DN], it could fundamentally change the business models of networking vendors (maybe not in the way you'd like them to be changed). 

On the more technological front, I still don't expect to see miracles. Most OpenFlow-related ideas I've heard about have been tried (and failed) before. I fail to see why things would be different just because we use a different protocol to program the forwarding tables.

I wrote about my OpenFlow views in an article that was published on SearchNetworking.com in 2011. That article is long gone, so I'm including in this blog post.

[^DN]: Hint: It did not.

---

If you haven’t spent the last few weeks on a forgotten island with no satellite phone coverage, you’ve probably noticed the spiking levels of hype surrounding the newest internetworking technology OpenFlow. The networking industry is obviously in dire need of the next big thing. The last time I saw something similar to this was in the early 2000s when MPLS was supposed to solve every internetworking problem ever envisioned. In those days the levels of hype were so high that someone wrote an April 1st RFC describing the use of MPLS for electricity transport.

Like MPLS, OpenFlow won’t bring world peace, cure cancer or discover alien civilizations. It might, however, help change the internetworking environment in the same way Unix and Linux changed the operating system landscape by providing a standard way of configuring forwarding tables in a distributed switching architecture.

But that doesn't account for the explosion of OpenFlow announcements at Interop. After all, OpenFlow was an unknown academic toy only a few months ago. In fact, the speed with which vendors were able to throw together a proof-of-concept code indicates one of the drawbacks of OpenFlow: it’s a simple low-level API (some people are comparing it to BIOS). The hard part of the exercise will be writing the controller software that everyone is already raving about. But that won't be easy. Networking vendors have invested thousands of man-years into similar efforts. So those that expect revolutionary new controller applications appearing out of the blue sky probably also believe in tooth fairy and unicorn tears.

One of the most extreme analogies I’ve heard so far compared OpenFlow to a C compiler. Instead of using off-the-shelf applications, now we have the ability to develop our own. This might be true, but someone still has to develop these applications, test them and make sure they scale, which is one of the biggest hurdles OpenFlow has to cross. Meanwhile, vendors are already touting controller applications as the “magic” ingredient, but I wouldn't expect miracles. As technical guru and professor Scott Shenker explained: “[OpenFlow] doesn't let you do anything you couldn't do on a network before.”

Moreover, even if OpenFlow were comparable to a C compiler, we haven’t seen an explosion of database packages or spreadsheet programs just because we have a C compiler. A few vendors own the majority of the market in each application segment, and the OpenFlow controller landscape might look very similar in a few years. There will likely be a few makers of commoditized hardware based on common merchant silicon and a few software vendors (probably including Cisco, Juniper and VMware) providing the vast majority of the controller nodes. And just in case you still believe OpenFlow will bring down prices and shrink the fat margins of some internetworking companies, take a brief look at Oracle’s financial reports.

### Still Want to Know More about OpenFlow?

If you're keen on figuring out how an obsolete protocol worked, you'll find all the gory details in the OpenFlow Deep Dive webinar. If you're more interested in real-life solutions, explore other [SDN](https://www.ipspace.net/SDN) or [network automation](https://www.ipspace.net/Roadmap/Network_Automation_webinars) webinars.

### Revision History

2022-07-06
: Added the OpenFlow article to the blog post

