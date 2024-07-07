---
date: 2015-06-18 09:00:00+02:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- bridging
- high availability
title: Another Spectacular Layer-2 Failure
url: /2015/06/another-spectacular-layer-2-failure/
---
[Matjaž Straus](https://www.linkedin.com/in/matjaz6) started the [SINOG 2 meeting](http://www.sinog.si) I attended last week with a great story: during the RIPE70 meeting (just as I was flying home), [Amsterdam Internet Exchange](https://ams-ix.net) (AMS-IX) crashed.

Here's how the AMS-IX failure impacted ATLAS probes (world-wide monitoring system run by RIPE) -- no wonder, as RIPE uses AMS-IX for their connectivity.
<!--more-->
{{<figure src="/2015/06/s1600-619DA045-CC2B-4ED4-926A-3CDBC6EC00FA.png">}}

My friend Jeremy Stretch saved the daily traffic graph for posterity in one of his tweets:

{{<figure src="/2015/06/s1600-5C1D9D2B-88B9-4AF1-9876-E906431FBBB6.png">}}

As you can see from the graph, Internet lost 2 Tbps of transit capacity, and many networks using AMS-IX (including some cloud services providers) were severely impacted.

You might wonder what the root cause for the outage was. Here's the relevant tweet:

{{<figure src="/2015/06/s1600-285C27B7-B885-4FA3-BD46-A2DA4092C2E6.png">}}

As I said many times before, it's not a question of *whether* a [large layer-2 fabric](/2012/05/layer-2-network-is-single-failure/) will crash, it's only the [question of *when* and *how badly*](/2012/10/if-something-can-fail-it-will/).

Also, keep in mind that there are a few significant differences between AMS-IX and clueless geniuses that tell you to build large layer-2 fabric (hopefully stretched across two data centers):

-   AMS-IX is one of the large Internet exchanges and they usually know what they're doing... and still bad things happen;
-   AMS-IX has been in business for almost 20 years and thus has significant operational experience. They've learned loads of lessons during past outages and have built their own tools (like ARP sponge) to make their infrastructure more reliable;
-   Internet exchanges that don't want to dictate routing policies of their members have to be layer-2 fabrics (the proof is left as an exercise for the reader), while your data center doesn't have to be.

### Want Even More Horror Stories?

[Jay Swan pointed me to a recent Cisco Live presentation](https://twitter.com/sanjuanswan/status/609341083403706369) (BRKDCT-3102), which documented several interesting layer-2 failures, including a split-brain cluster -- I was [telling people](/2011/04/distributed-firewalls-how-badly-do-you/) about [these scenarios](/2011/06/stretched-clusters-almost-as-good-as/) for years, and it's so nice to have corroboration from a major vendor (not sure what the evangelists of layer-2 fabrics and DCI solutions working for that same vendor think about that presentation ;).
