---
title: BGP in Data Center Fabrics
layout: custom
minimal_sidebar: true
sidebar_box: rb
---
You must use BGP as the endpoint reachability routing protocol in your data center fabric if you decide to run VXLAN with EVPN control plane... but should you also run it as the transport (underlay) routing protocol instead of OSPF or IS-IS? The resources collected on this page might help you make that decision.

{{<plushy happy>}}We covered this topic in these webinars, articles, and podcasts:

-   [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)
-   [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
-   [Using BGP in a Data Center Leaf-and-Spine Fabric](https://www.ipspace.net/Data_Center_BGP/)
-   [BGP in EVPN-Based Data Center Fabrics](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics)
-   [BGP Navel Gazing](https://blog.ipspace.net/2020/06/bgp-navel-gazing.html) (Software Gone Wild episode 112)
-   [Can We Trust Routing Protocols](https://rule11.tech/the-hedge-pdocast-episode-43-ivan-pepelnjak-and-trusting-routing-protocols/) (The Hedge episode 43)
-   [Cool or Hot? Lapukhov + Nkposong’s BGP SDN](https://packetpushers.net/podcast/show-164-cool-or-hot-lapukhov-nkposongs-bgp-sdn/) (Packet Pushers episode 164)

[Petr Lapukhov](https://www.linkedin.com/in/petrlapu/) (the author of [BGP-as-better-IGP idea](https://www.youtube.com/watch?v=yJbqnOdD3cg)) initially proposed to use BGP as a data center SDN mechanism. I covered that use case in the [BGP-Based SDN Solutions](https://www.ipspace.net/BGP-Based_SDN_Solutions) webinar and in these blog posts:

{{<series-listing tag="sdn" year="sure">}}

{{<plushy confused>}}We also tried to answer the question "*Do we need a new routing protocol for data center fabrics?*" in these Software Gone Wild episodes and related blog posts (TL&DL: No):

{{<series-listing tag="newrp" year="please do" weight="yes">}}

{{<plushy master>}}I covered the design aspects of using BGP in data centers (in particular in combination with EVPN) in these blog posts:

{{<series-listing tag="design" year="please do" weight="yes">}}

{{<plushy magic>}}It's also popular to run BGP on redundantly connected servers, or on edge appliances connecting overlay virtual networks with physical world. More details in these blog posts and in the [Routing on Servers](https://my.ipspace.net/bin/list?id=Clos#ROUTING_SERVERS) part of [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.

{{<series-listing tag="server" year="please do" weight="yes">}}

The designers of Cumulus Linux preferred the EBGP-only data center design, and added numerous features to their BGP routing daemon (now FRR). We covered those features in the [FRRouting Architecture and Features](https://www.ipspace.net/FRRouting_Architecture_and_Features) webinar, in the [Cumulus Linux](https://my.ipspace.net/bin/list?id=DCFabric#CUMULUS) part of the [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics) webinar, and in these blog posts:

{{<series-listing tag="cl" year="needed">}}

Some vendors love making your life overly complex, inventing ridiculous architectures like running IBGP (EVPN) over EBGP (IP routing). Here are a few choice ~~rants~~ blog posts on that topic:

{{<series-listing tag="rant" year="needed">}}

{{<plushy magic>}}Two other interesting topics often pop up in BGP-related discussions: [anycast](/series/anycast.html) and [multipathing](/series/ucmp.html):

{{<series-listing tag="interesting" year="sure">}}

You might also find these blog posts somewhat relevant to your data center BGP designs:

{{<series-listing tag="relevant" year="sure">}}

{{<plushy master>}}These BGP details might help you when designing or deploying your next BGP-based network:

{{<series-listing tag="details" year="why not">}}

Finally a few more abstract blog posts to tickle your gray cells:

{{<series-listing tag="abstract" year="absolutely">}}
