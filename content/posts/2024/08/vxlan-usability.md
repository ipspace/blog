---
title: "Response: The Usability of VXLAN"
date: 2024-08-12 07:50:00+0200
tags: [ VXLAN, data center, fabric ]
---
Wes made an [interesting comment](https://blog.ipspace.net/2024/08/data-center-fabric-migration/#2360) to the [Migrating a Data Center Fabric to VXLAN](https://blog.ipspace.net/2024/08/data-center-fabric-migration/) blog post:

> The benefit of VXLAN is mostly scalability, so if your enterprise network is not scaling... just don't. The migration path from VLANs is to just keep using VLANs. The (vendor-driven) networking industry has a huge blind spot about this.

Paraphrasing the [famous Dinesh Dutt's Autocon1 remark](https://youtu.be/6mNLESvNuCs?si=C4rBX1r3XTA6WGTX&t=1849): I couldn't disagree with you more.
<!--more-->
While it's true that VXLAN allows you to build scalable layer-2 networks (while remaining limited to 4K VLANs per edge device) and that the network industry is on a VXLAN/EVPN lemming run, I [forcefully disagree that the path from VLANs is more VLANs](2020/03/should-i-go-with-vxlan-or-mlag-with-stp/).

The VLAN-only data center fabrics have two major problems:

* Unless you want to deploy something like TRILL or SPB (in which case [VXLAN is a better option anyway](/2024/04/spb-trill-evpn/)), you have to use STP to detect loops. We learned the hard way how brittle STP is, and I wouldn't want to use that landmine in a new fabric.
* You're usually forced to use [MLAG](/series/mlag/) between leaf and spine switches to avoid the STP limitations (and a peer link between switches in an MLAG cluster).

While MLAG might not have been a big deal more than a decade ago when everyone recommended using LAG everywhere, it's a huge drawback in a world where most devices attached to the fabric don't need LAG uplinks (with some vendors actively discouraging LAG). It's also another ticking bomb waiting to explode; I've seen more than one data center meltdown caused by an MLAG bug.

Both limitations disappear if you use VXLAN as the fabric transport mechanism:

* While you have to run STP on the fabric edges, you can configure **bpdu guard** on the edge ports and use it as a canary.
* Fabric transport uses IP routing, which means that ECMP load balancing works as soon as equal-cost paths exist.

{{<note>}}If you still have devices that require LAG uplinks, concentrate them on a single pair of leaf switches to contain the MLAG abomination.{{</note>}}

Please note that I'm not telling you to use EVPN. Small VXLAN-based fabrics [do not need a VPN control plane](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/), and I wouldn't use [EVPN-based MLAG](/2023/05/mlag-without-peer-link/) in small deployments.

Not surprisingly, I wrote about the same topics in the past:

* [Should I Go with VXLAN or MLAG with STP?](https://blog.ipspace.net/2020/03/should-i-go-with-vxlan-or-mlag-with-stp/)
* [EVPN/VXLAN or Bridged Data Center Fabric?](https://blog.ipspace.net/2022/09/mlag-bridging-evpn/)
* [vSphere Does Not Need LAG Bandaids](https://blog.ipspace.net/2014/01/vsphere-does-not-need-lag-bandaids/)
* [Don&#39;t Base Your Design on Vendor Marketing](https://blog.ipspace.net/2019/05/dont-base-your-design-on-vendor/)
