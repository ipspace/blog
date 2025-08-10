---
title: "SwiNOG 40: Application-Based Source Routing with SRv6"
date: 2025-08-27 08:28:00+0200
tags: [ segment routing, IPv6 ]
---
The *we should give different applications different paths across the network* idea never dies (even though in many places the residential Internet gives you enough bandwidth to watch 4K videos), and the [Leveraging Intent-Based Networking and SRv6 for Dynamic End-to-End Traffic Steering](https://www.swinog.ch/wp-content/uploads/2025/06/Severin-Dellsperger-OST-University-Leveraging-Intent-Based-Networking-and-SRv6-for-Dynamic-End-to-End-Traffic-Steering.pdf) ([video](https://youtu.be/vpdKcHth6wg)) by Severin Dellsperger was an interesting new riff on that ancient grailhunt.

Their solution uses SRv6 for traffic steering[^SRv6], an Intent-Based System[^IBS] that figures out paths across the network, and eBPF on client hosts[^eBPF] to add per-application SRv6 headers to outgoing traffic.
<!--more-->
[^SRv6]: Remember: SRv6 is mostly remarketed source routing

[^IBS]: Sounds so much better than an SDN controller, right?

[^eBPF]: Everything is better with ~~Bluetooth~~ eBPF

Does this make sense? It might in some niche scenarios. It's also one of the first use cases I encountered where I said, "_Well, maybe it does make sense to use SRv6 here, assuming the problem is worth solving._" 

This solution has a clear advantage over RSVP-based TE -- it scales infinitely better because there is no host-to-network signalling (all the magic happens in the Intent-Based System), no periodic path refreshments, and no extra state in the network.

Drawbacks? The obvious one is the *path liveliness problem*, going all the way back to Token Ring Source Route Bridging sometime in the previous millennium. The path an application is using might become unavailable[^FH], but as nobody knows the application is using the path (because there is no host-to-network signalling), nobody is telling the application to start using another path. In principle, the Intent-Based System could use something like HTTP/2 Server Push to tell the hosts to change their application paths. In practice, I'd like to see how well that scales and how quickly it reacts to network failures in a large-scale environment.

[^FH]: And the usual rerouting doesn't help because the application is using a fixed path across the network. In some cases, that fixed path might result in interestingly circuitous traffic flows; the proof is left as an exercise for the reader.
