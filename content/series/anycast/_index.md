---
title: Anycast
layout: custom
minimal_sidebar: true
---
Anycast is a design in which a single destination IP address is shared by devices in multiple locations. It can be used to implement large-scale UDP services (example: DNS) or to build multi-site high-availability solutions without DNS-based load balancing.

Anycast is also commonly used in data center fabrics to implement redundant first-hop gateways, and with overlay virtual networks (example: VXLAN) to build scale-out gateway clusters or [MLAG clusters](/2022/09/mlag-deep-dive-vxlan-fabric.html).

{{<series-listing tag="intro" title="What Is Anycast?" weight="1">}}
{{<series-listing tag="fabric" title="Anycast in Data Center Fabrics">}}
{{<series-listing tag="design" title="Network Designs Using Anycast">}}
{{<series-listing tag="use" title="Anycast Use Cases" soon="deep_dive">}}
{{<series-listing tag="ecmp" title="Anycast Multipathing">}}
{{<series-listing tag="lab" title="Testing IP Anycast in a Virtual Lab">}}
{{<series-listing tag="reading" title="Further Reading">}}
