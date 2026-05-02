---
title: SRv6
page_title: Segment Routing over IPv6 (SRv6)
minimal_sidebar: true
layout: custom
---
Segment Routing over IPv6 (SRv6) is mostly a solution in search of a problem, reimplementing source routing with various forms of IPv6 extension headers. Not surprisingly, its vocal proponents sell it as the ultimate solution to all networking problems.

{{<figure src="/images/srv6-white.png">}}

### {{<plushy confused>}}Is It Useful?

Is it useful to have yet another tunneling mechanism with source routing capabilities? Here are a few thoughts:

{{<series-listing tag="intro">}}

### {{<plushy angry>}}No, It Is Not

Quite a few people (myself included) came to the conclusion that SRv6 makes little sense:

{{<series-listing tag="rant">}}

### {{<plushy idea>}}Potential Use Cases

A few people (besides vendor Distinguished Marketing Engineers) have proposed potentially interesting SRv6 use cases:

{{<series-listing tag="use">}}

Still want to try out SRv6? 

{{<series-listing tag="lab">}}

### {{<plushy master>}}More Information

* We [implemented SRv6 in _netlab_](https://netlab.tools/module/srv6/). You can try it out on Cisco IOS XE, Cisco IOS XR, Nokia SR OS, and FRRouting.
* Browse [_netlab_ SRv6 integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration/srv6) for sample lab topologies.
* Tiziano Tofoni covered SRv6 basics in his [ITNOG10 workshop](https://www.itnog.it/itnog10/files/TRaining_Segment%20Routing%20ITNOG%202026%20april%2020_signed.pdf)
* [@eldananivas](https://github.com/eldaninavas) collected numerous SRv6-related links into an [open-source SRv6 knowledge base](https://srv6.md/).

{{<series-listing title="Blog Posts I Forgot to Categorize" notag="yes">}}
