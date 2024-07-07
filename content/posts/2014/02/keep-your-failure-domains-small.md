---
date: 2014-02-11 06:49:00+01:00
dr_tag: life
high-availability_tag: dr
series:
- dr
tags:
- bridging
- data center
- high availability
title: Keep Your Failure Domains Small
url: /2014/02/keep-your-failure-domains-small/
---
A week after the [disastrous sleet](/2014/02/disasters-and-recoveries-part-1/) that kicked whole regions of Slovenia off power grid the servicemen of the local power distribution company (working literally days and nights) managed to restore electricity to the closest town ... but it still might take days or even weeks before everyone gets it. One of the reasons: huge failure domains.
<!--more-->
The 10 KV power lines that bring electricity to the transformer near my house (luckily I have an underground cable) are hardwired together in a multidrop fashion that would have made SDLC oldtimers either immensely proud or scared to death (because they knew how much havoc a single misbehaving modem could wreak).

For those of you that never experienced the beauties of multidrop SDLC, here's how the power distribution works around my place:

![](/2014/02/s400-PowerGrid_Failure_Domain.png)

The crucial problem: there's no [disconnector](http://en.wikipedia.org/wiki/Disconnector) at the junctions, making the whole distribution tree a single failure domain. A single tree branch short-circuiting the wires at the remotest point could cut off hundreds of customers.

### Back to Bits and Bytes

Wondering what this blog post has to do with networking? You do remember that [every bridged network (aka layer-2 network) is also a single failure domain](/2012/05/layer-2-network-is-single-failure/), right? A [forwarding loop](/2012/04/stp-loops-strike-again/) might bring down the whole domain (which some people [enthusiastically extend across multiple data centers](/2011/06/stretched-clusters-almost-as-good-as/)).

### What Can We Do?

Here are a few things to keep in mind:

-   Keep your failure domains as small as possible. Terminate bridging as soon as possible;
-   Insert as much failure isolation as you can. [Overlay virtual networks](/2011/12/decouple-virtual-networking-from/) nicely isolate the single failure domain of a layer-2 virtual network from the robust layer-3 transport infrastructure;
-   Use technologies that reduce the size of a failure domain. [Layer-3 hypervisor switching](/2013/12/hyper-v-network-virtualization-packet/) eliminates layer-2 failure domains altogether (other failure domains like single cluster of managements systems are obviously still an issue);
-   Build a hierarchy of failure domains. Availability zones in your private cloud are the necessary first step.
-   Analyze the structure of mission-critical applications (covered in more details in the fantastic [Scalability Rules](http://www.amazon.com/gp/product/0321753887?ie=UTF8&camp=1789&creativeASIN=0321753887&linkCode=xm2&tag=cisioshinandt-20) book).

### More Information

Watch these [cloud computing](http://www.ipspace.net/Roadmap/Cloud_computing_webinars) webinars:

-   [Overlay virtual networking](http://www.ipspace.net/Overlay_Virtual_Networking);
-   [Cloud computing networking](http://www.ipspace.net/Cloud_Computing_Networking);
-   [Designing the infrastructure for a private cloud](http://www.ipspace.net/Designing_a_Private_Cloud).
