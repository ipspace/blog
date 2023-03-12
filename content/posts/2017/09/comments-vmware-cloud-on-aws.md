---
date: 2017-09-07 11:56:00+02:00
ha-cloud_tag: stretch
series:
- ha-cloud
tags:
- cloud
- AWS
- virtualization
title: 'Rant: VMware Cloud on AWS Marketing and Reality'
url: /2017/09/comments-vmware-cloud-on-aws.html
---
VMware started talking about VMware Cloud on AWS a while ago, and my first response was "*yeah, it's just vCloud Air but they wanted to get rid of CapEx, so it's running on someone else's servers*"

Last week Frank Denneman published a [technical overview of the solution](http://frankdenneman.nl/2017/08/29/vmware-cloud-aws-technical-overview/) and I was mostly correct.
<!--more-->
> VMware Cloud on AWS is a service and that means that we will not using product versions when we refer to the service. 

Meaning: we want to charge you perpetually (and we also have to pay Amazon's infrastructure, so there you have it).

> VMware Cloud on AWS is operated by VMware. \[and later\] Host failures remediation is the responsibility of VMware. If a host fails permanently, VMware replaces this ESXi host without user intervention. 

Here's the only significant operational difference I can see between VMware Cloud on AWS and yourself doing the same thing in your data center or with Amazon's *dedicated host* instances. Licensing (CapEx) versus service (OpEx) is obviously another one.

> At initial availability, the VMware Cloud on AWS base cluster configuration contains four hosts.

This looks like they won't give you vCloud Air account where you could consume resources on demand, but a fixed-size private cloud implementation running on AWS infrastructure.

> At initial availability, the Cloud SDDC is restricted to a single AWS region and availability zone (AZ).

So much for reliability. It's a nice proof-of-concept, but environments that actually care about availability would have to wait.

> In future VMware Cloud on AWS releases, through the partnership of VMware and AWS, multi-AZ availability will be possible for the first time ever, by stretching the cluster across two AZs in the same region.

Makes perfect sense. Let's link two availability zones (failure domains) with a layer-2 extension (what you need if you want to stretch a cluster) and [making them into one](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html). Hooray!

> With this groundbreaking offering, refactoring of traditional applications will no longer be required to obtain high availability on the AWS infrastructure. 

Awesome! More unicorn dust and flat-earth magic. This is **not** how you get higher availability, but some vendors [never stop peddling their warez](https://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html). Time to reuse a picture from [another blog post](http://blog.ipspace.net/2015/11/stretched-firewalls-across-layer-3-dci.html).

![](/2017/09/s500-Triple-facepalm.jpg)

However, that section of Frank's blog post described VSAN synchronous replication. Apart from "no need to refactor" that wasn't too bad. However, wait till we get to networking:

> At initial availability, users connect to VMware Cloud on AWS via a layer 3 VPN connection.

So far so good. This is how AWS works today and it makes perfect sense.

> Future releases of VMware Cloud on AWS, however, will support AWS Direct Connect and allow **cross-cloud vSphere vMotion operations**.

\*\*\*\* NO! This is the \*\*\*\* that only ever works in PowerPoint and carefully scripted demos. Time for another picture from that same blog post.

![](/2017/09/s500-Enough+of+this+shit.jpg)

Long story short: while I see plenty of use cases for VMware SDDC on AWS (assuming the pricing is not extravagant) there are no silver bullets. If you want true high availability, you have to design it at the application layer.
