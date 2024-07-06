---
title: "Hub-and-Spoke VPLS: Revenge of LDP"
date: 2022-03-16 07:55:00
lastmod: 2022-03-18 07:02:00
tags: [ MPLS, segment routing ]
---
In the [Segment Routing vs LDP in Hub-and-Spoke Networks](/2022/03/hub-spoke-ldp-segment-routing.html) blog post I explained why you could get into interesting scaling issues when running MPLS with LDP in a large hub-and-spoke network, and how you can use Segment Routing (MPLS edition) to simplify your design.

{{<figure src="/2022/03/LDP-Hub-Spoke.jpg" caption="Sample hub-and-spoke network">}}

Now imagine you'd like to offer VPLS services between hubs and spokes, and happen to be using equipment that uses targeted LDP sessions to signal pseudowires. Guess what happens next...
<!--more-->
Even though the network was supposed to be using Segment Routing to propagate labels for loopback interfaces, a label will be assigned to every applicable prefix in the IP forwarding table[^LABL] the moment the LDP process is started, and all those labels will be advertised to every LDP peer (whoever you configured targeted LDP sessions with). In our case (assuming Cisco IOS/XE deployment), the hub routers yet again receive label assignments for every prefix in the global routing table.

You can use the tricks [described in the previous blog post](/2022/03/hub-spoke-ldp-segment-routing.html) to limit the label allocation or advertisement, but if you happen to be using IOS XR there's [another nerd knob to tweak](https://www.cisco.com/c/en/us/td/docs/iosxr/ncs5500/mpls/71x/b-mpls-cg-ncs5500-71x/b-mpls-cg-ncs5500-71x_chapter_010.html#concept_yv1_fkx_vmb): with **mpls ldp capabilities sac** configuration command you can disable IPv4 and/or IPv6 label bindings. I couldn't find a similar configuration command for IOS XE, a pointer to relevant documentation would be appreciated.

{{<note info>}}Did you know LDP has *capabilities* similar to BGP (see [RFC 5561](https://www.rfc-editor.org/rfc/rfc5561.html) for details) and can negotiate them between peers during the session initialization? I didn't, but I wasn't exactly surprised when I found that RFC. For a full list of LDP capabilities, check the [IANA LDP registry](https://www.iana.org/assignments/ldp-namespaces/ldp-namespaces.xhtml).{{</note>}}

### It Gets Worse

[Jeff Tantsura](https://www.linkedin.com/in/jeff-tantsura/) pointed out a particularly nasty implementation detail in a LinkedIn comment:

> If you run older software of a particular vendor, it won’t resolve tLDP over SR LSPs and requires full LDP configuration, with as consequence - LDP to SR mapping and SRMS deployment. Talk to your vendor before deployment.

### Revision History

2022-03-18
: Added tLDP-over-SR implementation gotcha

[^LABL]: By default, [Cisco IOS assigns a label to every prefix, while Junos assigns labels only to loopback interfaces](/2011/11/junos-versus-cisco-ios-mpls-and-ldp.html).