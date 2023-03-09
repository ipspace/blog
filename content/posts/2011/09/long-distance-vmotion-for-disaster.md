---
date: 2011-09-30 06:43:00+02:00
dr_tag: avoid
high-availability_tag: dr
series:
- dr
tags:
- data center
- vMotion
- high availability
title: Long-distance vMotion for Disaster Avoidance? Do the Math First
url: /2011/09/long-distance-vmotion-for-disaster.html
---
The proponents of inter-DC layer-2 connectivity (required by long-distance vMotion) inevitably cite *disaster avoidance* (along with buzzword-bingo-winning *business agility*) as one of the primary requirements after they figure out [stretched clusters might not be such a good idea](https://blog.ipspace.net/2011/06/stretched-clusters-almost-as-good-as.html) (and there's no way to explain [the dangers of split subnets](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html) to some people). When faced with the *disaster avoidance* "requirement", ask them to do some basic math first.
<!--more-->
{{<note update>}}This blog post was written in 2011. A decade later we have higher link speeds at lower cost, but also larger virtual machines. Do the math!{{</note>}}

However, before starting this third-grade math exercise, let's define *disaster avoidance*. The idea is simple: an [iRene](http://en.wikipedia.org/wiki/Hurricane_Irene_(2011)) is approaching, you know you'll have to shut down one of the data centers, and want to migrate the workload to another data center. Major obstacle: [maximum round-trip time supported by vMotion with vSphere 4.x is 5 ms](http://www.yellow-bricks.com/2009/09/21/long-distance-vmotion/) (some other documents cite 200 km), extended to [10 ms in vSphere 5.x](http://www.yellow-bricks.com/2011/08/03/vsphere-5-metro-vmotion/). Is that enough to bring you out of harm's way? It depends; you might want to check the disaster avoidance requirements against the distance limits first.

Now let's focus on the inter-DC bandwidth. To simplify the math, assume you have two 1Gbps links (that seems to be a common inter-DC link speed these days) between your data centers.

{{<note>}}If you have a single link and someone starts talking about disaster avoidance, tell them to buy the second link first.{{</note>}}

The inter-DC links are probably not empty (or your boss should be asking you some tough questions), so let's say we have 1Gbps of bandwidth available for disaster avoidance-induced vMotion. Assuming perfect link utilization, no protocol overhead, and no [repeat copies of dirty memory pages](http://blogs.vmware.com/uptime/2011/02/vmotion-whats-going-on-under-the-covers.html), you can move a GB of RAM in 8 seconds \... or completely saturate a 1Gbps link to vacate a physical server with 256 GB of RAM in just over half an hour \... or 2 hours for a single quarter-rack UCS chassis full of [B230 M1 blade servers](http://www.cisco.com/en/US/products/ps11206/index.html). Obviously the moved VMs will cause [long-distance traffic trombones](https://blog.ipspace.net/2010/09/long-distance-vmotion-and-traffic.html), further increasing the utilization of inter-DC link and reducing effective migration rate.

So, the next time someone drops by with a great disaster avoidance scheme, make sure you ask the following questions (after politely listening to all the perceived business benefits):

**How much workload do we need to migrate?** Remember the VM RAM utilization only tends to increase (and the few mission-critical VMs they talk about today will likely explode as soon as you implement inter-DC vMotion), so you might want to multiply today's figures by a healthy safety margin.

**How quickly do we need to evacuate the data center?** Don't forget that this business objective includes the time required for all preparatory and cleanup operations, including fixing the storage configuration and IP routing at the end of the migration.

**How often do you think we'll do that?** Of course the answer will be "we don't know" but good disaster recovery planners should always know whether they're trying to protect the assets against frequently recurring events (like yearly floods) or [100-year events](http://en.wikipedia.org/wiki/Hundred_year_flood).

From the answers to these questions, you can compute the extra bandwidth needed to migrate the workload. Add another safety margin for protocol overhead and repeat copies. 20-30% seems reasonable, but you might get way more repeat copies if you move large VMs over low-speed links; if you disagree, please add your comment.

Next, investigate how much spare capacity you have on the inter-DC links during the peak period (unless someone gives you 48 hours to evacuate the data center, you have to assume the worst-case scenario). Subtract that from the required migration bandwidth. Now you know how much extra bandwidth you need to support the disaster avoidance solution.

Last step: ask your service provider for a quote and multiply incremental monthly costs by the expected period between disaster avoidance events (if you want to be extra fancy, compute the [present value of a perpetual expense](http://en.wikipedia.org/wiki/Time_value_of_money#Present_value_of_a_perpetuity)).

{{<note info>}}A simplified data point: present value of a \$10,000 perpetual monthly expense is just over one and a quarter million dollars (\$1,254,054 to be precise) assuming 10% discount rate.{{</note>}}

The present value of the future WAN link expenses is the minimum implementation cost of the disaster avoidance idea; add the additional equipment/licensing expenses you need to support it (for example, OTV licenses for Nexus 7000) and the costs caused by increased operational complexity. Icing on the cake: add the opportunity cost of a once-in-a-decade two-DC meltdown caused by a broadcast storm or a bridging loop.

Expected final result: the disaster avoidance idea just might lose a bit of its luster after having to face the real-life implementation costs. Disagree? Please write a comment.

{{<note info>}}I would like to thank Jeremy Filliben, Matthew Norwood and Ethan Banks who helped me verify the basic assumptions of this blog post.{{</note>}}

### More Information

You'll find a long list of L2 DCI caveats and descriptions of major applicable technologies (including VPLS, OTV, vPC/VSS and F5's EtherIP) in my [Data Center Interconnects](https://www.ipspace.net/DCI) webinar.

You'll find big-picture perspective as well as in-depth discussions of various data center and network virtualization technologies in two other webinars: [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) and [VMware Networking Deep Dive](https://www.ipspace.net/VMnet).
