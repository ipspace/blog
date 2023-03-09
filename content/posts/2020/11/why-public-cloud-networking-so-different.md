---
date: 2020-11-23 07:00:00+00:00
ha-cloud_tag: design
series_weight: 1000
series:
- ha-cloud
tags:
- cloud
- IP routing
- AWS
- Azure
title: Why Is Public Cloud Networking So Different?
---
A while ago (eons before AWS introduced Gateway Load Balancer) I discussed the intricacies of [AWS](https://blog.ipspace.net/2020/05/aws-networking-101.html) and [Azure](https://blog.ipspace.net/2020/05/azure-networking-101.html) networking with a very smart engineer working for a security appliance vendor, and he said something along the lines of "_it shows these things were designed by software developers -- they have no idea how networks should work._" 

In reality, at least some aspects of public cloud networking come closer to the original ideas of how [IP and data-link layers should fit together](https://blog.ipspace.net/2015/05/reinventing-clns-with-l3-only-forwarding.html) than today's [flat earth theories](https://blog.ipspace.net/2020/04/stupidity-stretched-vlan.html), so he probably wanted to say "_they make it so hard for me to insert my virtual appliance into their network._"
<!--more-->
Regardless of personal perspectives, networking in public clouds looks like it was designed in a universe with a different set of laws of physics, so it's natural to wonder "_why, oh why did they have to do that unto me?_" and couldn't just follow the "_we've always done things this way_" trail blazed by the networking vendors.

I can see at least three reasons the hyperscale public cloud providers had to go back to the first principles and design virtual networking that works well (as opposed to [emulate the thick yellow cable](https://blog.ipspace.net/2015/02/lets-get-rid-of-thick-yellow-cable.html)).

### Business Drivers

The only way for "premium" networking vendors to sell you more high-priced boxes is to heap more and more complexity into their networking implementation, [supposedly to satisfy customers' business needs](https://blog.ipspace.net/2020/09/business-needs-excuses.html). In reality they often focus on box sales, not long-term customer satisfaction. Stock price tracks quarterly earning reports, not long-term customer retention, and so the [next-generation unicorn dust](https://blog.ipspace.net/2020/02/be-careful-when-using-new-features.html) has to work just long enough for the customer to generate a P/O.

Cloud providers have to focus on running a stable infrastructure that just works. Their earning reports depend on making profits on service revenues, and as those revenues depend on actual amount of services used, they better get their stuff together.

### Admitting Failures

Networking vendors are rarely exposed to public scorn when their products fail. When people couldn't board United flights, nobody blamed the configuration intricacies of the routers running the network... and [when a hospital is down for days due to spanning tree problems](https://www.computerworld.com/article/2581420/all-systems-down.html), the consultants who sold them that design, or vendors who were only too happy to implement it, are rarely mentioned.

{{<note>}}Please note I'm blaming the industry-wide mindset, not the individuals working for said vendors. I know hundreds of excellent highly motivated networking engineers who work really hard to make the ever-more-complex stuff work. I admire their efforts and dedication, but it doesn't change the fact that their employers make them solve the wrong problem.{{</note>}}

Compare that to public clouds: the buck stops there. If AWS is down, everyone knows whose fault it is... and with usage-based charging it's in public cloud providers' best interest to keep things stable and running.

### Scale

Our daily challenges are minuscule compared to what's going on in some public clouds. We're discussing whether you really need BGP to build a 200-node fabric. VMware could never get beyond ~1000 hypervisor hosts in a single management domain. Some public cloud providers run [tens- if not hundreds of thousands of servers](https://www.lastweekinaws.com/blog/why-aws-announces-regions-in-advance/) under a single orchestration system in a single availability zone within a region.

Smart people realized it's extremely hard to run large-scale systems years ago. Straight from RFC 3439, section 2.2:

> In particular, the largest networks exhibit, both in theory and in practice, architecture, design, and engineering non-linearities which are not exhibited at smaller scale.  

And later in section 2.2.1:

> In many large networks, even small things can and do cause huge events. In system-theoretic terms, in large systems such as these, even small perturbations on the input to a process can destabilize the system's output.

In layman words, "_we don't have time for the [**** people use to push the problems down the stack](https://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html)._"

**Long story short**: If you want to know how to build networks that work well within the confines of having Ethernet adapters on every server, and using IPv4 or IPv6 connectivity, study the network services from public cloud providers. There's a reason they don't provide (among other things) continent-spanning layer-2 domains, or VLANs stretching into your data center. 
