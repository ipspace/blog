---
date: 2014-06-24 07:09:00+02:00
ospf_tag: config
tags:
- OSPF
- fabric
- Cumulus Linux
title: Unnumbered OSPF Interfaces in Quagga (and Cumulus)
url: /2014/06/unnumbered-ospf-interfaces-in-quagga.html
---
[Carlos Mendioroz](https://ar.linkedin.com/pub/carlos-g-mendioroz/1/85/723) sent me an interesting question about unnumbered interfaces in Cumulus Linux and some of the claims they make in their documentation.

**TL&DR**: Finally someone got it! Kudos for realizing how to use an ancient trick to make data center fabrics easier to deploy (and, BTW, the claims are exaggerated).
<!--more-->
{{<note update>}}Since I wrote this blog post, Quagga went extinct ([again](https://en.wikipedia.org/wiki/Quagga)), and was replaced by [Free Range Routing](https://en.wikipedia.org/wiki/FRRouting) (FRR) -- the control plane daemons used in recent Cumulus Linux distributions{{</note>}}
### Why Am I Excited about Unnumbered Interfaces?

Every data center fabrics vendor claims how easy it is to configure their fabrics. Plug in the cables and the devices almost self-configure the fabric (or you might have to [add a single configuration command](http://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus5000/sw/fabricpath/513_n1_1/N5K_FabricPath_Configuration_Guide/fp_n5k_interfaces.html) like **switchport mode fabric**). Messing up the wiring? No problem, It All Just Works™.

These same vendors require you to configure IPv4 subnets on point-to-point links in a layer-3 leaf-and-spine fabric. Messing up the wiring? We wish you a happy troubleshooting!

{{<note info>}}
Just in case you're wondering why someone needs layer-3 leaf-and-spine fabrics: it's not just overlay virtual networks, they could also be a large web property, doing finite element modelling, running a Hadoop cluster...
{{</note>}}

Can we get around the requirement of configuring IPv4 subnets on links that connect two routed interfaces on adjacent switches? Of course -- we've been using unnumbered interfaces on point-to-point links for ages. It's just that the routing protocol programmers haven't realized the days of thick coax cable are gone; in this century most people use Ethernet on point-to-point links. There's even a [6-year-old informational RFC describing this idea](http://tools.ietf.org/rfc/rfc5309).

To be fair, some vendors did implement unnumbered Ethernet interfaces. For example, [some Cisco IOS images have support for unnumbered VLAN and Ethernet interfaces](http://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/15-1-2/XE_340/configuration/guide/config/unnumber.html#wp1083666), but cannot run routing protocols over them. Not exactly what I've been looking for. Does any other vendor fare better? Write a comment.

{{<note>}}
Did you notice I emphasized IPv4? IPv6 has unnumbered interfaces built in (they are called *Link Local Addresses*), and intra-AS routing protocols like OSPF have to use them (so it's impossible to mangle your implementation in a way that would make numbered IPv6 point-to-point links mandatory).
{{</note>}}

### And Now for the Claims

The [Cumulus documentation](http://cumulusnetworks.com/docs/2.0/user-guide/layer_3/ospf.html#configuration-tip-unnumbered-interfaces) claims:

> In OSPFv2, configuring unnumbered interfaces reduces the links between routers into pure topological elements, and thus dramatically simplifies network configuration and reconfiguration. In addition, routing database contains only the real networks, hence memory footprint is reduced and SPF is faster.

Let's walk through all of these claims:

> Configuring unnumbered interfaces reduces the links between routers into pure topological elements

Translated into engineering terms: the Type-1 (router) LSA no longer contains the stub networks for inter-router subnets. You can do something similar on Cisco IOS with [OSPF prefix suppression](http://www.cisco.com/c/en/us/td/docs/ios/12_4t/12_4t15/ht_osmch.html).

{{<note update>}}2014-06-24 17:40Z - Converting Ethernet interfaces into point-to-point links would also speed up adjacency establishment (no need for DR election) and get rid of type-2 LSAs connecting the two routers (as Enrique pointed out in the comments), which might result in marginally faster SPF (see below). You can achieve the same results in other OSPF implementations by configuring point-to-point OSPF interfaces.{{</note>}}

> ... and thus dramatically simplifies network configuration and reconfiguration.

Marketese for "[we don't check IP subnets in OSPF hello packets](https://blog.ipspace.net/2008/10/ospf-ignores-subnet-mask-mismatch-on.html)".

> In addition, routing database contains only the real networks,

I don't know what they call the *routing database*. OSPF database contains exactly the same number of LSAs, the routing table does contain smaller number of routes (but see also prefix suppression).

> ... hence memory footprint is reduced and SPF is faster.

Memory footprint is reduced. SPF speedup is probably measured in per mils -- after all, the router considers the stub networks attached to Type-1 router LSAs only in the second part of the SPF algorithm, which has linear complexity.

### Summary

I love the way FRR handles point-to-point Ethernet links -- it does make the task of building a layer-3-only leaf-and-spine fabric much easier and error-resistant, but do you really have to call it *dramatic*?
