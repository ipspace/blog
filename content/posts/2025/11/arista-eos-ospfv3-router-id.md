---
title: "OSPFv3 Router ID Documentation on Arista EOS"
date: 2025-11-27 07:27:00+0100
tags: [ OSPF ]
ospf_tag: rant
---
When I published a blog post [making fun of the ridiculously incorrect Cisco IOS/XE OSPFv3 documentation](/2025/10/ospf-automatic-router-id/), an engineer working for Cisco quickly sent me an email saying, "Well, the other vendors are not much better."

Let's see how well Arista EOS is doing; this is their description of the **router-id** command (taken from EOS 4.35.0F documentation; unchanged for at least a dozen releases):

{{<figure src="/2025/11/arista-eos-ospfv3-router-id.png">}}
<!--more-->
Not too bad, apart from a few "minor" details. They should emphasize:

* The router ID selection algorithm uses IPv4 (not IPv6) addresses
* The OSPFv3 router won't start without a valid router ID, which means it's mandatory to configure it on an IPv6-only device.

The second omission is correctly explained in the Defining the Router ID section of the configuration guide, which unfortunately also contains this gem:

{{<figure src="/2025/11/arista-eos-ospfv3-cfg.png">}}

**NO, NO, NO, NO, NO,** the router ID selection algorithm does **NOT** use IPv6 addresses (see what happens when you're sloppy in the command reference, and the technical writer uses it to write the rest of the documentation).

The documentation errors are clearly annoying and may confuse users with a limited understanding of how OSPFv3 works. Even worse, there are at least three pretty hurtful implementation gotchas:

* Without a valid router ID (configured or derived from an IPv4 address), the OSPFv3 process cannot start (no surprise there). The **show** printout is somewhat unhelpful; it doesn't mention a missing router ID at all.

```
dut#show ipv6 ospf 1
  FIPS mode disabled
  Maximum number of LSAs allowed 0
    Exceed action disable
    LSA limit for warning message 75%
    Disabled-time 5 minutes, clear timeout 5 minutes
    Incident count 0, incident count limit 5
```

* When you remove a **router-id** from an OSPFv3 process, Arista EOS does not complain even when the device has no IPv4 addresses (in that VRF).
* Likewise, Arista EOS does not complain when you remove the last IPv4 address (that was used for OSPFv3 router ID) from the device.

Needless to say, when you reboot a box that has a running OSPFv3 process (for historical reasons) but no valid means of restarting it (because it no longer has IPv4 addresses or a configured **router-id**), you might end up with a bricked network.
