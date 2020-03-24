---
title: "Automation Example: Drain a Circuit"
tags: [ automation, WAN ]
date: 2020-03-24 07:19:00
---

One of the attendees of our [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course asked an interesting question in the course Slack team:

> Has anyone wrote a playbook for putting a circuit into _maintenance mode_ — i.e. adjusting metrics to drain traffic away from a circuit that is going to be taken down for maintenance?

As always, you have to figure out what you want to do before you can start to automating stuff.
<!--more-->
**Notes**:

* We're talking about controlled gradual drain, not abrupt disruption;
* It's circuit drain, not node drain. The latter is easy to solve with a simple configuration change in most IS-IS and OSPF implementations;
* You might not have this challenge if you're using BGP as your routing protocol, and use boxes supporting BGP shutdown community (or have an interestingly complex BGP configuration).

If you’re using OSPF or IS-IS as the routing protocol, then you have to tweak metrics on both ends of the link (so you have to know both devices and corresponding interfaces), if you use BGP then you can apply inbound and outbound route-maps, so you only need to know one end of the link (device/interface).

In the ideal case, you’d have a nodes+links source-of-truth describing your network ([sample solution](https://github.com/ipspace/ansible-examples/tree/master/OSPF-Deployment)), or something equivalent in a network-centric IPAM like NetBox. After having that information, it’s trivial to say “_bring this circuit into maintenance mode_” - extract nodes and interfaces from the circuit description, and apply configuration commands.

Meanwhile on Planet Enterprise: there is no source of truth, and nobody has a clue how to build one.

You could [reverse-engineer the network topology using LLDP](https://github.com/ipspace/ansible-examples/tree/master/LLDP-to-Graph) using LLDP and build your source-of-truth from LLDP information, or import whatever Excel data you have into a reasonable data model or anything else along those lines. The information gathered with LLDP is probably highly reliable (assuming your naming conventions are consistent, and you run LLDP on all interfaces), anything else should be validated before being trusted.

{{< note info >}}I also wrote a sample playbook that [creates a data model based on interface description](https://github.com/ipspace/ansible-examples/tree/master/Description-to-Links) in case you think you can trust that information (because we're so diligently updating those descriptions every time someone moves a cable due to a faulty transceiver, right?){{< /note >}}

Worst case, assuming you’re running OSPF or IS-IS, use **show neighbors** command to get router IDs on all links, figure out the local router ID, and match the two. If you decide to go down this path, I’d split the workflow into two stages:

* Identify all links that might lead from R1 to R2;
* Have the operator select one of those and put it into maintenance mode.

After all, you don’t want to put all parallel links between two nodes into the maintenance mode at the same time, right? ;))

Want to learn how to get this done? If you insist on using Ansible (custom Python code might be better in this particular case), check out our [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar, but if you need a bigger picture (like the mental framework I used to write this blog post), our [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) course might be exactly what you're looking for.
