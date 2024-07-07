---
title: "Worth Reading: Cloudflare Control Plane Outage"
series_title: "Cloudflare Control Plane Outage"
date: 2023-11-16 09:04:00
tags: [ worth reading, high availability ]
high-availability_tag: outage
---
Cloudflare experienced a significant outage in early November 2023 and published a detailed [post-mortem report](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/). You should read the whole report; here are my CliffsNotes:

* Regardless of how much redundancy you have, [sometimes all systems will fail at once](/2012/10/if-something-can-fail-it-will/). Having redundant systems [decreases the probability of total failure](/2017/09/redundancy-does-not-result-in-resiliency/) but does not reduce it to zero.
* As your systems grow, they gather [hidden- and circular dependencies](/2021/10/circular-dependencies-considered-harmful/).
* You won't uncover those dependencies unless you run a full-blown disaster recovery test (not a [fake one](/2019/09/disaster-recovery-test-faking-another/))
* If you [don't test your disaster recovery plan](/2019/10/disaster-recovery-faking-take-two/), it probably won't work when needed.

Also (unrelated to Cloudflare outage):
<!--more-->
* Even Cloudflare can get an outage. Don't expect your *[stretched VLAN](/series/dr.html#stretched-vlans)* fairyland to survive the encounter with reality.
* Keep your design [as simple as possible](/2021/02/fast-simple-disaster-recovery-solution/)
* Don't rely on [vendor-supplied miracles](/series/dr.html#vendors)
* Unless you can stress-test your ideas, leave the high-level decisions (for example, [when to failover](/2016/05/unexpected-recovery-might-kill-your/)) to humans.
* Automate the low-level operations as much as you can
