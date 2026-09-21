---
title: "The OSPF MTU Mismatch Saga"
date: 2026-09-23 08:07:00+0200
tags: [ OSPF ]
ospf_tag: details
---
The *OSPF is stuck in database exchange state* symptom is probably familiar to every networking engineer who ever had to pass a certification exam. It's caused by the MTU mismatch between adjacent OSPF routers.

The recent (unexpected) trip into the *[how crazy is it to declare your interface MTU to be zero](/2026/08/junos-ospfv3-tunnels/)* wonderland uncovered way more than I ever wanted to know about this arcane topic. Here are a few highlights (thanks a million to [Aleksey Popov](https://www.linkedin.com/in/popovalexey/) for researching this topic and posting information [here](https://blog.ipspace.net/2026/08/junos-ospfv3-tunnels/#3057), [here](https://github.com/ipspace/netlab/issues/3657), and [here](https://www.linkedin.com/feed/update/urn:li:activity:7498258758863691776/)).
<!--more-->
The early versions of the OSPFv2 protocol did not care about the interface MTU. [RFC 1583](https://www.rfc-editor.org/info/rfc1583/) did not have the MTU field in its [database description packet](https://www.rfc-editor.org/info/rfc1583/#appendix-A.3.3). It relied on IP fragmentation to send the oversized OSPF packets ([page 35](https://www.rfc-editor.org/info/rfc1583/#page-35), section 4.3):

> The OSPF protocol runs directly over IP, using IP protocol 89. OSPF does not provide any explicit fragmentation/reassembly support. When fragmentation is necessary, IP fragmentation/reassembly is used.

Regardless of that wording, they realized early on that this is a bad idea. The very next statement says:

> OSPF protocol packets have been designed so that large protocol packets can generally be split into several smaller protocol packets. This practice is recommended; IP fragmentation should be avoided whenever possible.

Let's recap this gem before moving on: a single paragraph says, "_you can use X, but you should not use X._" That wording goes all the way back to RFC 1131 (the original OSPFv2 RFC) and remains in the final version of OSPFv2 specs (RFC 2328/STD 54). IETF at its finest[^GBI].

[^GBI]: A sarcastic mind might assume that a loud-enough vendor had an implementation that used IP fragmentation and viciously opposed any attempt to clean that up. 

Anyway, IP fragmentation isn't the only problem one has to deal with when faced with (overly) large packets. A device using fixed-size buffers might not be able to receive a packet larger than the interface MTU[^MRU]. A revision of OSPFv2 specified in [RFC 2178](https://www.rfc-editor.org/info/rfc2178/) tried to solve that problem by cramming the MTU into an OSPFv2 packet with enough "unused" bits while retaining backward compatibility with RFC 1583.

[^MRU]: Technically, an interface has an MTU (Maximum Transmission Unit) and MRU (Maximum Receive Unit). Most of the time (including when [writing bridging software](/2025/03/linux-bridge-mtu-hell/)), everyone assumes that MRU == MTU.

It turned out that the hello packets (where the "these are the things I can do" settings would belong) had no free space, so they put the "this is my MTU" value into the database description (DBD) packet, resulting in the well-known crazy behavior of two routers establishing adjacency and then getting stuck in the database exchange (ExStart) state.

Anyway, late revisions of OSPFv2 tried to retain backward compatibility with RFC 1583, so they specified a lax MTU check:

> If the Interface MTU field in the Database Description packet indicates an IP datagram size that is larger than the router can accept on the receiving interface without fragmentation, the Database Description packet is rejected.

RFC 1583 specified that that particular part of the DBD packet should be zero (reserved), so an RFC 1583 router (which would ignore the MTU field) would be able to talk to an RFC 2328 router (which would accept the DBD packet because zero is always less than the interface MRU). Most OSPFv2 code uses the "less than or equal to MRU" check for RFC 1583 compatibility.

OSPFv3 took the easy way out and refers to OSPFv2 in its [Receiving Protocol Packets](https://datatracker.ietf.org/doc/html/rfc5340#section-4.2.2) section. However, once the restriction on accepting mismatched MTU values to retain RFC 1583 compatibility was lifted, some OSPFv3 implementations (notably [FRR](https://github.com/ipspace/netlab/issues/3657#issuecomment-5435809420)) started enforcing a strict MTU match. I'd appreciate a comment in case you have a definitive answer on why they decided to do that; I can only guess that real life taught the OSPFv3 implementers that it's better to reject an OSPF adjacency than deal with an even crazier case of a remote router ignoring the MTU (this time due to a twisted nerd knob) and then dropping incoming OSPF updates.

{{<note>}}
Checking which vendors enforce a strict MTU check versus a more relaxed one prescribed in the RFC is trivial if you invested time into [installing netlab](https://netlab.tools/install/) and building [containers](https://netlab.tools/labs/clab/#clab-vrnetlab)/[boxes](https://netlab.tools/labs/libvirt/#vagrant-boxes) for your network devices. Just saying 😎
{{</note>}}

Anyway, as we [figured out the hard way](/2026/08/junos-ospfv3-tunnels/), there are OSPFv3 implementations out there that send DBD packets with crazy values over tunnels, and others that enforce strict MTU checks. I guess "Caveat emptor" still applies after more than 2000 years.

Finally, I hope you didn't expect any guidance from the IETF. When someone tried to add an [OSPFv3 errata](https://mailarchive.ietf.org/arch/browse/lsr/?gbt=1&index=vUyvzp5zohq3dgET31DEFm6Fhso) saying "_sending DBD packets claiming your interface MTU is zero is plain wrong_", he got (technically correct) [response](https://mailarchive.ietf.org/arch/msg/lsr/MHwPz6zIQ0olkyyW4MsK4qvfKdk/) like "_Gee, sending OSPFv3 DBD packets with MTU=0 is perfectly fine, the receiver is broken if it rejects it,_" and nothing changed. Even better, the (again, technically correct) [conclusion](https://mailarchive.ietf.org/arch/msg/lsr/wXdOtU9H2vIoA1xs10xZ4oh8bwU/) was "_an OSPFv3 adjacency over a tunnel should NOT be misconstrued as an OSPFv3 virtual link, and the Errata is invalid_" where the errata author wanted to clarify that the "_you can set MTU to zero_" case MUST NOT apply to interfaces 🤦‍♂️. I suggest you make some popcorn and read the whole thread.
