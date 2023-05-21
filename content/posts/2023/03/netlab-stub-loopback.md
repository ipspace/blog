---
date: 2023-03-06 06:38:00+00:00
netlab_tag: guidelines
series_title: Change Stub Networks into Loopbacks
tags: [ netlab ]
title: "netlab: Change Stub Networks into Loopbacks"
---
One of the least-documented limitations of virtual networking labs is the number of network interfaces a virtual machine could have. vSphere supports up to 10 interfaces per VM, the default setting for *vagrant-libvirt* is eight, and I couldn't find the exact numbers for KVM. Many vendors claim their KVM limit is around 25; I was able to bring up a Nexus 9300v device with 40 adapters.

Anyway, a dozen interfaces should be good enough if you're building a proof-of-concept fabric, but it might get a bit tight if you want to emulate plenty of edge subnets.
<!--more-->
*netlab* supported stub links (links with a single device connected to them) from the very beginning, and I consciously chose to implement them as LAN interfaces. Who knows what weird features might be available on a LAN interface that you cannot configure on a loopback interface (across over a dozen platforms)? For example, if you want to build a simple 2-node network with LAN and WAN interface, you'll get Ethernet interfaces for the stub links:

```
defaults.device: iosv

module: [ ospf ]

nodes: [ r1, r2 ]
links:
- r1-r2
- r1:
- r2:
```

That works very well until you hit the limit mentioned above, at which point it might be a good idea to turn some of those LAN interfaces into loopbacks.

*netlab* release 1.5.0 introduced *loopback* link type. If a link has a single node attached to it and a link **type** set to **loopback**, *netlab* uses a loopback interface to implement it. For example, the following topology has a P2P link between two routers and an additional loopback interface per router to emulate a LAN network:

```
defaults.device: iosv

module: [ ospf ]

nodes: [ r1, r2 ]
links:
- r1-r2
- r1:
  type: loopback
- r2:
  type: loopback
```

Even though _netlab_ implements _loopback_ links with loopback interfaces, they still behave as stub links. For example, the IP prefix assigned to a stub link comes from the LAN pool (like for the "real" stub links).

Having a granular configuration is nice, but it's also tedious. That's why you can set the default behavior in the system defaults:

- **defaults.links.stub\_loopback** parameter (boolean, True = use loopbacks) sets system-wide behavior
- **defaults.devices.*&lt;device&gt;*.features.stub\_loopback** parameter sets the behavior for an individual device type.

For example, if you want to test how Arista vEOS works, but need a few extra devices in your lab to advertise the subnets, set the **stub\_loopback **parameter just for the extras:

```
defaults.device: iosv
defaults.devices.iosv.features.stub_loopback: True

module: [ ospf ]

nodes:
  rtr:
    device: eos
  x1:
  x2:

links:
- rtr-x1
- rtr-x2
- rtr
- x1
- x2
```

{{<note warn>}}The default settings are not checked in the same way as topology attributes -- you'll get no error message if you make a typo (do I have to explain how I know that?){{</note>}}

### Getting Started

To get more details and learn about additional features included in release 1.5.0, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

### Revision History

2023-03-06
: Fixed the initial lab topology which incorrectly included **type: loopback** (thanks a million to Sander Steffann for reporting the typo).

