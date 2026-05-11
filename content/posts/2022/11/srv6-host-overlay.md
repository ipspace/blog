---
title: "SRv6 as a Host-to-Host Overlay"
date: 2022-11-08 07:38:00
tags: [ SRv6 ]
srv6_tag: rant
lastmod: 2026-05-11 16:47:00+0200
---
During the [discussion](https://www.linkedin.com/posts/ivanpepelnjak_on-applicability-of-mpls-segment-routing-activity-6988028852761427968-0Qeq/) of the [On Applicability of MPLS Segment Routing (SR-MPLS)](/2022/10/applicability-sr-mpls/) blog post on LinkedIn someone made an off-the-cuff remark that...

> SRv6 as an host2host overlay - in some cases not a bad idea

It's probably just my myopic view, but I fail to see the above idea as anything else but another tiny chapter in the "_Solution in Search of a Problem_" SRv6 saga[^LISP].
<!--more-->
There are two well-known reasons one might want to use a host-to-host overlay:

[^LISP]: Still not as bad as "_we could use LISP to implement global VM mobility_" idea followed by a demo of a single VM moved across Europe.

* Implement virtual networks
* Implement service insertion

{{<long-quote>}}
According to a [comment](https://blog.ipspace.net/2022/11/srv6-host-overlay/#2963) by an Anonymous Friend of the Blog, hyperscalers and friends use SRv6 for host-based traffic engineering.

Yeah, I missed that use case, but I doubt it's relevant to many readers of this blog. There is no need for that in most data center fabrics; no ready-to-use product does that, and the amount of prerequisite engineering (not to mention the ASIC requirements) is non-trivial. However, that's the least of your problems when you're ~~wasting~~ spending hundreds of billions of dollars on hardware. Also, there's sometimes a bit of a gap between what tech companies claim they do and what they do in most of their production.

It's like claiming front and rear wings make perfect sense on cars because F1 cars use them.
{{</long-quote>}}

On the *virtual networks* front, we had GRE for decades. We got VXLAN almost a decade ago, and GENEVE a few years later. GRE and VXLAN address a specific use case -- GRE is primarily used for some-L3-over-IP transport[^NVGRE], while VXLAN excels when you have to transport Ethernet frames over IP.

GENEVE extends VXLAN with multi protocol capabilities and TLV-encoded metadata. It's not Turing-complete, but it's probably pretty close to an overlay kitchen sink[^KS]. SRv6 adds nothing to the table apart from the _one protocol to rule them all_ Kool-Aid[^RE] and larger headers.

[^NVGRE]: Although we did use GRE for bridging decades ago, and one could always considered NVGRE just a variant of GRE.

[^KS]: As in "_you can throw anything into it without clogging it too much_"

[^RE]: ... and the awesome opportunity to enhance your resume

Maybe we're looking at the wrong problem. Watching various SRv6 (marketing) presentations, one gets the impression that SRv6 shines in the Service Insertion arena, so maybe that's why we should use it instead of VXLAN or GENEVE. This is how the _service insertion_ fairy tale is usually told:

* A controller figures out what needs to be done
* The controller programs a stack of entries listing all the services a packet must visit in the ingress node
* The ingress node adds that stack of entries to the incoming packet, ensuring the packet will traverse all the required services.
* Every service in the list receives the packet, removes itself from the list of services, processes the packet, and sends the packet to the next service.

Ignoring for the moment the stupendous complexity of real-life service insertion (anyone remembers Cisco's Virtual Security Gateway?), there's a tiny detail usually glossed over: all the services have to be aware of the "service processing" header and handle that header together with the user packet. That's why Network Services Header idea never took off. For more details, watch the [Service Insertion](https://my.ipspace.net/bin/get/SDNUseCases/5.1%20-%20Service%20Insertion.mp4?doccode=SDNUseCases) part of [SDN Use Cases](https://www.ipspace.net/SDN_Use_Cases) webinar.

Now ask yourself: how many commercial network appliances can do something along those lines? Let me help you: all those that are integrated with AWS Gateway Load Balancer, Azure Gateway Load Balancer, or VMware NSX east-west packet inspection. How many of those use SRv6? None.

It's not surprising that VMware chose GENEVE as the east-west service insertion transport protocol[^NS] -- GENEVE is the default overlay protocol in VMware NSX-T. It's more interesting that AWS Gateway Load Balancer uses GENEVE even though they use VXLAN for Transit Gateway Connect. Finally, there's Azure Gateway Load balancer using two VXLAN tunnels between the load balancer and each appliance, proving the age-old wisdom that _as long as service insertion means VLAN stitching, you can do it with VXLAN and EVPN_[^AE]. Is there a shipping implementation of service insertion using SRv6? I'm not aware of one.

[^NS]: North-South service insertion in VMware NSX-T is simple VLAN stitching.

[^AE]: I'm not implying that Azure uses EVPN, just that you can do VLAN stitching with EVPN control plane.

Back to the original _SRv6 as host-to-host overlay_ idea:

* I see no good reason to use SRv6 instead of VXLAN or GENEVE to implement overlay virtual networks. It seems no commercial data center overlay virtual networking product is using it[^HG].
* Large-scale commercial service insertion implementations use VXLAN or GENEVE.

[^HG]: There is a [home-grown OpenStack implementation](https://speakerdeck.com/line_developers/line-data-center-networking-with-srv6)

As always, I might be missing something obvious, in which case I'd appreciate your comments.

### More Information

* Service insertion challenges are described in the _[SDN Use Cases](https://www.ipspace.net/SDN_Use_Cases)_ webinar.
* VMware NSX-T east/west and north/south service insertion is covered in _[Firewalling and Security](https://my.ipspace.net/bin/list?id=NSX#FW)_ part of _[VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)_
* AWS Gateway Load Balancer and AWS Transit Gateway Connect are part of _[Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking)_ webinar.
* Azure Gateway Load Balancer will get a brief mention[^AGLB] in autumn 2022 update of _[Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking)_ webinar.

[^AGLB]: The documentation is approximately two pages long and mostly says "_we're working with our integration partners to bring you the best possible experience_."

### Revision History

2026-05-11
: According to an Anonymous Commenter, hyperscalers use SRv6 for host-based traffic engineering.