---
date: 2020-03-05 08:04:00+01:00
mlag_tag: design
series:
- mlag
tags:
- design
- bridging
- VXLAN
- data center
- fabric
title: Should I Go with VXLAN or MLAG with STP?
url: /2020/03/should-i-go-with-vxlan-or-mlag-with-stp.html
---
**TL&DR**: It's 2020, and VXLAN with EVPN is all the rage. Thank you, you can stop reading.

On a more serious note, I got this questions from an [Johannes Spanier](https://www.linkedin.com/in/johannes-spanier/) after he read my *[do we need complex data center switches for NSX underlay](/2020/02/do-we-need-complex-data-center-switches.html)* blog post:

> Would you agree that for smaller NSX designs (\~100 hypervisors) a much simpler Layer2 based access-distribution design with MLAGs is feasible? One would have two distribution switches and redundant access switches MLAGed together.

I would still prefer VXLAN for a number of reasons:
<!--more-->
-   **No dependency on MLAG** (assuming you get the edge design right). MLAG (or any other technology that makes two devices pretend they're a single device through convoluted state sharing) is a brittle kludge. I've seen several data center meltdowns caused by MLAG bugs, and haven't heard of one caused by an IP forwarding bug for a very long time.
-   [I wouldn't run a bridging-only fabric without STP](/2014/08/stp-and-expert-beginners.html). STP is the only protection you have against stupidities like cable errors or [technicians testing cables by plugging TX and RX ports together](/2012/04/stp-loops-strike-again.html) (although modern connectors make that less likely). Unfortunately, **STP is way worse than MLAG**.
-   I prefer having a "*we know what we're doing*" behavior in my backbone instead of "*[**we haven't heard anything so it must be OK to forward**](/2014/07/is-stp-really-evil.html)*".
-   Call me old-fashioned but I **prefer routing over bridging** in my transport infrastructure.
-   Finally, even though my friends at Avaya (now Extreme) tell me how well SPB works (and I believe them), I still prefer **running a protocol that has been around for decades** (like OSPF or IS-IS for IPv4/IPv6) hoping someone else already hit all the major bugs.

> Alternatively, to put my question into another perspective: For "small" designs is there any problem leaf-spine VXLAN EVPN solves that STP free distribution/access cannot?

Robustness, stability, standard-based, multi-vendor (not that [I would focus on this one](/2020/02/pragmatic-evpn-designs.html))... pick one (or a few). Also note that you don't have to run EVPN, VXLAN on top of simple IP network is good enough.

If your data center design follows the traditional *every VLAN on every leaf switch* approach (lovingly known as "[let's turn our data center into a thick yellow cable](/2015/04/what-is-layer-2-and-why-do-we-need-it.html)"), you'll be equally well off having a static VXLAN flood list containing every ToR switch in your fabric. Obviously I'd hope you'd automate the generation of that flood list, but with four to six switches (all you need for \~100 hypervisors) you just might get by configuring it manually.

And now for the ubiquitous list of where you could find way more details. You could go for our [data center course](https://www.ipspace.net/Building_Next-Generation_Data_Center) (available with [Expert Subscription](https://www.ipspace.net/Subscription/Individual)) or these webinars (available with [Standard Subscription](https://www.ipspace.net/Subscription/Individual)):

-   [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures);
-   [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive);
-   [VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive);
-   [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics);
-   [Designing Private Cloud Infrastructure](https://www.ipspace.net/Designing_Private_Cloud_Infrastructure)
