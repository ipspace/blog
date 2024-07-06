---
title: "Where Do We Need Smart NICs?"
date: 2020-09-09 06:44:00
tags: [ switching ]
---
We did a number of Software Gone Wild podcasts trying to figure out whether smart NICs address a real need or whether it's just another vendor attempt to explore all potential markets. As expected, we got opposing views from [Luke Gorrie claiming a NIC should be as simple as possible](/2018/09/smart-or-dumb-nics-on-software-gone-wild.html) to [Silvano Gai explaining how dedicated hardware performs the same operations at lower cost, lower power consumption and way higher speeds](/2020/05/smartnic-pensando-podcast.html).

In theory, there's no doubt that Silvano is right. Just look at how expensive some router line cards are, and try to figure out how much it would cost to get 25.6 Tbps of forwarding performance that we'll get in a single ASIC (Tomahawk-4) in software (assuming ~10 Gbps per CPU core). High-speed core packet forwarding has to be done in dedicated hardware.
<!--more-->
Back to the network edge. In practice, one has to balance the tradeoffs of increased software complexity caused by smart NICs against the cost of the CPU cores needed for software-based packet forwarding. While software developers yearn for simplicity, NIC vendors would love you to believe you cannot reach the performance you need with software-based packet processing. Even worse, there are still people justifying smart NICs with ancient performance myths. Here's a sample LinkedIn comment I got in June 2020:

> I think you are forgetting one if the major reasons for the rise of smart NICs; that being that ability to process high speed networking packet streams at line rates and to perform operations on the packet streams. You old x86 processor with an average PCIe 4-lane dumb NIC card is not to the task up for 25 Gbps networks or higher.

How about a few facts:

* x86 server architecture hasn't been a limiting factor for ages. Luke Gorrie [demonstrated how to push 200 Gbps from an off-the-shelf x86 server in 2013](https://twitter.com/lukego/status/327714050219847680), managed to do that with [two CPU cores and 64-byte packets in 2016](https://twitter.com/lukego/status/721693707251105792), and explained his ideas in details in the [very first episode](/2014/06/snabb-switch-and-nfv-on-openstack-in.html) of Software Gone Wild.

{{<note info>}}Luke "cheated" by creating a fixed transmit ring for each NIC and just pointing the NIC to the packets to be sent. He did demonstrate that the architecture of a typical x86-based server is NOT a performance bottleneck though.{{</note>}}

* In the meantime we did several Software Gone Wild episodes with people pushing the performance envelope of software-based forwarding, including [IPv4-over-IPv6 tunnel headend delivering 20 Gbps per x86 core](/2016/03/x86-based-switching-at-ludicrous-speed.html)... in March 2016.

I stopped tracking how far they got in the meantime, it was pretty obvious that _we need hardware switching in NICs_ argument was already bogus at that point, and if you want slightly more recent performance figures, check out the [fd.io VPP performance tests](https://docs.fd.io/csit/rls1701/report/vpp_performance_tests/) and Andree Toonk's blog posts on high-performance packet forwarding with [VPP](https://blog.apnic.net/2020/04/17/kernel-bypass-networking-with-fd-io-and-vpp/) and [XDP](https://blog.apnic.net/2020/04/30/how-to-build-an-xdp-based-bgp-peering-router/).

**TL&DR**: Just because you can't figure out how to do it doesn't mean it can't be done. Do some more research...

So where do we really need smart NICs? There are (large) niche use cases like [support for baremetal servers in public clouds](/2020/06/cloud-networking-architectures.html) or preprocessing stock quotes in High Frequency Trading (HFT) environments. NetApp is also using Pensando NIC as a generic offload engine, but in that case it just happens that the offload hardware also has an Ethernet port (for a minimal amount of additional details please check the [Pensando presentations from CFD7](https://techfieldday.com/appearance/pensando-presents-at-cloud-field-day-7/)). Anything else from real-life production as opposed to [conference-talk-generating](/2019/05/bathwater-and-hyperscalers.html) [proof-of-concept](/2018/05/the-difference-between-hodgepodge-poc.html)? Please let me know!