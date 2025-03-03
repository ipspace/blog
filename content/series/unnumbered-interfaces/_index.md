---
title: Unnumbered IPv4 Interfaces
sidebar_box: rb
layout: custom
---
IPv4 was designed to be used on large hosts connected to a third-party proprietary WAN network and thus assumed that an IP subnet would be assigned to every (edge) network segment. However, when we started deploying IPv4-only networks, we quickly discovered scenarios where this assumption wasted address space or made deploying the desired solution impossible.

Vendors tried to circumvent that limitation with various unnumbered IPv4 interface solutions, starting with point-to-point links and dialup scenarios and eventually ending with unnumbered Ethernet interfaces.

{{<note info>}}We don't have a similar problem in the IPv6 world as every IPv6-enabled interface always gets a link-local address.{{</note>}}

These blog posts will help you understand why IPv4 uses interface addresses, what we can gain with unnumbered IPv4 addresses, how they work over Ethernet links, and how they interact with routing protocols.

{{<series-summary>}}
