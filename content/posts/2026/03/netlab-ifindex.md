---
title: "Changing Interfaces Connected to netlab Links"
date: 2026-03-30 07:27:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
Some netlab users want to accurately replicate their physical network's topology in a virtual lab. Ignoring the [obvious caveats](/2025/06/digital-twins-powerpoint-reality/) for a moment, the first hiccup is usually the interface naming. All bets are off if you're using anything but Ethernet in your actual network, but even if you did standardize on Ethernet, the container/VM interface names might not match the physical ones.

netlab provided a solution for a long time -- you can [specify interface **ifindex**](https://netlab.tools/links/#changing-interface-names) when attaching a node to a link. For example, use the following topology to connect Ethernet3 on R1 to Ethernet6 on R2:
<!--more-->
```
nodes: [ r1, r2 ]

links:
- r1:
    ifindex: 3
  r2:
    ifindex: 6
```

It's easy to do that[^SSVE], but does it work?

[^SSVE]: For some small value of _easy_

The interface naming is easy. *netlab* uses the specified **ifindex** to generate the device-specific interface name. **ifindex** set to six will result in  **eth6** on FRRouting, **Ethernet6** on Arista EOS, **GigabitEthernet0/6** on IOSv, **Ethernet1/2** on Cisco IOL, **GigabitEthernet6** on Cisco Catalyst 8000v, **GigabitEthernet0/0/0/6** on Cisco IOS XRd, and **eth7** on Junos cRPD.

However, we also need to ensure that the desired interface matches the VM/container's virtual networking hardware, and that's where things get complicated. Let's go through various scenarios:

* You're responsible for proper cabling if you're using the **external** provider (configuring physical devices with _netlab_).
* We cannot remap KVM VM NICs. The only way to ensure a VM NIC is mapped to a desired interface in your network operating system is to create as many NICs as needed. For example, with an interface having **ifindex** set to 6, *netlab* must create five bogus *private network* connections in the Vagrantfile to ensure **Ethernet6** is connected to the correct link.
* _netlab_ creates *containerlab* topology file with the desired interface names[^CLIN] in the **links** section. What happens afterwards is containerlab's responsibility.

[^CLIN]: In most cases, **ethN** for **ifindex** set to N (Nokia SR-SIM is an exception where the container interface names match the SROS port names). **eth0** is always the management interface.

You know I'm not willing to pass the buck that easily. Of course, I tested various scenarios. In all cases, *containerlab* creates non-consecutive **ethX** interfaces. What happens next depends on the virtual device implementation:

* **Pure containers** (FRRouting, Arista cEOS, cRPD, IOS XRv): The network operating system maps non-consecutive interfaces into the familiar interface names. Everything works.
* **Virtual machines running in vrnetlab containers**: *vrnetlab* start script must figure out what to do with non-consecutive interfaces. I did a few spot checks, and it worked.
* **Linux process running in a container** (IOL/IOLL2): the wrapper script sets up the correct interface mapping.

Long story short: setting interface **ifindex** in _netlab_ topology worked in all scenarios I tested. However, you'll still be limited by the number of virtual NICs a VM can have, and generating interface names for chassis devices with more than one linecard, or dealing with different linecard types, is often Mission Impossible.
