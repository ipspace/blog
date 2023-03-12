---
date: 2017-09-28 09:28:00+02:00
high-availability_tag: need
lastmod: 2021-11-02 15:57:00
series_weight: 700
tags:
- design
- data center
- high availability
title: Redundancy Does Not Result in Resiliency
url: /2017/09/redundancy-does-not-result-in-resiliency.html
---
A while ago a large airline had a bad-hair day claiming it was caused by a faulty power supply. Not surprisingly, I got a question along the lines of "*is that feasible?*"

**Short answer**: Yes. However, someone should be really worried if that wasn't made up.
<!--more-->
There are companies out there that learn from their mistakes. Even more, they publicly admit what went wrong, what they learned, and how they improved their processes to ensure this particular SNAFU won't happen in the future. I even found a [nice list of public post-mortem reports](https://github.com/danluu/post-mortems) and [a list of AWS outages](https://awsmaniac.com/aws-outages/). Not surprisingly, airlines and legacy financial institutions are nowhere to be found.

Sometimes something really stupid goes wrong. For example, you're upgrading a component, and its redundant pair fails. Or you thought you had redundancy, but it wasn't configured correctly (missing HSRP neighbor comes to mind). Or a failure resulted in resource shortage resulting in cascading failures as [Amazon found a while ago](https://aws.amazon.com/message/65648/).

Organizations seriously investing in services uptime talk about *Site Reliability Engineers*[^SRE]. They also trigger unexpected failures [manually](http://queue.acm.org/detail.cfm?id=2371297) or [automatically](https://medium.com/netflix-techblog/the-netflix-simian-army-16e57fbab116). AWS even made a [cloud service out of that idea](https://aws.amazon.com/fis/).

Organizations who love to talk about redundancy to get a tick-in-the-box from their auditors move the active database instance once a year under tightly controlled conditions and at the time of minimum load (or even during a scheduled maintenance window).

[^SRE]: So does everyone else -- SRE is becoming another meaningless buzzword

{{<note info>}}For more details on doing failover tests correctly read at least the *failovers* part of the [Small Batches Principle](http://queue.acm.org/detail.cfm?id=2945077) article by Tom Limoncelli (and I strongly recommend you read the whole article).{{</note>}}

**Long story short**: Full redundancy doesn\'t prevent failures. When done correctly, it reduces the probability of a total failure. When done incorrectly, redundant solutions get less robust than non-redundant ones due to increased complexity\... and you don't know which one you're facing until you stress-test your solution.

There's also this crazy thing called statistics. It turns out that [adding redundant components results in decreased availability under gray (or byzantine) failures](https://blog.acolyer.org/2017/06/15/gray-failure-the-achilles-heel-of-cloud-scale-systems/)*.* The authors of the original article [handwaved](https://en.wikipedia.org/wiki/Hand-waving) us to that conclusion, but I did check the math and the results are what they claim they are (or my knowledge of statistics is even worse than I assume).

Finally, do keep in mind that what I was talking about so far are ideal circumstances. In reality, we keep [heaping layers of leaky abstractions](https://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html) and [ever-more-convoluted kludges](http://blog.ipspace.net/2013/08/temper-your-macgyver-streak.html) on top of each other until the whole thing comes crashing down resulting in days of downtime. Or as Vint Cerf said in a [recent article](https://cacm.acm.org/magazines/2017/7/218867-a-brittle-and-fragile-future/fulltext): we're facing a brittle and fragile future.

Need more details? You might find some useful ideas in my [Designing Active-Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar... or you might go read a vendor whitepaper. [The choice](https://en.wikipedia.org/wiki/Red_pill_and_blue_pill) is yours.

### Revision history

2021-11-02
: Added links to a list of AWS outages and AWS Fault Injection Simulator.
