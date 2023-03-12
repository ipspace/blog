---
date: 2015-10-13 07:33:00+02:00
high-availability_tag: fail
series_weight: 440
tags:
- bridging
- data center
- WAN
- high availability
title: Sometimes You Have to Decide How You Want to Fail
url: /2015/10/sometimes-you-have-to-decide-how-badly.html
---
Another week, another [ExpertExpress](http://www.ipspace.net/ExpertExpress) session, as is often the case focusing on two data centers with stretched VLANs spanning both of them. However, this one was particularly irksome, as the customer ran a firewall cluster stretched across two locations.

I gave the customer engineers my usual recommendations:
<!--more-->
-   Try to get rid of stretched VLANs, or at least minimize the number of VLANs that span both data centers;
-   Try to identify the [real business needs](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) and solve them with the right tool(s) for the job (example: VMware SRM instead of [stretched HA cluster](http://blog.ipspace.net/2011/06/stretched-clusters-almost-as-good-as.html));
-   Split applications (and subnets) across both data centers so that every application (and subnet) is active only in one data center, having the second one as a backup;
-   Consider the storage failover: if the storage failover is not automatic, it doesn't make sense to even consider a stretched HA cluster (the proof is left as an exercise for the reader ;)
-   Sometimes good enough is good enough -- you can create VLANs and subnets in the alternate location with automation scripts before starting the data center recovery.

They understood all the arguments and agreed with most of them, but it was obvious every single one of them was going to be an uphill battle for them.

In the end, we were left with the question of the [stretched firewall cluster](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html). As we already agreed to try to keep (active parts of the) subnets in a single data center, it would be easy to split the cluster in two independent firewalls, each one of them serving a subset of IP subnets, but then they'd lose the redundancy features.

The obvious solution was to deploy two independent firewall clusters, but they didn't have the budget to buy additional boxes, so the only advice I could give them was ***you have to decide how badly you want to fail (and when)***:

-   You could keep the stretched firewall cluster, and risk shutting down one data center (if one firewall in the cluster shuts down after losing connectivity with the other one) or having an interesting split-brain failure when the DCI link fails;
-   You could run two non-redundant firewalls and risk losing external access to a data center when one of them crashes;

{{<note warn>}}I won't even mention the crazy traffic flows across the DCI link after one of the cluster members fails, or the challenges of upgrading the software in these firewalls, in either standalone or cluster mode.{{</note>}}

**Summary**: when faced with a lose-lose decision, the only thing you can do is (A) evaluate all possible failure modes, (B) identify all the risks associated with individual options, (C) decide which one(s) you want to accept, (D) document the risks and the decision, and have your boss sign it off.
