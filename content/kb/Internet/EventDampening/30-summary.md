---
kb_section: EventDampening
minimal_sidebar: true
pre_scroll: true
title: Summary
date: 2025-01-08 08:18:00+0100
---
In this article, you’ve seen how you can reduce the impact of interface flaps on the stability of your network. The IP Event Dampening feature provides a mechanism by which Cisco IOS detects highly repetitive interface flaps and temporarily disables IP routing on the interface (suppresses the interface). The suppressed interface is unavailable to any IP routing activity; the routing protocols stop sending Hello packets over the interface, and the static routes pointing to the suppressed interface (or next-hops reachable through it) are removed from the IP routing table while the interface is not operational.

You can monitor the IP event dampening status with the **show dampening interface** and the **show interface dampening** commands but cannot track it in real-time, as the object tracking feature of Cisco IOS does not take the interface suppression status into account when tracking the IP routing status of an interface (a workaround might be to configure a bogus static route pointing to the interface and track its presence).

Cisco IOS cannot track any other network instabilities (for example, unstable routing protocol adjacency); you can write Embedded Event Manager applets to track the status of a particular object (interface or routing protocol neighbor), or you could use EEM Tcl policy to implement a more generic solution.
