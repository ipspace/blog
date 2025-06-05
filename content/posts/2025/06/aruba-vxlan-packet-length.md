---
date: 2025-06-12 07:08:00+0200
title: "ArubaCX Cannot Count When Dealing with VXLAN"
tags: [ netlab ]
netlab_tag: quirks
---
_This blog post describes yet another [bizarre example of how reliable digital twins are](/tag/netlab#quirks), but don't worry; they all work great in PowerPoint._

After "fixing" the integration tests to deal with ArubaCX's notion of [VXLAN VNI having 16 bits](/2025/05/arubacx-vxlan-vni-arp/), the bridging test worked, but the IRB tests kept failing.

In the IRB test, the lab has two layer-3 switches. Each of them should be able to *bridge* within a VLAN/VXLAN segment and *route* across the segments.
<!--more-->
For example, H1 should be able to ping H2 (bridging), as well as H3 and H4 (routing). The way _netlab_ sets up the lab, all hosts use S1 (ArubaCX) as the default gateway.

{{<figure src="/2022/09/vxlan-bridging.png" caption="Lab diagram">}}

This is the lab topology I was using (it has been [adjusted in the meantime](https://github.com/ipspace/netlab/blob/3451ac559d5b030b1d65fca57b6a27723a30721a/tests/integration/vxlan/03-vxlan-irb.yml) to deal with ArubaCX):

{{<printout>}}
module: [ vlan, vxlan, ospf ]

groups:
  _auto_create: True
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux
    provider: clab

nodes:
  s1:
    device: arubacx
  s2:
    device: frr
    provider: clab

vlans:
  red:
    vni: 5000
    ospf.passive: True
    links: [ s1-h1, s2-h2 ]
  blue:
    vni: 5001
    ospf.passive: True
    links: [ s1-h3, s2-h4 ]

links:
- interfaces: [ s1, s2 ]
  mtu: 1600

tools:
  edgeshark:
{{</printout>}}

The test results were disheartening:

* The lab worked with two ArubaCX virtual machines
* It failed when S2 was replaced with an FRR container
* It worked (again) when S2 was an Arista vEOS virtual machine, but not when it was an Arista cEOS container.
* Everything started working when I rebooted my _netlab_ server.

Fortunately, if the [previous troubleshooting exercise](/2025/05/arubacx-vxlan-vni-arp/) taught me anything, it was to do a packet capture before wasting time on anything else. _netlab_ includes support for the excellent [Edgeshark](https://edgeshark.siemens.io/) tool, so I was able to perform [packet capture](/2025/06/ws-arubacx-arp.pcapng.gz) on my Mac OS laptop from my Ubuntu server, which was ~50 km away (yay, Tailscale!).

Here's the VXLAN-encapsulated ARP request (captured on the link between S1 and S2) sent from H1 before it tries to ping H2:

{{<figure src="/2025/06/ws-arp-intra-subnet.png">}}

And here's the VXLAN-encapsulated ARP request for H3 sent by S1 (ArubaCX) when it tries to route the packet from H1 to H3:

{{<figure src="/2025/06/ws-arp-aruba.png">}}

Can you spot the difference? Even though the two packets have the same size (Ethernet frames are 92 bytes long), the IP packet length and the UDP payload length don't match. ArubaCX claims the packet contains four bytes more than it does.

**Long story short:** VXLAN packets generated *by ArubaCX routing process* have invalid length. The likely culprit is the VLAN tag attached to the packet before it enters the (software) VXLAN encapsulation process. The VLAN tag is removed (as it should be), but the packet length is not adjusted.

Now for the fun part: why did the test sometimes work? It's evident that most VXLAN implementations don't verify the IP or UDP packet length (a bad idea), or the test could never work with devices from other vendors. But why did Arista vEOS accept the packet when it never reached Arista cEOS?

Welcome to the wonderful world of Linux bridges that love to [masquerade as firewalls](/2025/03/linux-bridge-mtu-hell/) and *sometimes* decide it's their job to filter invalid IP traffic. Fortunately, we can do a packet capture on interfaces connected to a Linux bridge to verify who the culprit is, and here's what was going on in my server:

* _netlab_ uses [libvirt UDP tunnels](/2025/02/virtual-labs-p2p-links/) to create point-to-point inter-VM links. ArubaCX VM and Arista vEOS VM are thus connected with a UDP tunnel, and the Linux bridge is not involved.
* _netlab_ has to use a Linux bridge to connect ArubaCX VM and Arista cEOS (or FRR) container, and the Linux bridge dropped the packets with an invalid IP length.
* It seems that the FRR VM (Debian Bookworm) checks the IP packet length, while the FRR container does not.

Finally, why did things start to work after I rebooted the server? The firewall-on-a-bridge is an add-on module that is not loaded at boot time, so the test works after a server reboot. However, something (and I wasn't able to figure out what) triggers the loading of that kernel module, and from that point onwards, the ArubaCX VM can no longer send VXLAN-encapsulated ARP requests to adjacent containers.

Maybe we should rename the Linux bridge to a Heisenberg bridge? If it works, you don't know why, and if you think you know how it's configured, it works in unpredictable ways.
