---
title: "BGP Labs: Use Your Preferred Device for External Routers"
series_title: "Use Your Preferred Device for External Routers"
date: 2026-03-31 07:34:00+02:00
tags: [ BGP, netlab ]
netlab_tag: bgplab
BGP_tag: lab
---
**TL&DR:** With the recent changes to [online BGP labs](https://bgplabs.net/), you can also use Aruba CX, Cisco IOS, Cisco IOS XE, Cisco IOS XR, Dell OS10, Junos, or VyOS as external lab devices in most lab exercises (you could always use these devices for the routers you worked on). Previously, you could choose between Arista EOS and FRRouting, both of which are (obviously) still supported.

One of the goals of the [Online BGP Labs project](https://bgplabs.net/) was to create an environment in which you could practice the BGP features you were interested in without spending an inordinate amount of time preparing the lab.

For example, if you want to figure out [why BGP wedgies work the way they do](https://bgplabs.net/policy/e-wedgies/), you need at least four additional autonomous systems, two of them acting as upstream ISPs for your customer router, and at least one of them implementing BGP policies using BGP communities.
<!--more-->
{{<figure src="https://bgplabs.net/policy/topology-wedgies.png">}}

While many labs used _[netlab](https://netlab.tools/)_ features like *[originate BGP default route](https://netlab.tools/plugins/bgp.session/)* to configure "external" routers[^XR], more complex labs used *[custom configuration templates](https://netlab.tools/custom-config-templates/)* to configure AS-path filters, BGP community lists, and route maps. Those templates were only available for FRRouting and Arista EOS, forcing you to use potentially unfamiliar devices in your labs.

[^XR]: External as in "you don't need to configure them". They are obviously still part of the lab.

In the meantime, we implemented routing policies, AS-path filters, and BGP community lists on a [half-dozen network operating systems](https://netlab.tools/module/routing/#id4) (for a total of ~20 [device types](https://netlab.tools/platforms/)), and it would be a shame not to use that functionality in the BGP labs.

In March 2026, I rewrote most of the lab topologies that used custom configuration templates to use the *netlab* [Generic Routing features](https://netlab.tools/module/routing/), resulting in a much wider range of devices you can use for the external routers. For example, it's now perfectly feasible to run almost all labs in a Cisco IOS-only (or Junos-only) environment, making it much easier to troubleshoot the labs because you won't have to deal with less-familiar devices[^TNH].

[^TNH]: Although I never heard of anyone being hurt by knowing how to do **show** commands on a box from another vendor.

Hope you'll like the wider selection of lab devices. If you experience any problems, please report them by opening a [GitHub issue](https://github.com/bgplab/bgplab/issues/new/choose).