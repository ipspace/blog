---
title: "SR-MPLS or SRv6 for Greenfield Networks"
date: 2022-09-22 07:05:00
tags: [ MPLS, segment routing]
---
Here's an [interesting question](https://twitter.com/ccurtis584/status/1563950747120979968) randomly appearing in my Twitter feed:

> If you had a greenfield network, would you choose SR-MPLS, or SRv6? And why?

**TL&DR**: SR-MPLS, assuming you're building a network providing end-to-end connectivity between hardware edge devices.

Now for the _why_ part of the question:
<!--more-->
* SR-MPLS is just a different (better) control plane for the ancient MPLS data plane. All you need to use it on existing hardware is a software update. SRv6 is a brand-new data plane technology and might not be available in the gear you're interested in.
* SR-MPLS is still simple label swapping. You might need longer label stacks, but that's it. SRv6 (assuming we can agree which version of it we want to use -- there's also SRm6) is way more complex to implement in hardware, which might result in more expensive hardware.
* The overhead of SR-MPLS is just the MPLS label stack. The overhead of SRv6 is a set of IPv6 extension headers plus a brand new IPv6 header in case the payload is not an IPv6 packet.
* There are tons of technologies riding on top of MPLS, including FRR/LFA, L3VPN, 6PE, and EVPN. Replacing LDP with SR-MPLS does not affect any of them (OK, LFA gets easier ;). Of course you can implement all of these technologies on top of SRv6, but that requires new code, which inevitably results in new bugs.
* If you believe in centralized controller-based networking (because that worked so well in Frame Relay and IBM SNA days), you can use a controller to push the SR-MPLS label stack or SRv6 extension header chain into network nodes.

But wait, it gets worse. Contrary to the popular PowerPoint-based wisdom:

* [SRv6 is no more secure than MPLS](/2021/11/worth-reading-srv6-insecure/).
* SRv6 running on top of public IPv6 network is therefore as secure as MPLS-over-GRE-over-IP.
* SRv6 does not enable service insertion any more than VXLAN, Geneve, Network Services Header (NSH), or MPLS.

A quick detour into the _service insertion_ land:

* You can always [implement service insertion](https://my.ipspace.net/bin/get?doccode=SDNUses&id=4961e898-4de2-11e3-a4ce-005056880254) with VLAN- or VRF stitching (even in [VXLAN/EVPN world](https://my.ipspace.net/bin/list?id=EVPN#L47SVC)).
* Implementing any other type of service insertion requires cooperation between the network and the node providing the service[^EXR]. That's why VMware NSX requires [tight integration with the software providing east-west traffic inspection](https://my.ipspace.net/bin/list?id=NSX#FW), and why NSH never took off.
* Anything else is PowerPoint-based handwaving (although I would love to be proven wrong).

[^EXR]: The proof is left as an exercise for the reader

Does that mean that SRv6 makes absolutely no sense? Not exactly; if you want to push traffic through virtual machines or containers, it's (conceptually) easier to use SRv6[^VSR] than SR-MLPS as you don't have to think about pulling LSPs into your virtual world[^VLSP]. As soon as you open that can of worms, you have to ask "_wrong with VXLAN or Geneve?_" or "_what extra value does SRv6 bring?_" unless you desperately want to have *Segment Routing* because it sounds cool.

[^VLSP]: Hint: just because you could build SR-MPLS paths into containers or virtual machines doesn't mean that you should. If you want to insert virtualized workloads into a forwarding path, use something that rides on top of IPv4/IPv6.

[^VSR]: Ignoring for the moment the pain of making sure containers have all the necessary Linux drivers, and the pain of provisioning all those extra tunnel interfaces before starting the containers.
