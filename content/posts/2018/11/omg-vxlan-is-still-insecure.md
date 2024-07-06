---
date: 2018-11-27 09:01:00+01:00
tags:
- VXLAN
- security
- NSX
title: OMG, VXLAN Is Still Insecure
url: /2018/11/omg-vxlan-is-still-insecure.html
---
A friend of mine told me about a "[VXLAN is insecure, the sky is falling](https://ripe77.ripe.net/presentations/32-vxlan-ripe77.pdf)" presentation from RIPE-77 which claims that you can (under certain circumstances) inject packets into VXLAN virtual networks from the Internet.

Welcome back, Captain Obvious. Anyone looking at the VXLAN packet could immediately figure out that **there's no security in VXLAN**. I pointed that out several times in my [blog posts](/2015/04/omg-vxlan-encapsulation-has-no-security.html) and presentations, including [Cloud Computing Networking](https://my.ipspace.net/bin/get/CloudNet/Cloud%20Computing%20Networking%20(EuroNOG).pdf) (EuroNOG, September 2011) and [NSX Architecture](https://my.ipspace.net/bin/list?id=NSXArch) webinar (August 2013).
<!--more-->
Another conclusion I made in NSX Architecture webinar (slide 28, included below) was "**transport network MUST be secure**" (notice the RFC2119 use of MUST).

{{<figure src="/2018/11/s1600-VXLAN+Security.jpg">}}

I would also like to point out that VXLAN is no different from most other layer-heaping technologies including GRE, L2TP, and MPLS, or earlier virtual circuit technologies like Frame Relay and ATM. The moment an intruder gains access to the transit network it's game over... but of course it's so much more fun to make the same point with examples like "I can insert UDP packets into a VXLAN network".

Well, the presenter should have gone a step further: in VXLAN networks that use dynamic MAC learning instead of a decent control plane, the VTEPs would blindly accept whatever is injected from the outside, **and create forwarding entries** that would ensure the return traffic gets back to the intruder.

Does that mean VXLAN is broken? Not really, any technology can be dangerous in hands of clueless incompetents... including Kinder Surprise Eggs (there must be a reason [they are banned in some countries](https://en.wikipedia.org/wiki/Kinder_Surprise#United_States)). At least in the VXLAN case, the drawbacks are clearly documented in the [Security Considerations section of RFC 7348](https://datatracker.ietf.org/doc/html/rfc7348#section-7):

> Traditionally, Layer 2 networks can only be attacked from 'within' by rogue end points -- either by having inappropriate access to a LAN and snooping on traffic, by injecting spoofed packets to 'take over' another MAC address, or by flooding and causing denial of service. A MAC-over-IP mechanism for delivering Layer 2 traffic significantly extends this attack surface. This can happen by rogues injecting themselves into the network by subscribing to one or more multicast groups that carry broadcast traffic for VXLAN segments and also by sourcing MAC-over-UDP frames into the transport network to inject spurious traffic, possibly to hijack MAC addresses.

As always, whenever you want to start using a new tool, you should [understand how it works, and what its advantages and limitations are](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S4A)... after all, you want to [call yourself an engineer](/2018/01/how-to-become-better-networking-engineer.html), right? Oh, and don't be surprised when the \$vendors don't tell you what the limitations and drawbacks are.

Finally, I would love to see security researchers shift their focus from "*OMG, look how I managed to break it*" to "*there are some fundamental limitations of what can be done, and if you don't know what they are you might get hurt... like in this example."*

And just in case you want to know more -- you'll find tons of details in VXLAN details in _[VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive)_ and _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_.

### Revision History

2022-02-22
: Added a quote from RFC 7348
