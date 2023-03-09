---
date: 2020-02-20 07:35:00+01:00
ha-cloud_tag: stretch
high-availability_tag: cloud
series:
- ha-cloud
tags:
- vMotion
- cloud
- AWS
- high availability
title: Live vMotion into VMware-on-AWS Cloud
url: /2020/02/live-vmotion-into-vmware-on-aws-cloud.html
---
Considering VMware's [enrapturement with vMotion](https://blog.ipspace.net/2014/09/vmotion-enhancements-in-vsphere.html) the following news ([reported by Salman Naqvi in a comment to my blog post](https://blog.ipspace.net/2020/01/youre-responsible-for-resiliency-of.html?showComment=1580417029396#c5624129873759076242)) was clearly inevitable:

> I was surprised to learn that [LIVE vMotion is supported between on-premise and Vmware on AWS Cloud](https://cloud.vmware.com/vmc-aws/faq#workload-migration)

What's more interesting is *how did they manage to do it?*
<!--more-->
A few basics first:

-   VMware-on-AWS has little to do with AWS or public cloud. It's a vSphere/NSX-T/VSAN cluster managed by VMware and running on AWS bare-metal servers. The only difference between VMware-on-AWS and a vSphere cluster running in any collocation facility is that they had to cope with the fact that [AWS doesn't care about layer-2 tricks](https://blog.ipspace.net/2020/01/there-is-no-layer-2-in-public-cloud.html).
-   VMware-on-AWS runs NSX-T, so the question really becomes "*how do you do a vMotion between two NSX-T instances or between a traditional vSphere cluster and an NSX-T instance?*"

Since VMware introduced cross-vCenter vMotion, it's easy to migrate a running virtual machine across multiple vCenter deployments... all you need is a matching port group name on both ends, and end-to-end layer-2 connectivity if you expect the virtual machine to keep communicating with its environment.

The "magic" of live vMotion to VMware-on-AWS thus boils down to "*how do I get layer-2 connectivity into AWS?*". Well, you don't - AWS is not stupid enough to allow you to bring your flooding challenges into their environment... but there's always [the duct-tape-of-networking](https://blog.ipspace.net/2010/12/where-would-you-need-gre.html).

NSX-T includes L2VPN - bridging across an IPsec-protected GRE tunnel. Hooray, problem solved. You might experience MTU issues I was told (and that's probably why they want you to have a DirectConnect link into AWS), but who cares about such minor inconveniences when you can do what everyone always wanted: move a running server into AWS.

You probably know my opinion on the feasibility of [long-distance vMotion](https://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html), long-distance bridging and L2 DCI, and the latest VMware's trick didn't change it a bit. If anything, the L2 DCI features they're offering in NSX-T release 2.5 are worse than what Cisco had in OTV a decade ago

{{<note>}}
I'm not saying that you should do L2 DCI or endorsing OTV, but if you absolutely want to do crazy things, at least do them right.
{{</note>}}

**Long story short**: the only advice I can give you regarding this marketing gimmick is what [James Mickens told people enchanted with the promise of ML/AL](https://blog.ipspace.net/2018/10/worth-watching-machine-learning-in.html):

-   In three words: Think before deploying.
-   In two words: Think first.
-   In one word: Don't.

On the other hand, if you want to know how stuff works behind the scenes check out:

-   [VMware NSX technical deep dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)
-   [AWS networking](https://www.ipspace.net/Amazon_Web_Services_Networking)
-   [vSphere 6 networking deep dive](https://www.ipspace.net/VSphere_6_Networking_Deep_Dive)
