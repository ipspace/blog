---
date: 2020-02-26 08:29:00+01:00
high-availability_tag: cloud
tags:
- design
- data center
- cloud
- high availability
title: The Myth of Scaling From On-Premises Data Center into a Public Cloud
url: /2020/02/the-myth-of-scaling-from-on-premises.html
---
Every now and then someone tries to justify the "wisdom" of [migrating VMs from on-premises data center into a public cloud](https://blog.ipspace.net/2020/02/live-vmotion-into-vmware-on-aws-cloud.html) (without renumbering them) with the idea of "scaling out into the public cloud" aka "cloud bursting". My usual response: this is another vendor marketing myth that [works only in PowerPoint](https://blog.ipspace.net/2011/09/long-distance-irf-fabric-works-best-in.html).

To be honest, that statement is too harsh. You can easily scale your application into a public cloud assuming that:
<!--more-->
-   You have a scale-out architecture with eventually-consistent database at the bottom;
-   You have already learned how to deploy independent *swimlanes* (totally uncoupled application stacks), how to synchronize data between them, and how to handle inevitable conflicts;
-   You are already replicating data into a public cloud (for example for backup purposes).

Turning the replicated data that already reside in a public cloud into yet another swimlane is a piece of cake (assuming you also figured out infrastructure-as-code-based deployments). Add another entry to your DNS-based load balancing and you're done.

{{<note info>}}
You'll find more information on the above concepts in [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar and the fantastic [Scalability Rules](https://www.amazon.com/gp/product/013443160X/ref=as_li_tl) book.
{{</note>}}

However, that's not what the enterprise-focused \$vendor evangelists have in mind. Here's a typical explanation, [courtesy of Piotr Jablonski](https://blog.ipspace.net/2020/02/live-vmotion-into-vmware-on-aws-cloud.html?showComment=1582215526577#c6431086606253857338):

> What about a use case for development/staging where the company want to test a new app on 10 servers and they have 2 on-prem and they don't need to wait for new hardware? They can run 8 servers or more in the cloud. For a production use case, if workloads are contained, then scaling-out a particular app layer is a viable option. Do you think a VPN/interconnect/DCI kills benefits of the scale-out?

I have just one word for that idea: **latency**.

Here's a longer explanation I gave in the [Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.

Assume you have a typical multi-layer application stack consisting of a web server, an application server, a database server, and a storage array (and don't get me started on what happens when you decide to replace that with microservices ;).

{{<figure src="/2020/02/s400-AA-App-Stack.jpg" caption="Typical application stack">}}

Now imagine that layer X has to make N requests to layer X-1 to satisfy a request coming from the client. In a typical scenario the number of requests increase down the stack (more so if the developers never mastered the dark art of SQL JOIN statement) - supposedly over 90% of the traffic stays within large data centers.

The number of requests made between layers of an application stack typically doesn't matter if the underlying server is fast enough, and if the latency is negligible (end-to-end latency in a data center is measured in microseconds)... but what happens if you increase the latency between parts of your application stack?

To illustrate that, let's draw boxes between individual layers of an application stack, with the width of the box indicating the number of requests, and the height of the box indicating latency. The area of the box is then the total time a component of an application stack has to wait for data while processing a client request. That time is usually directly added to whatever usual response time your application has, as most applications haven't been written with asynchronous processing and/or multithreading in mind.

{{<figure src="/2020/02/s640-AA-Stack-Requests.jpg" caption="Latency added to the application stack">}}

Now imagine you increase latency between application stack components. Some of the boxes grow ridiculously large.

{{<figure src="/2020/02/s640-AA-Stack-Latency.jpg" caption="The effects of increased latency between application stack components">}}

{{<note>}}The boxes are obviously not to scale.{{</note>}}

Of course you might argue that having an application with 10- or 100-second response time (instead of the usual 100 msec one) is useful. YMMV, but please don't waste everyone else's time.

**To recap**: cloudbursting should stay in PowerPoint.

Finally, what could you do if your organization got infected by this particular strain of stupidity? If your applications run on Linux add artificial latency (at least one RTT worth of it) using **tc** to the components that should be moved into the public cloud, lean back and enjoy the results. Need even more cloud marketing antidote? You might get it in our [Networking in Public Cloud Deployments online course](https://www.ipspace.net/PubCloud/).

{{<note>}}
If you detest **tc** CLI as much as I do, read the [great article by Andre Toonk explaining how to add artificial latency on a Linux box](https://medium.com/@atoonk/tcp-bbr-exploring-tcp-congestion-control-84c9c11dc3a9), or you might prefer the [Comcast CLI](https://github.com/tylertreat/comcast) (name chosen by the author for some unfathomable reasons).
{{</note>}}
