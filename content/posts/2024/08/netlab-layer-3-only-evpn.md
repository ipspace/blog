---
title: "Building Layer-3-Only EVPN Lab"
date: 2024-08-08 08:38:00+0200
tags: [ EVPN, VXLAN, netlab ]
netlab_tag: vxlan_evpn
---
A few weeks ago, [Roman Dodin mentioned layer-3-only EVPNs](https://www.linkedin.com/posts/rdodin_yesterday-i-threw-in-a-question-if-someone-activity-7221853963795472384-9TB9/): a layer-3 VPN design with no stretched VLANs in which EVPN is used to transport VRF IP prefixes.

{{<figure src="/2024/08/evpn-l3vpn-topology.png">}}

The reality is a bit muddier (in the VXLAN world) as we still need transit VLANs and router MAC addresses; the best way to explore what's going on behind the scenes is to build a simple lab.
<!--more-->
Roman provided a [lab using SR Linux](https://learn.srlinux.dev/tutorials/l3evpn/rt5-only/), but what if you want to use some other devices and don't know how to configure them correctly? Let's use _[netlab](https://netlab.tools/)_ to build an EVPN network with two switches, two VRFs, and two hosts attached to each VRF. All links will be layer-3 point-to-point links, and we'll mention VLANs only because the _netlab_ [VXLAN module](https://netlab.tools/module/vxlan/) requires the [VLAN module](https://netlab.tools/module/vlan/) to work.

Here's the lab topology we'll be using:

{{<printout>}}
defaults.device: eos
provider: clab

module: [ ospf, bgp, vrf, vlan, vxlan, evpn ]
bgp.as: 65000

groups:
  _auto_create: True
  switches:
    members: [ s1, s2 ]
  hosts:
    device: linux
    members: [ h1, h2, h3, h4 ]

vrfs:
  red:
    links: [ h1-s1, h2-s2 ]
    evpn.transit_vni: True
  blue:
    links: [ h3-s1, h4-s2 ]
    evpn.transit_vni: True

links:
- s1:
  s2:
  mtu: 1600
{{</printout>}}
Let's walk through the lab topology:

* Lines 1-2: We'll use Arista cEOS containers. I'll describe [how to use other devices](#old) at the end of this blog post.
* Line 4: The Arista cEOS switches will run OSPF (to provide loopback-to-loopback connectivity), BGP (to support EVPN), VRFs (we're talking about layer-3 VPNs), VLANs (because the VXLAN module is not happy without a VLAN module), VXLAN (to implement EVPN transit VNI), and EVPN (to exchange VPN prefixes).
* Line 5: The lab will use IBGP in AS 65000.
* Lines 6-8: We'll simplify the node definition with [groups](https://netlab.tools/groups/).
* Lines 9-10: The lab has two switches: S1 and S2
* Lines 11-13: The lab has four Linux hosts: H1 through H4
* Lines 15-21: The lab has two VRFs, each with two host-to-switch links. The VRFs use EVPN transit VNI (that's how we tie VRFs with EVPN).
* Lines 23-26: We need the inter-switch link. It must have a larger MTU to transport VXLAN-encapsulated Ethernet frames.

The easiest way to start the lab is to [use GitHub Codespaces](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/) (the lab topology is in the `EVPN/l3vpn` directory). As of August 2024, you still have to [upload the cEOS container image manually](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) (or [use `frr` containers](#old))

{{<note info>}}
You can also [build your own lab infrastructure](https://netlab.tools/install/) or [run the lab in a Ubuntu VM on your laptop](https://netlab.tools/install/ubuntu-vm/) (including [Apple laptops](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/) if you're OK with using FRRouting containers).
{{</note>}}

After starting the lab with **netlab up**, you should see two IP prefixes in each VRF, and the hosts should be able to ping each other.

{{<cc>}}IP routing table in VRF red on S1{{</cc>}}
```
s1>show ip route vrf red|begin Gateway
Gateway of last resort is not set

 C        172.16.0.0/24
           directly connected, Ethernet2
 B I      172.16.1.0/24 [200/0]
           via VTEP 10.0.0.2 VNI 200000 router-mac 00:1c:73:eb:d5:13 local-interface Vxlan1

```

{{<cc>}}Pinging H2 from H1{{</cc>}}
```
$ netlab connect h1 ping h2
Connecting to container clab-l3vpn-h1, executing ping h2
PING h2 (172.16.1.4): 56 data bytes
64 bytes from 172.16.1.4: seq=0 ttl=62 time=2.902 ms
64 bytes from 172.16.1.4: seq=1 ttl=62 time=1.076 ms
64 bytes from 172.16.1.4: seq=2 ttl=62 time=1.632 ms
64 bytes from 172.16.1.4: seq=3 ttl=62 time=1.307 ms
64 bytes from 172.16.1.4: seq=4 ttl=62 time=1.743 ms
^C
--- h2 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 1.076/1.732/2.902 ms
```

{{<next-in-series page="/posts/2024/08/layer-3-only-evpn-behind-scenes.html">}}**Next step**: figure out how this design works and what other EVPN routes it requires (or wait for a follow-up blog post).{{</next-in-series>}}

### Using Other Lab Devices {#old}

You can replace cEOS containers with [any device supported by the netlab EVPN module](https://netlab.tools/module/evpn/):

* Download the device image and [build a Vagrant box](https://netlab.tools/labs/libvirt/#building-vagrant-boxes) or [a vrnetlab container](https://github.com/hellt/vrnetlab). You can skip this step if the device containers can be downloaded automatically (Cumulus Linux, FRRouting, Nokia SR Linux, VyOS)
* Change the lab topology's `defaults.device` and `provider` settings. For example, use the `frr` device to run FRRouting containers.
* Start the lab with **netlab up** and have fun ;)

Alternatively, you could:

* Start the lab with **netlab up -d _device_ -p _provider_** parameters.
* Set the NETLAB_DEVICE and NETLAB_PROVIDER [environment variables](https://netlab.tools/defaults/#changing-defaults-with-environment-variables).
