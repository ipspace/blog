---
title: "What Happened to FabricPath and Its Friends?"
date: 2022-05-03 06:59:00
tags: [ fabric, data center ]
---
Continuing the [*what happened to old technologies* saga](/2022/04/x25-still-alive.html), here's [another question](/2022/04/do-you-care-about-mpls.html#1137) by Enrique Vallejo:

> Are FabricPath, TRILL or SPB still alive, or has everyone moved to VXLAN? Are they worth studying?

TL&DR: Barely. Yes. No.

[Layer-2 Fabric craziness exploded in 2010](/2010/08/how-many-large-scale-bridging-standards.html) with vendors playing the [usual misinformation games](/2011/03/dont-lie-about-proprietary-protocols.html) that eventually resulted in totally fragmented market full of partial- or proprietary solutions. At one point in time, some HP data center switches supported only TRILL, and other data center switches *from the same company* supported only SPB.

Now for individual technologies:
<!--more-->
* I wrote the [last major blog post about TRILL](/2012/08/the-state-of-trill.html) in 2012. As Gartner would say, TRILL died before it [reached the through of disillusionment](https://en.wikipedia.org/wiki/Gartner_hype_cycle)[^SDN].
* [Juniper QFabric](/2011/09/qfabric-part-1-hardware-architecture.html) was the first to die[^QFEOL]. Scaling a centralized control and management plane to 128 switches is a hard task, and even though Juniper might have been best-positioned to make it work (and had decent architecture), in the end they still failed.
* Juniper Virtual Chassis was a lame attempt to make stackable switches work in data center environment, and even [Virtual Chassis Fabric](/2013/11/finally-juniper-supports-leaf-and-spine.html) couldn't save the day. Running a single control plane for the whole fabric on an underpowered switch CPU is obviously not a good idea (see also: OpenFlow).
* When Nexus 9000 switches were launched without FabricPath support in 2013, the writing on the wall was very obvious. I wouldn't be surprised to see FabricPath deployments in the wild, but anyone considering it for a Greenfield deployment should look at the calendar.
* Brocade was the last data center switching vendor worth mentioning that abruptly joined the EVPN/VXLAN lemming run in 2016, dropping VCS Fabric like a steaming pile of ****.
* HP[^HP] was overpromising and underdelivering until they managed to become irrelevant. The were telling us they planned to support TRILL, SPB, and FCoE at Networking Field Day 1 in 2010, and [couldn't deliver a single one of those protocols](/2013/05/update-trill-on-hp-data-center-switches.html) by the time of Nexus 9000/ACI launch. They did manage to deliver in the end, but it was already too late. [According to Philipp](#1197), HPE is still selling H3C-developed switches with Comware version 7 that supports VXLAN with EVPN. They also push Aruba switches these days, and while (according to data sheets) they support VXLAN/EVPN, there's zero mention of TRILL or SPB.

[^SDN]: Gartner made a similar claim about SDN in its 2021 [Networking Hype Cycle document](https://blogs.gartner.com/andrew-lerner/2021/10/11/networking-hype-cycle-2021). I'm not sure product marketers working for networking vendors got the memo.

[^QFEOL]: More precisely, a [migration document from 2019 says](https://www.juniper.net/documentation/en_US/release-independent/nce/topics/concept/nce-169-qfabric-evpn-vxlan-migration-tech-overview.html) "_Juniper Networks continues to support QFabric Systems, but many of the hardware devices in QFabric Systems have reached end of life (EOL) status._"

[^HP]: An entity now known as HPE because someone realized pouring huge profits from toner packages into developing products that consistently stay in the "others" category in industry surveys makes no sense. I couldn't figure out what happened with H3C, the company developing the data center switches HP/HPE was selling under their own brand until the Aruba acquisition.

How about standard-based layer-2 fabric implementations? I'm not aware of anyone (apart from HPE) ever implementing TRILL[^TRILL]. Avaya had [interesting SPBM implementation](/2014/04/is-is-in-avayas-spb-fabric-one-protocol.html) ([more details](/2016/04/shortest-path-bridging-spb-and-avaya.html)), and they're [still selling SPBM switches](/2016/12/would-you-use-avayas-spbm-solution.html) under the Extreme brand. I've heard someone mentioning a SP-focused vendor (Alcatel Lucent?) using SPB in Carrier Ethernet implementations a while ago, but I never looked at the details. 

I probably missed a few things, in which case a comment from someone with more details (preferably with links to product documentation) would be most welcome.

[^TRILL]: However, there's always someone saying "_I could use this technology to solve X_". According to [Kevin Myers](https://twitter.com/stubarea51/status/1521623586435444744?s=27&t=KXFFusJOyV2VgLVQklG26A), at least one company uses TRILL in their [fixed wireless mesh products](https://www.ignitenet.com/network-switches/meshlinq).

### Revision History

2022-05-03
: Added more information on HPE data center switches

2022-05-04
: Added a footnote pointing to a TRILL implementation.
