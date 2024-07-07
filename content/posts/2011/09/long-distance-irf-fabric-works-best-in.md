---
date: 2011-09-12 06:39:00+02:00
high-availability_tag: ignore
ha-cluster_tag: overview
series:
- ha-cluster
tags:
- switching
- data center
- workshop
- WAN
- high availability
title: 'Long-distance IRF Fabric: Works Best in PowerPoint'
url: /2011/09/long-distance-irf-fabric-works-best-in/
---
HP has commissioned an [IRF network test](https://web.archive.org/web/20170806120331/http://www3.networktest.com/hpirf/hpirf1.pdf) that came to absolutely astonishing conclusions: vMotion runs almost twice as fast across two links bundled in a port channel than across a single link (with the other one being blocked by STP). The test report contains one other gem, this one a result of incredible creativity of HP marketing:

> For disaster recovery, switches within an IRF domain can be deployed across multiple data centers. According to HP, a single IRF domain can link switches up to 70 kilometers (43.5 miles) apart.

You know my [opinions about stretched cluster](/2011/06/stretched-clusters-almost-as-good-as/)... and the more down-to-earth part of HP Networking (the people writing the documentation) agrees with me.
<!--more-->
{{<note>}}Please note: this post is not a critique of IRF fabric technology or its implementation, just of a particularly \"creative\" use case.{{</note>}}

Let's assume someone is actually brave enough to deploy a network using the design shown in the following figure with switches in two data centers merged into an IRF fabric (according to my Twitter friends this design was [occasionally promoted by some HP-certified instructors](http://twitter.com/singlekorn/status/81069716852056065)):

{{<figure src="/2011/09/s320-IRF_DC_Stupid.png" caption="Stretched IRF fabric design">}}

The [IRF documentation for the A7500 switches](http://bizsupport1.austin.hp.com/bc/docs/support/SupportManual/c02985993/c02985993.pdf) ([published in August 2011](http://h20000.www2.hp.com/bizsupport/TechSupport/DocumentIndex.jsp?contentType=SupportManual&lang=en&cc=us&docIndexId=64179&taskId=101&prodTypeId=12883&prodSeriesId=4177519))[^NLOL] contains the following facts about IRF partitions (split IRF fabric) and Multi-Active Detection (MAD) collisions (more commonly known as *split brain* problems):

[^NLOL]: HP managed to break all links to their product documentation links I had in this blog post. I have better things to do than chasing them across Internet Archive; I left the links intact in case you want to do that.

> The partitioned IRF fabrics operate with the same IP address and cause routing and forwarding problems on the network.

No surprise there, we always knew that split subnets cause interesting side effects, but it's nice to see it acknowledged.

It\'s interesting to note, though, that pure L2 solution might actually work \... but the split subnets would eventually raise their ugly heads in adjacent L3 devices.

> During an IRF merge, the switches of the IRF fabric that fails the master election must reboot to re-join the IRF fabric that wins the election.

Hold on -- I lose the inter-DC link(s), reestablish them, and then half of the switches reboot. Not a good idea.

Let's assume the above design is "extended" with another bright idea -- to detect split brain scenarios, the two switches run BFD over an alternate path (could be the Internet) to detect split brain events. According to the manual:

> An IRF link failure causes an IRF fabric to divide into two IRF fabrics and multi-active collision occurs. When the system detects the collision, it holds a role election between the two collided IRF fabrics. The IRF fabric whose master's member ID is smaller prevails and operates normally. The state of the other IRF fabric transitions to the recovery state and temporarily cannot forward data packets.

Isn't that great -- not only have you lost the inter-DC link, you've lost one of the core switches as well.

**Summary**: As always, just because you can doesn't mean you should \... and remember to be wary when consultants and marketing people peddle ideas that seem too good to be true.

### What Are the Alternatives?

As I've explained in the [Data Center Interconnects](https://www.ipspace.net/DCI) webinar (available as [recording](https://www.ipspace.net/Recordings?code=DCI) or part of the [yearly subscription](https://www.ipspace.net/Subscription) or [Data Center Trilogy](https://www.ipspace.net/Data_Center_trilogy)), there are at least two sensible alternatives if you really want to implement layer-2 DCI and have multiple parallel layer-1 links (otherwise IRF wouldn't work either)

**Bundle multiple links in a port channel between two switches.** If you're not concerned about device redundancy (remember: you can merge no more than two high-end switches in an IRF fabric), use port channel between the two DCI switches.

{{<figure src="/2011/09/s320-IRF_DC_PC.png" caption="DCI link implemented with LAG bundle">}}

**Use IRF (or any other MLAG solution) within the data center** and establish a port channel between two IRF (or VSS or vPC) clusters. This design results in full redundancy without unexpected reloads or other interesting side effects (apart from the facts that Earth curvature didn\'t go away, Earth still orbits the Sun and not vice versa, and split subnets still don't work).

{{<figure src="/2011/09/s320-IRF_DC_Full.png"  caption="DCI link implemented as an MLAG bundle">}}
