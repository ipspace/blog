---
date: 2015-12-02 10:34:00+01:00
tags:
- switching
- OpenFlow
- performance
title: Is Flow-Based Forwarding Just Marketing Fluff?
url: /2015/12/is-flow-based-forwarding-just-marketing/
---
When writing the [Packet- and Flow-Based Forwarding blog post](/2015/11/packet-and-flow-based-forwarding/), I tried to find a good definition of flow-based forwarding (and I was [not the only one being confused](/2015/11/packet-and-flow-based-forwarding/#c2863387231465052303)), and the one from [Junos SRX documentation](https://www.juniper.net/techpubs/software/junos-security/junos-security10.1/junos-security-admin-guide/packet-flow-based-fwd-section.html) is as good as anything else I found, so let's use it.

**TL&DR**: Flow-based forwarding is a valid technical concept. However, when mentioned together with OpenFlow, it's mostly marketing fluff.
<!--more-->
According to Junos SRX documentation ([here's](http://www.juniper.net/documentation/en_US/junos12.3x48/information-products/pathway-pages/security/security-processing-overview.html) a later, more detailed version), packet-by-packet (stateless) forwarding works like this for every single packet:

-   Receive a packet;
-   Pass packet through ingress ACL (and whatever other input policy you have);
-   Perform a forwarding lookup (L2, L3, PBR, whatever);
-   Pass packet through egress ACL (and other output policies).

{{<note warn>}}Junos documentation calls this process **packet-based forwarding** or **packet-based processing**, conveniently ignoring the fact that all statistical multiplexing technologies in use today work on packets, particularly when they're based on Ethernet or IP.{{</note>}}

Flow-based forwarding, on the other hand, is a **cache-based** forwarding mechanism that:

-   Performs packet forwarding for the first packet in a flow;
-   Caches the results (output interface, rewriting, logging, counting and QoS actions);
-   Performs cache lookup on subsequent packets of the same flow and applies cached results without evaluating the input and output path.

{{<note info>}}I over-simplified the process a bit. Cache lookup is performed on every input packet, and the cache misses are punted to the slower forwarding path.{{</note>}}

### Is OpenFlow Flow-Based Forwarding?

At this point it's worth mentioning that hardware OpenFlow devices from major vendors don't use flow-based forwarding as described above. They use the exact same forwarding hardware as they'd use with standalone network OS.

The only OpenFlow switch I've seen so far that actually used the orthodox (micro)flow-based forwarding was the [early implementation of Open vSwitch](/2013/04/open-vswitch-under-hood/), and they quickly dropped that idea and [implemented megaflows](/2014/02/flow-based-forwarding-doesnt-work-well/) due to [dismal performance](/2014/11/open-vswitch-performance-revisited/). Technically, megaflows-based forwarding is still doing flow-based forwarding, but with way coarser flows. I haven't looked into what they're doing these days with Bloom filters.

There might be other vendors out there doing true flow-based forwarding with hardware OpenFlow switches (please write a comment), and I'd dare to guess that the price of their hardware might be a bit higher than what you can get with traditional 10GE switches today.

### Back to Flow-Based Forwarding

Does the description of flow-based forwarding remind you of fast switching or Netflow-based switching (aka MLS)? It's exactly the same concept, and the old grunts know how well those mechanisms work. Every single cache-based scheme ever invented faces interesting challenges like:

-   [Cache thrashing](https://www.quora.com/What-is-cache-thrashing) when faced with packet sprays (or DoS attacks). Widespread port scans performed on early Internet quickly brought down fast switching caches in core routers (forcing Cisco to roll out CEF in a hurry);

The past experience with cache-based switching makes me really skeptical about reinvented cache-based wheels like LISP.

-   Edge cases that are not handled correctly in the caching code. Sometimes the cached results don't match exactly the results (and side effects) produced by the slow forwarding path. Just think about all the times you had to turn off fast switching in Cisco IOS to make a feature work;
-   Limited cache size in hardware-based solutions (be it x86 CPU or 10GE switch), which results in either cache thrashing, or excessive punting to slow path which also kills performance.

### Does It Make Sense?

Flow-based forwarding makes perfect sense when:

-   It's cheap enough to implement large flow caches that can easily cope with the maximum number of flows the device could reasonably have to handle;
-   The cost (in terms of hardware utilization or latency) of full pipeline processing significantly exceeds the cost of doing a cache lookup and applying the cached actions;
-   It's possible to protect the device using flow-based forwarding against cache exhaustion, either by using a very large cache size or by flow-setup policing (example: [TCP SYN cookies](https://en.wikipedia.org/wiki/SYN_cookies)).

Firewalls and load balancers are thus a perfect use case for flow-based forwarding. Using the same concepts in high-speed L2/L3 forwarding devices is asking for trouble and reassuringly-expensive hardware.
