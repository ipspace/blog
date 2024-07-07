---
title: "netlab: VRF Instantiation on Lab Devices"
date: 2024-05-13 08:37:00+0200
tags: [ netlab ]
netlab_tag: vlan_vrf
series_title: VRF Instantiation on Lab Devices
---
In the [previous blog post on this topic](/2024/04/netlab-global-node-vrf/), I described how *node* and *global* VRFs work in *[netlab](https://netlab.tools/)*.

**TL&DR:** If you use the same VRF on multiple devices, it's better to define it globally.

However, you might not need every VRF on every lab device in a more complex lab topology. Considering that, *netlab* tries to minimize the number of VRFs configured on lab devices using a simple rule: a VRF is configured on a lab device only if the device has at least one interface in that VRF.
<!--more-->
### Simple Scenarios

Let's start with the simplest scenario: two PE routers using a single VRF[^AS].

[^AS]: The topology is simple enough to run on [Apple silicon](/2024/03/netlab-bgp-apple-silicon/).

{{<printout>}}
provider: clab
module: [ vrf, bgp, mpls, ospf ]
bgp.as: 65000
mpls.vpn: True

vrfs:
  red:
    links: [ r1-h1, r2-h2 ]

nodes:
  r1:
    device: frr
  r2:
    device: frr
  h1:
    device: linux
  h2:
    device: linux

links: [ r1-r2 ]
{{</printout>}}

Each PE router has an interface in VRF red (the link to the attached host). Red VRF is thus configured on both routers.

What about a more complex topology with inter-VRF route leaking?

{{<printout>}}
provider: clab
module: [ vrf, bgp, mpls, ospf ]
bgp.as: 65000
mpls.vpn: True

vrfs:
  red:
    links: [ r1-h1 ]
    import: [ red, blue ]
  blue:
    links: [ r2-h2 ]
    import: [ red, blue ]

nodes:
  r1:
    device: frr
  r2:
    device: frr
  h1:
    device: linux
  h2:
    device: linux

links: [ r1-r2 ]
{{</printout>}}

There's no need to configure the red VRF on R2 or the blue VRF on R1, and that's precisely what _netlab_ does. The *instantiate the VRF if it has an interface* rule works as expected.

### Loopback-Only VRFs

Sometimes, you'd like to check the PE-to-PE VRF connectivity without adding external devices to the lab topology. That is no problem; _netlab_ can add loopback interfaces to VRFs. You can create VRF loopbacks with *[loopback links](https://netlab.tools/links/#loopback-links)*[^NK] or set the **[vrf.loopback](https://netlab.tools/module/vrf/#creating-vrf-loopback-interfaces)** parameter to automatically create loopback interfaces in all- or in the specified VRFs.

[^NK]: In which case _netlab_ knows there's an interface in a VRF. Problem solved.

The simplest way to build a loopback-only-VRF topology is to set the **loopback** parameter in a VRF definition on every node:

{{<printout>}}
provider: clab
defaults.device: frr

module: [ vrf, bgp, mpls, ospf ]
bgp.as: 65000
mpls.vpn: True

vrfs:
  red:

nodes:
  r1:
    vrfs.red.loopback: True
  r2:
    vrfs.red.loopback: True

links: [ r1-r2 ]
{{</printout>}}

{{<note info>}}In an FRRouting container, use the `ip vrf exec red ping 10.2.0.1 -I 10.2.0.2` command to ping X1 VRF loopback from X2.{{</note>}}

### Pushing the Limits

Can we simplify the above topology? We could set the **vrf.loopback** global parameter and hope for the best, but that wouldn't work. _netlab_ would decide the red VRF has no interfaces on any of the nodes, find no reason to use the global VRF definition on any node, and consequently not configure the red VRF.

The minimum you must do is to mention the VRF in the node definition. That mention would (combined with the global **vrf.loopback** parameter) trigger the creation of a loopback interface in the VRF, giving _netlab_ a reason to instantiate and configure it.

{{<printout>}}
provider: clab
defaults.device: frr

module: [ vrf, bgp, mpls, ospf ]
bgp.as: 65000
mpls.vpn: True

vrf.loopback: True

vrfs:
  red:

nodes:
  r1:
    vrfs.red:
  r2:
    vrfs.red:

links: [ r1-r2 ]
{{</printout>}}

Want to make the topology a bit more cryptic? Let's move the *these nodes use red VRF* definition into a group:

{{<printout>}}
provider: clab
defaults.device: frr

module: [ vrf, bgp, mpls, ospf ]
bgp.as: 65000
mpls.vpn: True

vrf.loopback: True

vrfs:
  red:

groups:
  red_group:
    members: [ r1, r2 ]
    vrfs.red:

nodes: [ r1, r2 ]

links: [ r1-r2 ]
{{</printout>}}

