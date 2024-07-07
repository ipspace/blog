---
cdate: 2022-07-06
comment: 'The real-life approach of numerous vendors I’ve seen during [Networking
  Field Day 2 and OpenFlow Symposium](/2011/10/network-field-day-first-impressions/)
  made me overly optimistic – I thought we just might be able to get to real-life
  OpenFlow and SDN use cases without the usual vendor jousting and get-rich-quick
  startup mentality.


  I wrote the following blog post in October 2011. Looking back (from a safe distance
  of over a decade), I was wrong. Nothing much came out of OpenFlow.

  '
date: 2011-10-30 19:40:00.001000+01:00
sdn_hype_tag: initial
series:
- sdn_hype
tags:
- SDN
- OpenFlow
title: I Apologize, but I’m Excited
url: /2011/10/i-apologize-but-im-excited/
---
The last few days were exquisite fun: it was great meeting so many people focusing on a single technology (OpenFlow) and concept (Software-Defined Networking, whatever that means) that just might overcome some of the old obstacles (and introduce new ones). You should be at least a bit curious what this is all about, and even if you don't see yourself ever using OpenFlow or any other incarnation of SDN in your network, it never hurts to enhance your resume with another technology (as long as it's relevant; don't put CICS programmer at the top of it).
<!--more-->
Watching the [presentations from the OpenFlow symposium](http://techfieldday.com/2011/openflow-symposium/) is a great starting point. I would start [with the ones from Igor Gashinsky (Yahoo!) and Ed Crabbe (Google)](http://techfieldday.com/2011/yahoo-google-openflow-technology/) -- they succinctly explained the problems they're facing in their networks and how they feel OpenFlow could solve them. If you're an IaaS cloud provider, this is the time to start thinking about potentials OpenFlow could bring to your network, and if you're not talking to NEC, BigSwitch or [Nicira](/2011/10/what-is-nicira-really-up-to/), you're missing out. I would also talk with Juniper (more about that later).

Next step: watch the [vendor presentations from the OpenFlow symposium](http://techfieldday.com/2011/openflow-presentations-bigswitch-brocade-cisco-nec-juniper/). Kyle Forster presented a [high-level overview of Big Switch architecture](http://static.techfieldday.com/wp-content/uploads/2011/10/BSN+Concept+PP+15+mins+10-24-11.pdf), Curt Beckmann from Brocade added a [healthy dose of reality check](http://static.techfieldday.com/wp-content/uploads/2011/10/BrocadeAppliedOpenFlow10-26-11.pdf) (highly appreciated), David Meyer (Cisco) presented an [interesting perspective on robustness and complexity](http://static.techfieldday.com/wp-content/uploads/2011/10/dmm-symposium.pdf) (and several OpenFlow use cases), Don Clark from NEC talked about their OpenFlow products (watch the video, PDF is not online) and finally David Ward from Juniper presented the hybrid approach: [use OpenFlow *in combination* (not as a replacement) with existing technologies](http://static.techfieldday.com/wp-content/uploads/2011/10/jnpr-dward.pdf).

The [afternoon technical Q&A panel](http://vimeo.com/31205206) just confirmed that numerous vendors well understand the challenges associated with OpenFlow deployments outside of small lab setups, and that they're actively working on solving those problems and making OpenFlow a viable technology.

Two vendors expanded their coverage of OpenFlow during the Network Field Day: David Ward from Juniper did a [technical deep dive](http://techfieldday.com/2011/juniper-presents-networking-field-day-2/) (don't skip the Junos automation part at the beginning of the video, it's interesting... and you just might spot the VRF Smurf) and [NEC even showed us a demo of their OpenFlow-based switched network](http://techfieldday.com/2011/nec-presents-networking-tech-field-day-2/).

Luckily there are still some coolheaded people around (read Ethan Banks' [OpenFlow State of the Union](http://packetpushers.net/openflow-state-of-the-union-reflections-on-the-openflow-symposium/) and Derick Winkworth's [More Open Flow Symposium Notes](http://packetpushers.net/more-open-flow-symposium-notes/)), but I can't help myself. The grumpy old man from L3 ivory tower is excited (listen to [PacketPushers OpenFlow/SDN podcast](http://packetpushers.net/show-71-openflow-sdn-vxlan-controllers-wishing/) if you don't believe me), and not just about OpenFlow. I still can't believe that I stumbled upon so many interesting or cool technologies or solutions in the last few days. Could be that it's just vendors adapting to the blogging audience, or there actually might be something fundamentally new coming to light like MPLS (then known as *tag switching*) was in the late 1990s.

**Disclosure**: vendors mentioned in this post indirectly covered my travel expenses. [Read the full disclosure](/2011/10/network-field-day-first-impressions.html#NFD2_disclosure) (or a [more precise one by Tony Bourke](http://datacenteroverlords.com/2011/10/31/brace-yourself-networking-field-day-posts-are-coming/)).
