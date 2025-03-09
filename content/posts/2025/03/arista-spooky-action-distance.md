---
title: "Arista EOS Spooky Action at a Distance"
date: 2025-03-17 09:10:00+0100
tags: [ virtualization, netlab ]
netlab_tag: quirks
---
_This blog post describes yet another bizarre behavior discovered during the [netlab](https://netlab.tools/) [integration testing](https://tests.netlab.tools/)._

It started innocently enough: I was working on the [VRRP integration test](https://github.com/ipspace/netlab/blob/dev/tests/integration/gateway/02-vrrp.yml) and wanted to use Arista EOS as the second (probe) device in the VRRP cluster because it produces nice JSON-formatted results that are easy to use in validation tests.

Everything looked great until I ran the test on [all platforms on which _netlab_ configures VRRP](https://netlab.tools/module/gateway/#platform-support), and all of them passed *apart from Arista EOS* (that was [before we figured out how Sturgeon's Law applies to VRRPv3](/2025/01/sturgeon-law-vrrp-edition/)) -- a "That's funny" moment that was directly responsible for me wasting a few hours chasing white rabbits down this trail.
<!--more-->
I whittled the lab topology to the bare minimum: two routers and a host connected to the same LAN segment. I had to use Arista VMs; Arista EOS containers do not respond to pings to the VRRP IP address[^LE].

[^LE]: Another mishap in the *Networking Digital Twins* fairy tale.

{{<cc>}}Minimal VRRP lab topology{{</cc>}}
```
module: [ gateway ]
gateway.protocol: vrrp
gateway.id: 1

nodes:
  r1: { device: eos }
  r2: { device: eos }
  h:  { device: linux }

links:
- interfaces: [ r1, r2, h ]
  gateway: True
```

The lab started, and the host could ping the VRRP IPv4 address. However, when I shut down the Ethernet interface on the VRRP master, the VRRP backup router failed to respond to pings. That's not how VRRP is supposed to work, right?

The "that's funny" moment quickly turned into a "that's definitely weird" one when I discovered the root cause of the problem: when I shut down the Ethernet interface on one Arista switch, the *line protocol* on the Ethernet interface on the other switch went down.

{{<cc>}}Shutting down the Ethernet interface on R2...{{</cc>}}
```
$ netlab connect r2
Connecting to 192.168.121.103 using SSH port 22
Last login: Sun Mar  9 13:35:40 2025 from 192.168.121.1
r2#conf t
r2(config)#int eth1
r2(config-if-Et1)#shut
r2(config-if-Et1)#
```

{{<cc>}}... causes a link loss on R1{{</cc>}}
```
$ netlab connect r1
Connecting to 192.168.121.102 using SSH port 22
Last login: Sun Mar  9 13:35:40 2025 from 192.168.121.1
r1#term mon
Mar  9 13:36:24 r1 Fhrp: %VRRP-5-STATECHANGE: Ethernet1 Grp 1 state Backup -> Stopped
Mar  9 13:36:24 r1 Ebra: %LINEPROTO-5-UPDOWN: Line protocol on Interface Ethernet1 (r1 -> [r2,h]), changed state to down
```

If this were to happen with Arista EOS containers, I might have suspected that an action on one Linux interface could affect another interface connected to the same bridge. However:

* I was using VMs
* There's QEMU between the VM NIC and the interface connected to a Linux bridge
* Quantum entanglement does not work across Linux bridges (yet)
* Like Einstein, I don't believe in [spooky action at a distance](https://en.wikipedia.org/wiki/Quantum_entanglement).

{{<figure src="/2025/03/capture-libvirt-bridge.png" caption="Inter-VM connectivity in my lab">}}

The only sane conclusion was that one Arista switch told the other, "I'm shutting down this interface."

Next step: figuring out how that works. I removed VRRP from the lab topology to reduce the clutter produced by **tcpdump**, started [packet capture on the Linux bridge](/2025/03/virtual-labs-traffic-capture/), and quickly found the culprit. The Arista switch on which I shut down the Ethernet interface sent out a squeak just before it obeyed:

{{<cc>}}Packet captured at the moment the Ethernet interface was shut down{{</cc>}}
```
$ sudo tcpdump -evvv -i virbr1
tcpdump: listening on virbr1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
13:45:08.860471 08:4f:a9:fb:f2:43 (oui Unknown) > 01:1c:73:ff:ff:ff (oui Unknown), ethertype Arista Vendor Specific Protocol (0xd28b), length 19: SubType: 0xe1ba, Version: 0x0000,
	0x0000:  e1ba 0000 00                             .....
```

The same switch sent another packet when I reenabled the interface:

{{<cc>}}Packet captured after the Ethernet interface was reenabled{{</cc>}}
```
13:45:20.660672 08:4f:a9:fb:f2:43 (oui Unknown) > 01:1c:73:ff:ff:ff (oui Unknown), ethertype Arista Vendor Specific Protocol (0xd28b), length 19: SubType: 0xe1ba, Version: 0x0000,
	0x0000:  e1ba 0000 01
```

It looks like Arista's developers tried really hard to emulate [point-to-point Ethernet links](/2025/02/virtual-labs-p2p-links/), including the link loss behavior when the remote interface is shut down. That's wonderful, but unfortunately:

* They used a proprietary implementation (not that I would be aware of a standard solution they could use)
* Their implementation brings down the Ethernet interfaces on all Arista switches connected to the same bridged segment (but not on any other device).
* I couldn't find this behavior documented anywhere.
