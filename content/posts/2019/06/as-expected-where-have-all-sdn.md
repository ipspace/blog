---
date: 2019-06-07 07:07:00+02:00
distributed-systems_tag: openflow
series:
- distributed-systems
tags:
- SDN
title: 'As Expected: Where Have All the SDN Controllers Gone?'
url: /2019/06/as-expected-where-have-all-sdn.html
---
Roy Chua (SDx Central) published a blog post titled "[Where Have All the SDN Controllers Gone](https://www.sdxcentral.com/articles/analysis/where-have-all-the-sdn-controllers-gone/2019/03/)" a while ago describing the gradual disappearance of SDN controller hype.

No surprise there - some of us were [pointing out the gap between marketing and reality](https://blog.ipspace.net/2015/12/running-open-daylight-in-production.html) years ago.

It was evident to anyone familiar with how [networking actually works](https://www.ipspace.net/How_Networks_Really_Work) that in a generic environment the drawbacks of [orthodox centralized control plane SDN approach](https://blog.ipspace.net/2014/01/what-exactly-is-sdn-and-does-it-make.html) far outweigh its benefits. There are special use cases like [intelligent patch panels](https://blog.ipspace.net/2015/12/running-open-daylight-in-production.html) where a centralized control plane makes sense.
<!--more-->
There are applications like [traffic engineering](https://blog.ipspace.net/2012/02/bandwidth-on-demand-is-openflow-silver.html) where central visibility (but not centralized control plane) makes sense. There are environments where [treating the whole network as a single box](https://blog.ipspace.net/2018/02/single-image-systems-or-automated.html) is acceptable (see also: Juniper's [Virtual Chassis Fabric](https://blog.ipspace.net/2013/11/finally-juniper-supports-leaf-and-spine.html)). Is that good enough to support multiple controller ecosystems? Obviously not - in most cases, automation and abstraction give you better results without having to deal with a newly-reinvented wheel.

Then there are the hardware challenges. Early SDN controllers tried to push a square peg into a round hole and failed miserably or required a [vertically-integrated stack](https://blog.ipspace.net/2015/06/vertically-integrated-musings.html) that defied the whole idea of the original SDN religion (as opposed to what \$vendor marketers made out of the term).

Controllers that were [designed to do useful work in real-life networks](https://blog.ipspace.net/2019/04/using-faucet-to-build-sc18-network-with.html) like [Faucet](https://faucet.nz/) have limited [Hardware Compatibility List](https://docs.faucet.nz/en/latest/vendors/index.html) - once you figure out [all the OpenFlow functionality you need to get the job done](https://docs.faucet.nz/en/latest/architecture.html#faucet-openflow-switch-pipeline), you realize there are only a few switches on the market that have it all.

Finally, there's the Open Daylight's *kitchen sink* approach turning what might have been a potentially interesting platform into a [quagmire of dependencies](https://blog.ipspace.net/2018/05/the-difference-between-hodgepodge-poc.html) that could do things like *HTTP-to-BGP-LS* or *HTTP-to-NETCONF* protocol translation - obviously not enough to survive.

Now that the last vestiges of SDN controller hype are fading, we might start considering solutions that solve actual production challenges instead of fueling vendor marketing machinery. Like always, it took us almost a decade to wake up from unicorn dust induced haze. We never learn from past mistakes, do we?

{{<note>}}
If you're interested in how Nick Buraglio uses Faucet in production networks, listen to [Episode 101](https://blog.ipspace.net/2019/04/using-faucet-to-build-sc18-network-with.html) of [Software Gone Wild](https://www.ipspace.net/Podcast/Software_Gone_Wild).
{{</note>}}
