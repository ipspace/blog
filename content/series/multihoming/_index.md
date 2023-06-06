---
title: Site and Host Multihoming
layout: custom
minimal_sidebar: true
tags: [ high availability ]
high-availability_tag: infra
date: 2023-03-10 07:47:00
sidebar_box: HA
---
{{<quote source="ChatGPT explaining multihoming">}}Multihoming is the practice of connecting a computer or network to multiple Internet Service Providers (ISPs) at the same time. This allows the network to have multiple paths to the internet, which can improve network reliability, speed, and redundancy.{{</quote>}}

Not bad for a statistical text-building engine; now for the details. Site multihoming is usually implemented with provider-independent address space and BGP (details in [Redundant BGP-Based Internet Access](https://my.ipspace.net/bin/list?id=Design#2022_09) part of September 2022 [Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic)).

{{<series-listing tag="bgp">}}

That's way too complex for small sites which usually use NAT-based tricks in IPv4 world.

{{<series-listing tag="site">}}

Unfortunately, those tricks don't work very well with IPv6:

{{<series-listing tag="ipv6">}}

Site multihoming is just part of the whole story. In some scenarios we need multiple connections between servers and the network (see also: [Redundant Server-to-Network Connectivity](https://www.ipspace.net/Redundant_Server-to-Network_Connectivity)).

{{<series-listing tag="server">}}

Finally, it's worth mentioning that the multihoming issues SHOULD have been solved in the session layer, and that MP-TCP is a good first approximation:

{{<series-listing tag="session">}}

{{<series-untagged title="Blog Posts I Forgot to Tag">}}
