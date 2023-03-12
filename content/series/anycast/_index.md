---
title: Anycast Resources
layout: custom
minimal_sidebar: true
sidebar_box: rb
---
Anycast is a design in which a single destination IP address is shared by devices in multiple locations. It can be used to implement large-scale UDP services (example: DNS) or to build multi-site high-availability solutions without DNS-based load balancing.

Anycast is also commonly used in data center fabrics to implement redundant first-hop gateways, and with overlay virtual networks (example: VXLAN) to build scale-out gateway clusters or [MLAG clusters](/2022/09/mlag-deep-dive-vxlan-fabric.html).

### {{<plushy confused>}}What Is Anycast?
{{<series-listing tag="intro" weight="1">}}

Want to use anycast in a public cloud? Become a Cloudflare user ;) or use [AWS Global Accelerator](https://my.ipspace.net/bin/get/AWSNET/8.5%20-%20Global%20Accelerator.mp4?doccode=AWSNET&start=10) (described in [Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar).

### {{<plushy master>}}Anycast in Data Center Fabrics
{{<series-listing tag="fabric">}}

For more information watch:

* [Mixed Layer-2 + Layer-3 Fabrics](https://my.ipspace.net/bin/list?id=Clos#L2_L3_FABRIC) in [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar
* [Routing with EVPN](https://my.ipspace.net/bin/list?id=EVPN#ROUTING) in [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
* [Arista EOS](https://my.ipspace.net/bin/list?id=DCFabric#ARISTA) part of [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics) webinar.

### {{<plushy magic>}}Network Designs Using Anycast
{{<series-listing tag="design">}}

### Anycast Use Cases
{{<series-listing tag="use" soon="deep_dive">}}
{{<series-listing tag="ecmp" title="Anycast Multipathing">}}

### {{<plushy happy>}}Testing IP Anycast in a Virtual Lab
{{<series-listing tag="lab">}}
{{<series-listing tag="reading" title="Further Reading">}}

{{<series-listing notag="just in case" title="Blog Posts I Forgot to Categorize">}}