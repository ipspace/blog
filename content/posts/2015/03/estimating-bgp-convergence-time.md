---
date: 2015-03-09 07:56:00+01:00
tags:
- scalability
- BGP
title: Estimating BGP Convergence Time
url: /2015/03/estimating-bgp-convergence-time/
series: vagg
vagg_tag: basics
---
One of my readers sent me this question:

> I have an Internet edge setup with two routers connected to two upstream ISPs and receiving full BGP routing table from them. I'm running iBGP between my Internet routers. Is there a formula to estimate convergence time if one of my uplinks fail? How many updates will I need to get the entire 512K routes in BGP table and also how much time it would take?

As always, the answer is *it depends*.
<!--more-->
If you're trying to estimate how large the updates would be, look into how much memory the BGP process is consuming. BGP updates are pretty tightly packed, and the Cisco IOS in-memory structures probably closely reflect the BGP data model. In [one of my experiments](/2012/07/is-it-safe-to-run-internet-in-vrf/) BGP used approximately 250 bytes per prefix, or 128 MB for 512K routes.

On the other hand, a BGP update message carrying a prefix with 3 AS numbers in the AS path is less than 100 bytes long (based on [sample BGP wireshark capture](http://wiki.wireshark.org/SampleCaptures)), so you might need closer to 50-60 MB to send 512K routes in BGP updates.

{{<note>}}
Do you have more precise numbers? Please share them in the comments!
{{</note>}}

Next, estimate how long it would take to transfer that information to the other router. With 1Gbps link between the two boxes the answer should be "less than a second", more so as you have negligible latency and hopefully no packet drops between them.

However, very probably you won't get anywhere close to that - the two routers have to generate the updates, process the updates, choose new best paths, install them in IP routing table and FIB... and based on the CPU used in your router it can take significantly longer than 1 second.

Some platforms with dismal CPUs could take minutes to converge, resulting in unpleasant brownouts. I described these problems and potential solutions in the [BGP Convergence Optimization](http://www.ipspace.net/BGP_Convergence_Optimization) case study (part of [ExpertExpress Case Studies](http://www.ipspace.net/ExpertExpress_Case_Studies) and [Data Center Design Case Studies](http://www.ipspace.net/Data_Center_Design_Case_Studies) book)

In any case, if you're worried about BGP convergence time in this simple scenario, use [BGP Best External](/2013/05/bgp-best-external-explained/) and [BGP Prefix Independent Convergence](/2012/01/prefix-independent-convergence-pic/) features to ensure the local FIB converges immediately after the link or BGP neighbor loss, not after all the BGP updates have been processed.
