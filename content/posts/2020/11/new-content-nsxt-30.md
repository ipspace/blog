---
title: "New Content: VMware NSX-T 3.0 Update"
date: 2020-11-09 07:35:00
tags: [ NSX ]
---
When VMware NSX-T 3.0 came out, I planned to do an update session of the _[VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)_ webinar along the lines of what [I did for AWS Networking a few weeks ago](/2020/10/aws-networking-update.html). However, it turned out that most of the new features didn't take more than a bullet or two on an existing slide, or at most a new slide. 

Covering them in a live session and then slicing-and-dicing the resulting recording simply didn't make sense, so I updated the videos in summer 2020 (the last batch was published in early August).
<!--more-->
Features covered in updated videos include:

-   Changes to Data Center and Enterprise Plus licenses
-   NSX-T support on VDS 7.0
-   Custom MAC limit per VNI
-   Windows 2016 Bare Metal server (+ RHEL 7.6 and 7.7)
-   AMD EPYC support for NSX Edge nodes
-   NAT64 and DHCPv6, IPv6 load balancing
-   Rate limit on Tier-1 uplink
-   Lower BFD timers
-   Time-based scheduling of firewall rules
-   E-W service chaining at the edge
-   New Edge XL platform
-   Local egress for L2VPN
-   L2VPN on Tier-1 gateway
-   PMTUD discovery for L2VPN
-   Stateful VPN failover on NSX Edge node failure

{{<note>}}I'm positive there was a huge amount of effort behind some of these features, it's just that there's not much to say about them. Take NSX-T on VDS 7.0 as an example. I could go into the [nitty gritty details](https://nsx.techzone.vmware.com/resource/nsx-t-vds-7-guide) (which I could cynically summarize as "_too much third-party **** was borked, so we gave up_"), but from a bit further away it boils down to "_it works, use it, but only with vSphere 7_".{{</note>}}

That left what I considered to be *major* features: VRF-Lite and EVPN, IP Multicast, Distributed IDS, and NSX-T Federation. Some of these features were a bit under-documented, so I decided to wait until after VMworld 2020 to develop the update materials. 

{{<note>}}Another aside: kudos to whoever wrote IP Multicast documentation. Concise, precise, and very pleasant to read.{{</note>}}

I finally collected enough information in mid-October, but then it turned out that most of the new stuff doesn't take more than 10-15 minutes... yet again not warranting a live update session, so I just recorded short videos and published them.

The only new feature left was NSX-T federation. NSX-T 3.0 release notes claimed it was not production ready, so I decided to postpone any related work, but of course a few days after I made that decision VMware released NSX-T 3.1 with improved federation support. The current plan is to have an NSX-T Federation update sometime during the winter. In the meantime, you can get an overview of what it's all about in a [video](https://my.ipspace.net/bin/get/NSXACI/S2%20-%20NSX-T%20Multi-Site%20and%20Federation.mp4?doccode=NSXACI) I recorded when updating the [*VMware NSX, Cisco ACI, or EVPN* webinar](https://www.ipspace.net/VMware_NSX,Cisco_ACI_or_Standard-Based_EVPN).
