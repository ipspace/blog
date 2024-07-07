---
comment: 'It seems it’s easy to define what a [network device control plane](/2013/08/management-control-and-data-planes-in/)
  is (and how it’s different from the data plane)… until someone starts unearthing
  the interesting corner cases. This blog post is trying to address some of them.

  '
date: 2013-10-07 07:25:00+02:00
openflow_101_tag: intro
series:
- openflow_101
series_weight: 290
tags:
- IP routing
- SDN
title: What Exactly Is The Control Plane?
url: /2013/10/what-exactly-is-control-plane/
---
Tassos opened an [interesting can of worms](/2013/08/management-control-and-data-planes-in/#c568301941276652542) in a comment to my [*Management, Control and Data Planes*](/2013/08/management-control-and-data-planes-in.html?showComment=1378762930370) post: *Is ICMP response to a forwarded packet (TTL exceeded, fragmentation needed or destination unreachable) a control- or data-plane activity?*
<!--more-->
Other control plane protocols (BGP, OSPF, LDP, LACP, BFD \...) are more clear-cut -- they run between individual network devices (usually adjacent, but there's also targeted LDP and multihop BGP) and could be (at least in theory) made to run across a separate control plane network (or VRF).

Control plane protocols usually run over data plane interfaces to ensure [*shared fate*](http://en.wikipedia.org/wiki/Fate-sharing) -- if the packet forwarding fails, the control plane protocol fails as well -- but there are scenarios (example: optical gear) where the data plane interfaces cannot process packets, forcing you to run control plane protocols across a separate set of interfaces.

Typical control plane protocols aren't data-driven: BGP, LACP or BFD packet is never sent as a direct response to a data plane packet.

ICMP is different: some ICMP packets are sent as replies to other ICMP packets, others are triggered by data plane packets (ICMP unreachables and ICMPv6 neighbor discovery).

Trying to classify protocols based on where they're run is also misleading. It's true that the networking device CPU almost always generates ICMP requests and responses (it doesn't make sense to spend silicon real estate to generate ICMP responses). In some cases, ICMP packets might be generated in the [slow path](/2013/02/process-fast-and-cef-switching-and/), but that's just how a particular network operating system works. Let's ignore those dirty details for the moment; just because a device's CPU touches a packet doesn't make that packet a control plane packet.

Vendor terminology doesn't help us either. Most vendors talk about *Control Plane Policing* or *Protection*, equating control plane with the device CPU -- these mechanisms usually apply to control plane protocols as well as data plane packets punted from ASICs to the CPU.

Even IETF terminology isn't exactly helpful -- while C in ICMP does stand for *Control*, it doesn't necessarily imply control plane involvement. ICMP is simply a protocol that passes control messages (as opposed to user data) between IP devices.

Honestly, I'm stuck. Is ICMP a control plane protocol that's triggered by data plane activity or is it a data plane protocol? Can you point me to an authoritative source explaining what ICMP is? Share your thoughts in the comments!
