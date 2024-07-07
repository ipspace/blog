---
date: 2012-02-27 07:55:00+01:00
tags:
- switching
- data center
- virtualization
title: Edge Virtual Bridging (802.1Qbg) – a Technology Refusing to Die
url: /2012/02/edge-virtual-bridging-8021qbg/
---
I thought Edge Virtual Bridging (EVB) would be the technology transforming the [kludgy vendor-specific VM-aware networking solutions](/2011/12/vm-aware-networking-improves-iaas-cloud/) into a properly designed architecture, but the launch of L2-over-IP solutions for VMware and Xen hypervisors is making EVB obsolete before it ever made it through the IEEE doors.
<!--more-->
{{<note update>}}**2020-12-26**: The blog post was written in 2012, and I haven't heard anyone talking about EVB for years, so maybe it's truly dead by now, although it's still supported by Linux bridge, and there might be a zombie or two [lurking in a Juniper switch somewhere](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/edge-virtual-bridging.html). 

Meanwhile, IBM's vSphere virtual switch was a total failure. It was so unimpressive that nobody noticed when it disappeared.{{</note>}}

[IEEE WG is still working on the draft](http://www.ieee802.org/1/pages/802.1bg.html); the major hypervisor vendors have already moved on -- VMware has VXLAN, Microsoft has NVGRE and Xen/KVM have GRE+OpenFlow with Open vSwitch. As I predicted, the [hypervisor vendors woke up](/2011/08/imagine-ruckus-when-hypervisor-vendors/), realized [VLANs really don't scale](/2011/12/decouple-virtual-networking-from/) (there were a few old-school idiots yelling that message from their L3 ivory towers for the last few years, but nobody listened), and focused on implementing larger-scale virtualized networks with MAC-over-IP encapsulation.

{{<note>}}The truly sad part is that EVB isn't a bad technology. It's a [perfect solution if you want to use VLANs to create virtual networks](/2011/05/edge-virtual-bridging-evb-8021qbg-eases/), and its [S-component nicely solved the problem of virtual server-to-switch links](/2011/05/evb-8021qbg-s-component/) that we need in some environments.{{</note>}}

And then there's IBM: Its [DVS 5000V is the first virtual switch supporting EVB/VEPA](/2012/02/ibm-launched-nexus-1000v-competitor/), as does its [Virtual Fabric 10G switch module](http://www-01.ibm.com/support/docview.wss?uid=isg3T7000496). It's nice to see someone using standard technologies instead of proprietary solutions like Cisco's VN-Tag or HP's Virtual Connect (although IBM's documentation indicates they might have implemented a 2 year old draft). According to [the same documentation](http://www-01.ibm.com/support/docview.wss?uid=isg3T7000496), the current EVB implementation in Virtual Fabric 10G switch module doesn't support CDCP (a standard way of creating multiple NICs over the same uplink). A year ago I would have been excited; today I can't help being reminded of [ATM support on IBM Front End Processors](http://books.google.si/books?id=LhcEAAAAMBAJ&pg=PA61&lpg=PA61&dq=ATM+support+IBM+FEP&source=bl&ots=gy1pGmGO6d&sig=2pGQEqdL2sv-8Iawc4yRfxZAmo4&hl=en&sa=X&ei=MQpLT4a-CoLU0QXS9IH9DQ&ved=0CCEQ6AEwAQ#v=onepage&q=ATM%20support%20IBM%20FEP&f=false).
