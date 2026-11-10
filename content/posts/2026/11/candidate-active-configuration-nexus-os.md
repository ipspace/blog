---
title: "Candidate Configuration on Cisco Nexus OS"
date: 2026-11-11 08:16:00+0100
tags: [ automation ]
---
**TL&DR:** Third time is (supposedly) a charm. Not in this case.

It's a bit hard to understand why one would launch an enterprise data-center-grade network operating system without candidate/active configuration in the 21st century, but that's what Cisco and Arista did with Nexus OS and EOS. Arista fixed that omission with *configuration sessions* more than a decade ago[^R415]. It took Cisco *a bit* longer.

[^R415]: In mid-2015, in the 4.15.0F release, according to Gemini (you can only blame me for trusting it, but the date sounds about right).

The first attempt was the so-called *two-stage configuration commit*, which is functionally almost identical to the [Cisco IOS XR "candidate" configuration](/2026/11/candidate-active-configuration-iosxr/):
<!--more-->
* The *candidate* configuration is really a scratchpad of syntax-checked configuration commands.
* The **commit** command merges the commands on the scratchpad with the running configuration.

However:

* I couldn't find an equivalent of the **show configuration merge** command that would tell me what the running configuration will be after the **commit** command.
* The two-stage configuration works (according to Nexus OS documentation) only in interactive CLI mode, not over NX-API or NETCONF
* There can be a single active two-stage configuration session at any time.

**TL&DR:** mostly useless.

But wait, Cisco introduced *candidate configuration* in Nexus OS release 10.6(3)F (a decade after Arista EOS[^MP]):

[^MP]: That tells you everything you need to know about how much market pressure yelling networking engineers can exert 🤦‍♂️.

* It's a real candidate configuration
* You can make changes to a snapshot of the running configuration and view them with **show candidate-config diff** or view the final configuration with **show candidate-config**
* You can **commit** or **abort** the configuration process, and even exit the candidate configuration and resume at a later time (even though getting back is a bit tricky).

Looks like exactly what we need, right? Well, it is, until you try to use IS-IS. For whatever mysterious reason, the *candidate* configuration does not work with all Nexus OS features. If you try to use it on a device running IS-IS, you get an error message[^ISL]:

[^ISL]: I have to admit I didn't stumble upon this one; someone pointed me in the right direction.

```
dut# conf candidate
Error: Current running-config has commands which are not supported by candidate session.
Please check the 'show candidate-config last-unsupported' and remove the unsupported configs from running-config.
```

These are the commands that the Nexus OS release `10.6(4) [Maintenance Release]` cannot process as part of its candidate configuration:

```
dut# show candidate-config last-unsupported
feature isis
interface Ethernet1/1 ; isis network point-to-point
interface Ethernet1/1 ; ip router isis Gandalf
interface Ethernet1/2 ; isis network point-to-point
interface Ethernet1/2 ; ip router isis Gandalf
interface loopback0 ; ip router isis Gandalf
router isis Gandalf
router isis Gandalf ; net 49.0042.0101.0000.0042.00
router isis Gandalf ; is-type level-1
router isis Gandalf ; log-adjacency-changes
router isis Gandalf ; address-family ipv4 unicast
```

**To recap:** Cisco launched a device configuration feature that supports OSPF but not IS-IS in the mid-2020s. The 1980s called and want that stolen mindset back.
