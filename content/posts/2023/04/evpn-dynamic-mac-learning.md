---
title: "Is Dynamic MAC Learning Better Than EVPN?"
date: 2023-04-26 06:51:00
tags: [ bridging, EVPN ]
---
One of my readers worried about the control-plane-induced MAC learning lag in EVPN-based networks:

> In all discussions about the advantages/disadvantages of VXLAN/EVPN, I can't find any regarding the lag in learning new macs when you use the control plane for mac learning.

EVPN is definitely slower than data plane-based dynamic MAC learning (regardless of [whether it's done in hardware or software](https://blog.ipspace.net/2023/03/dynamic-mac-learning-hw-cpu.html)), but so is [MLAG](/series/mlag.html).
<!--more-->
{{<note "content-box small-margin">}}**Aside:** I had a customer that used an MLAG cluster with thousands of MAC addresses (VMs) reachable through an orphan (single-node) trunk link. It took minutes for the network to converge after a link failure that moved all those nodes to another orphan link due to the control-plane propagation of MAC reachability information.

That design was as awful as one could make it, but they inherited years of "organic growth" and that was the best they could do.
{{</note>}}

Anyway, while there's a noticeable difference between data-plane and control-plane MAC learning, the real question is "_does it matter?_". Back to my reader:

> This has implications in how much BUM traffic is generated when someone starts a communication with a silent host, or when you do vMotion. While in data plane learning you measure this time in ms, in control plane learning it can take hundreds of ms or in some vendors seconds.

The BUM traffic concern is valid, but I wonder how often we see silent hosts these days. If nothing else, at least some network devices periodically refresh their ARP caches -- if they've seen a host once, they'll send it an ARP request every now and then. Furthermore, you'd need a silent host combined with a heavy burst of UDP traffic[^PLE] to generate noticeable amount of BUM traffic. Plausible, but not likely.

[^PLE]: ... or TCP sessions with no idle detection.

The vMotion argument is more worrying, until you realize the "_at most one ping lost_" claim people love to make is nonsense[^SPL]. vMotion is [neither instantaneous nor lossless](https://blog.ipspace.net/2020/03/the-myth-of-lossless-vmotion.html), and while nobody wants to publish the measurements[^PM], the final step of the vMotion process (freeze-transfer-thaw-resume) takes milliseconds.

[^SPL]: Ping packets are usually sent once per second. If vMotion-induced outage takes half a second you have a 50% chance of not losing a ping. Furthermore, the usual ping timeout is two seconds. If you do lose a packet, it's likely you won't lose the next one two seconds later.

[^PM]: For whatever reason Spirent didn't want the _actual vMotion performance_ part of their Networking Field Day presentation recorded.

EVPN definitely adds extra delay to the vMotion process. After all, the target hypervisor sends the RARP packet[^RARP] once the VM is ready. From the real-life anecdata perspective, I know plenty of organizations running either EVPN/VXLAN or Cisco ACI, and nobody ever complained about the connectivity problems following VM moves. If you have a counterexample, please write a comment.

**Long story short:**

* Assuming the BGP update timers are tweaked down to zero, EVPN control-plane delay is probably not a big deal in networks with reasonable number of MAC addresses and reasonable amount of churn.
* When in doubt, don't vMotion VoIP gateways or high-performance workloads. Your users might notice.

### More Details

As always, you'll find hours of relevant content in these ipSpace.net webinars:
 
* [Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)
* [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
* [vSphere 6 Networking Deep Dive](https://www.ipspace.net/VSphere_6_Networking_Deep_Dive)
* [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) 

[^RARP]: Because VMware never bothered to figure out how to find the IP address of the VM, and RARP was the only broadcast packet they could find that did not need an IP address in the payload. Everyone else uses gratuitous ARPs.
