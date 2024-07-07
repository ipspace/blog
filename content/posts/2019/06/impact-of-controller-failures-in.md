---
date: 2019-06-20 08:14:00+02:00
distributed-systems_tag: sdn
ha-cluster_tag: sdn
high-availability_tag: ignore
sd-wan_tag: myth
series:
- ha-cluster
- distributed-systems
series_weight: 1400
tags:
- SD-WAN
- SDN
- WAN
- high availability
title: Impact of Controller Failures in Software-Defined Networks
url: /2019/06/impact-of-controller-failures-in/
---
[Christoph Jaggi](http://uebermeister.com/about.html) sent me this observation during one of our SD-WAN discussions:

> The centralized controller is another shortcoming of SD-WAN that hasn't been really addressed yet. In a global WAN it can and does happen that a region might be cut off due to a cut cable or an attack. Without connection to the central SD-WAN controller the part that is cut off cannot even communicate within itself as there is no control plane...

A controller (or management/provisioning) system is obviously the central point of failure in any network, but we have to go beyond that and ask a simple question: "What happens when the controller cluster fails and/or when nodes lose connectivity to the controller?"
<!--more-->
{{<note>}}
Whoever claims [you don't have to worry about failure scenarios because redundant links and out-of-band management network ensure total failures never happen](/2012/10/if-something-can-fail-it-will/) has just proven they have no clue what they're talking about.
{{</note>}}

Worst-case scenario is the orthodox SDN architecture with [centralized control plane residing in the controller](/2014/05/does-centralized-control-plane-make/). While packet forwarding might continue to work until the flows time out, even [ARP won't work anymore](/2013/06/implementing-control-plane-protocols/).

Architectures based on a bit more operational experience like Big Switch fabric can deal with short-term failures. Big Switch claims [ARP entries reside in edge switches](/2015/02/big-cloud-fabric-scaling-openflow-fabric/), so they can keep ARP going even when the controller fails. It might also be possible to pre-provision backup paths in the network (see also: SONET/SDH) so the headless fabric can deal with link failures (but not link recoveries because those require path recalculation). Dealing with external topology changes like VM migration is obviously already a mission impossible.

Some architectures deal with controller failure by falling back to *traditional* behavior. For example, ESXi hosts that lose connectivity with the NSX-V controller cluster enter *controller disconnected* mode in which they flood every BUM packet on every segment to every ESXi host in the domain. While this approach obviously works, try to figure out how much overhead (and wasted CPU cycles) it generates.

On the complete other end of the spectrum are systems with traditional distributed control plane that use SDN controller purely for management tasks. Cisco ACI immediately comes to mind - as I usually joke during my "NSX or ACI" workshops, you could turn off APIC controller cluster when going home for the weekend and the ACI fabric would continue to work just fine.

Where are SD-WAN systems in this spectrum? We don't know, because the vendors are not telling us how their secret sauce works. However, at least some vendors claim their magic SD-WAN controller replaces routing protocols, which means that controller failure might prevent edge topology changes from propagating across the network.

There's also the nasty question of key distribution. In traditional systems like DMVPN edge nodes exchange P2P keys with IKE and use shared secrets or pre-provisioned certificates to prevent man-in-the-middle attacks. In an SD-WAN system the controller might do key distribution, in which case I wish you luck when you'll face a nasty WAN partition (or AWS region failure if the controller runs in the cloud).

**Summary:** Things are never as rosy as they appear in PowerPoint presentations and demos. Figure out everything that could potentially go wrong (like WAN partitioning), try to find what happens from product documentation, and ask some really hard questions (or change the vendor) if the documentation is not useful. Finally, verify every claim a \$vendor makes in a lab.
