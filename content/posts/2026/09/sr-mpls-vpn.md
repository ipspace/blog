---
title: "MPLS/VPN with SR-MPLS Core"
date: 2026-09-15 07:45:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: ws
netlab_tag: ignore
---
As we discussed in the [BGP-Free Core with SR-MPLS](/2026/09/sr-mpls-bgp-free/) blog post, SR-MPLS works as a drop-in replacement for the traditional MPLS control plane. No wonder it works well (when properly implemented) with MPLS/VPN services -- the second "[fun](https://github.com/ipspace/SR-workshop/blob/main/2-fun)" scenario in my ITNOG10 [Segment Routing workshop](/2026/04/sr-mpls-workshop/). It uses the same topology as the BGP-Free Core scenario:

{{<figure src="/2026/09/sr-mpls-fun.png" caption="Simplest possible MPLS/VPN network with SR-MPLS core">}}
<!--more-->

### Does It Work?

Of course. After the BGP session is established between the PE routers (which implies IS-IS is working), the VRF routes get the familiar two-label stack:

{{<printout highlight="yes" caption="VRF route with a VPNv4 and an SR-MPLS label observed on PE1 running on Arista EOS">}}
pe1#show ip route vrf tenant 172.16.1.0/24 | begin 172.16
 B I      172.16.1.0/24 [200/0]
           via 10.0.0.3/32, IS-IS SR tunnel index 2, label <b>116384</b>
              via 10.1.0.1, Ethernet1, label <b>900003</b>
{{</printout>}}

### Lab Topology {#lab}

Here are the changes I made to the [lab topology](https://github.com/ipspace/SR-workshop/blob/main/2-fun/2-mpls-vpn/topology.yml) to enable MPLS/VPN services:

* I had to enable MPLS/VPN and disable LDP:

{{<printout caption="Global MPLS settings">}}
mpls.vpn: True
mpls.ldp: False
{{</printout>}}

* The *edge* devices (PE routers) use a different set of modules: IS-IS, SR-MPLS, BGP, MPLS (which includes MPLS/VPN) and VRF:

{{<printout caption="Modified definition of the edge group">}}
groups:
  edge:
    members: [ pe1, pe2 ]
    module: [ isis, bgp, sr, mpls, vrf ]
{{</printout>}}

* Finally, the PE-to-host links are moved to the *tenant* VRF:

{{<printout caption="Links in the tenant VRF">}}
vrfs:
  tenant:
    links: [ ha-pe1, hb-pe2 ]
{{</printout>}}

### Try It Out

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first. After that, you can:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Change directory to `2-fun/2-mpls-vpn`
* Execute **netlab up**
* Have fun
