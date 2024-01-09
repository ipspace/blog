---
title: "BGP Graceful Restart Considered Harmful"
date: 2024-01-16 08:37:00+0100
tags:
- BGP
- high availability
distributed-systems_tag: device
high-availability_tag: external
series:
- ha-switching
- distributed-systems
---
A networking engineer with a picture-perfect implementation of a dual-homed enterprise site using BGP communities according to [RFC 1998](https://www.rfc-editor.org/rfc/rfc1998.html) to select primary- and backup uplinks contacted me because they experienced unacceptably long failover times.

They measured the failover times caused by the primary uplink loss and figured out it takes more than five minutes to reestablish Internet connectivity to their site.
<!--more-->
{{<figure src="https://bgplabs.net/policy/topology-policy-2isp.png" caption="Approximate network diagram">}}

Such a long convergence time is unusual and often indicates a failure to [detect link- or neighbor loss in a timely manner](https://blog.ipspace.net/2020/11/detecting-network-failure.html). [BFD is the best alternative](https://blog.ipspace.net/2017/10/to-bfd-or-not-to-bfd.html) when the link loss is not signaled correctly to the higher-layer protocols. Unfortunately, one has to configure it on both ends of a connection, and some ISPs still haven't got the "*BFD is better than BGP timers*" memo.

{{<long-quote>}}
BFD Echo mode might seem to be a workaround; using it, a router sends packets to itself and uses layer-2 encapsulation to route them through the adjacent device. However:

* Even if a system uses BFD Echo procedure, the use of BFD has to be negotiated with the neighbor
* Even if it were possible to use BFD without the remote system's awareness, it wouldn't solve the failover of incoming traffic. If the BGP neighbor believes the link is up, it won't revoke the BGP prefix, and convergence won't happen.
{{</long-quote>}}

Lacking BFD, reducing BGP timers is the next best thing one can do. I suggested reducing them to something low enough for their needs but still sane and acceptable to the upstream ISP.

{{<long-quote>}}
Did you know that BGP neighbors negotiate the BGP timers during the BGP session establishment process? You can reduce the timers on one BGP neighbor and have the other neighbor accept the changes.

If I were a Service Provider, I'd want to prevent my customers from hogging my CPU with very short BGP timers. Some network operating systems allow you to specify the minimum BGP timer values a device is willing to accept from its BGP neighbors.
{{</long-quote>}}

However, the default BGP timers cause a three-minute convergence delay. Two minutes were still unaccounted for, and we couldn't figure out what might be causing that extra delay until [Andrea di Donato](https://www.linkedin.com/in/andreadidonato/) made an interesting remark when we were discussing the problem in one of the Design Clinics: _"Make sure you haven't configured BGP Graceful Restart."_

Here's what's going on behind the scenes:

* Any recent BGP implementation will accept that its neighbor uses [Graceful Restart](/2021/09/graceful-restart.html) regardless of whether the Graceful Restart is configured locally.
* After losing a BGP neighbor, the Graceful Restart procedure keeps BGP routes in the BGP table until the Graceful Restart timer expires, effectively prolonging the convergence process.
* The default Cisco IOS Graceful Restart timer is two minutes. Bingo -- we figured out the root cause for the five-minute convergence time.

**Takeaway:**

* Don't configure BGP Graceful Restart until you know full well what you're doing and what the implications are[^AMOT]
* Graceful Restart is a good idea *if and only if* you can [reliably detect forwarding path failures using a mechanism like BFD](https://blog.ipspace.net/2021/10/graceful-restart-bfd.html) ([more caveats](https://blog.ipspace.net/2021/10/repost-bfd-gr.html)).
* Using Graceful Restart when relying on BGP timers to detect BGP neighbor loss is useless. All it does is prolong the inevitable pain unless you experience control-plane failures more often than link failures, in which case you're dealing with a more severe challenge than convergence speed.

[^AMOT]: That same rule can be applied to many other things. It is consistently ignored in the blatant throwing-spaghetti-at-the-wall style by people indiscriminately using Google or AI to solve their challenges.

Obviously, no list of caveats ever stopped marketers from promoting a feature as the next best thing since sliced bread. For example, Cilium [proudly announced its BGP Graceful Restart capability](https://isovalent.com/blog/post/connecting-your-kubernetes-island-to-your-network-with-cilium-bgp/) in a scenario where it makes no sense to use it -- it's a cluster, so run two BGP daemons on two service nodes and move on.

Finally, no technology can ever resist the siren song of ever more nerd knobs. For example, [RFC 9494](https://datatracker.ietf.org/doc/html/rfc9494) describes long-lived BGP Graceful Restart that uses BGP communities to allow you to delay the convergence process for even longer.

### Need Hands-on Practice?

Try out these BGP lab exercises:

* [Use BFD to Speed Up BGP Convergence](https://bgplabs.net/basic/7-bfd/) to master BGP timers and using BFD with BGP.
* [BGP Local Preference in a Complex Routing Policy](https://bgplabs.net/policy/a-locpref-route-map/) to implement RFC 1998-style routing policy.
