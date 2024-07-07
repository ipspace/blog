---
date: 2019-04-24 08:59:00+02:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- bridging
- data center
- high availability
title: How Common Are Data Center Meltdowns?
url: /2019/04/how-common-are-data-center-meltdowns/
---
We all know about catastrophic headline-generating failures like AWS East-1 region falling apart or a [major provider being down for a day or two](/2019/01/large-layer-2-domains-strike-again/). Then there are failures known only to those who care, like [losing a major exchange point](/2015/06/another-spectacular-layer-2-failure/). However, I'm becoming more and more certain that the known failures are not even the tip of the iceberg -- they seem to be [the climber at the iceberg summit](https://www.redbull.com/int-en/videos/climbing-icebergs-in-greenland-klemen-premrl-and-aljaz-anderle).
<!--more-->
I'm occasionally running on-site design workshops and although I don't keep track, my guess is that at least 25% of the companies I'm running workshops in experienced a more-or-less catastrophic bridging-caused meltdown in not-so-distant past. Sometimes it stays within a data center and impacts the performance of all hosts attached to the affected VLAN, sometimes they manage to bring down two data centers (hooray for Stretched VLANs).

It might be [selection bias](https://en.wikipedia.org/wiki/Selection_bias). Customers engaging me usually run complex environments that might be by definition prone to weird failures. On the other hand, at least some of them run well-managed environments, and they got a bridging loop even though they did all the right things.

It might be [confirmation bias](https://en.wikipedia.org/wiki/Confirmation_bias). I keep telling people how dangerous large L2 environments are, so I might remember those workshops where they told me "yeah, that happened recently" better than others.

Or it could be that the vendors are truly peddling broken technology (of course only because the customers ask for it, right?) and we're paying the price of CIOs or high-level architects making decisions based on glitzy PowerPoints and "impartial" advice from \$vendor consultants.

I simply don't have enough data points to know better, and it seems [we made no real progress in the last few years](/2016/10/the-network-is-reliable-and-other/) -- all I could find was anecdata. Your feedback would be highly appreciated.
