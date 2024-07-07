---
date: 2021-10-21 06:48:00+00:00
dcbgp_tag: relevant
high-availability_tag: fail
series:
- dcbgp
tags:
- design
- BGP
- high availability
- virtualization
title: Circular Dependencies Considered Harmful
---
A while ago, my friend Nicola Modena sent me another intriguing curveball:

> Imagine a CTO who has invested millions in a super-secure data center and wants to consolidate all compute workloads. If you were asked to run a BGP Route Reflector as a VM in that environment, and would like to bring OSPF or ISIS to that box to enable BGP ORR, would you use a GRE tunnel to avoid a dedicated VLAN or boring other hosts with routing protocol hello messages?

While there might be good reasons for doing that, my first knee-jerk reaction was:
<!--more-->
> You are making that VM a crucial part of your transport infrastructure. There are some security implications right there. You might want to run it on a dedicated management cluster (like vCenter), in which case adding that extra VLAN to those two ToR switches and running OSPF/IS-IS on them doesn’t sound too bad.

There's an even more important fallacy in this line of thinking. You're making your core transport infrastructure dependent on:

* A data center,
* A data center fabric, 
* A controller managing that data center fabric (if you bought into the SDN religion),
* A virtualization environment, 
* A virtualization management/orchestration system,
* One or more virtual machines that you cannot reach with a console cable.

You need a running network to get to most of these components, resulting in a nightmare circular dependency -- once you lose that VM, it will be very hard to get it back.

Seasoned networking architects have been aware of the dangers of circular dependencies way before the *centralized controller* SDN hype started, and virtualization vendors like VMware were always very careful to have at least some semblance of an independent control plane on hypervisor hosts to be able to restart the management system from the outside[^CD-1000v]. Networking vendors have no such reservations -- looking at some slide decks, it seems perfectly fine to run a network control plane on infrastructure with heavy circular dependencies on the network itself (not to mention DNS or NTP)[^CD-Rule4].

[^CD-1000v]: Cisco Nexus 1000v architects learned that lesson the hard way -- after the 1000v control plane VM failure, the ESXi hosts would get (permanently) disconnected from the network because they ran LACP from the control plane.

[^CD-Rule4]: Proving (yet again) RFC 1925 rules 4 and 5
 
Think something like that can never happen, or that you could build enough resiliency into your design to survive any possible failure? Look no further than the October 2021 Facebook outage that [disconnected Facebook from the Internet](https://blog.cloudflare.com/october-2021-facebook-outage/).

According to the [official outage report](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/):

> To ensure reliable operation, our DNS servers disable those BGP advertisements if they themselves can not speak to our data centers, since this is an indication of an unhealthy network connection. In the recent outage the entire backbone was removed from operation,  making these locations declare themselves unhealthy and withdraw those BGP advertisements. The end result was that our DNS servers became unreachable even though they were still operational. This made it impossible for the rest of the internet to find our servers. 

It seems (from the outside) like they had a circular dependency between DNS and BGP ([here's why](https://news.ycombinator.com/item?id=28764214)), and never experienced a (real or simulated) failure that would expose that dependency.

In the meantime, there were [reports on Twitter](https://arstechnica.com/information-technology/2021/10/facebook-instagram-whatsapp-and-oculus-are-down-heres-what-we-know/) that Facebook employees couldn't enter buildings (doors not being able to reach authentication servers), and [couldn't use third-party services](https://www.theverge.com/2021/10/4/22709575/facebook-outage-instagram-whatsapp) like Google Docs or Zoom because those required Facebook authentication.

Based on how long it took them to get to the affected routers, it looks like their out-of-band network was useless (OOB access servers relying on RADIUS servers?). After the outage was over, [there were claims](https://twitter.com/cullend/status/1445156376934862848) the final tool needed to get to the bricked router(s) was an angle grinder  ([same source](https://twitter.com/cullend/status/1445157085591871489): *none of the doors have keyholes so what happens if that system goes down?*)

Every large enough system is full of circular dependencies (someone should make a law out of that). Kripa Krishnan (Google) mentioned a few they discovered during Disaster Recovery Testing in a (must read) [ACM Queue Article](https://queue.acm.org/detail.cfm?id=2371516):

* Failovers failed because the alternate location was unavailable;
* Lack of authentication servers locked out the workstations;
* The configuration server for the alerting and paging system went offline, making it impossible to redirect alerts to other locations.

Couldn't we avoid the dependencies? Of course, we could if someone could visualize the whole picture[^1], but that tends to be impossible in large enough systems. Another root cause might be the stability of the infrastructure[^2] -- when infrastructure is stable enough, its users take it as a given (see also: [first fallacy of distributed computing](https://my.ipspace.net/bin/get/Net101/F2.1%20-%20Network%20Is%20%28Not%29%20Reliable.mp4?doccode=Net101)).

What else could we do? Test, test, test. Trigger real failures ([don't fake them](/2019/09/disaster-recovery-test-faking-another/)), learn from them, and fix stuff. [All the big players do that](https://queue.acm.org/detail.cfm?id=2371297); maybe it's time for you to start as well.

[^1]: This is a perfect time to mention AI/ML as the fix to all problems.

[^2]: Does it look like I'm saying it's Ops fault for being too good? Get used to it -- it's always the Ops fault, and within the infrastructure, it's always the network. Within the network? DNS, of course... unless it's BGP.
