---
date: 2019-12-05 08:42:00+01:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- design
- data center
- cloud
- WAN
- high availability
title: Disaster Recovery and Failure Domains
url: /2019/12/disaster-recover-and-failure-domains.html
---
One of the responses to my *[Disaster Recovery Faking](/2019/09/disaster-recovery-test-faking-another.html)* blog post focused on failure domains:

> What is the difference between supporting L2 stretched between two pods in your DC (which everyone does for seamless vMotion), and having a 30ms link between these two pods because they happen to be in different buildings?

I hope you agree that a [single broadcast domain is a single failure domain](/2012/05/layer-2-network-is-single-failure.html). If not, let agree to disagree and move on - my life is too short to argue about obvious stuff.
<!--more-->
Having a VLAN stretched across multiple pods destroys the idea of having pods in the first place (unless you need them for physical structure and/or scaling reasons) - you merged two potential availability zones into one.

Doing the same across multiple data centers has the same effect: you [destroyed all the benefits of large investments you made when building a second site](/2013/01/long-distance-vmotion-stretched-ha.html), unless you use the second site solely as a cold/warm backup for the primary site. I don't know many organizations where CIO or bean counters would agree to that approach.

There's also a minor technical detail: WAN links fail more often than data center infrastructure (see also: [fiber finder in its natural habitat](https://twitter.com/lightingguy32/status/1131189271828860928)). Stretching a VLAN across two data centers to build an active-active architecture [introduces a weak link and effectively reduces the availability of that architecture](/2019/11/stretched-vlans-and-failing-firewall.html).

Fortunately, you can't (easily) do the same mistake if you use a public cloud as your backup site - most public cloud providers are sane enough to work exclusively on layer-3 and offer direct L3 (routed) links or IPsec-based VPN connectivity as the only means of building hybrid clouds (even when the [whole thing looks like stretched VLANs to untrained eyes](/2019/11/stretched-layer-2-subnets-in-azure.html)). Not at least surprisingly, some enterprise networking- or virtualization vendors offer all sorts of crazy schemes on top of IP transport to stretch the VLANs to places they don't belong to.

### More Information

-   You might want to watch [Building Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar;
-   We covered hybrid cloud connectivity details in [AWS](https://my.ipspace.net/bin/list?id=AWSNET#EXTERNAL) and [Azure](https://my.ipspace.net/bin/list?id=AzureNet#EXTERNAL);
-   For even more public cloud goodness, register for the [Networking in Public Cloud Deployments](https://www.ipspace.net/PubCloud/) online course.
