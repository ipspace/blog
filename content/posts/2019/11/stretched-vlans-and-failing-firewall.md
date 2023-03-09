---
date: 2019-11-12 08:14:00+01:00
dr_tag: vendor
ha-cluster_tag: firewall
high-availability_tag: dr
series:
- ha-cluster
- dr
tags:
- design
- firewall
- data center
- high availability
title: Stretched VLANs and Failing Firewall Clusters
url: /2019/11/stretched-vlans-and-failing-firewall.html
---
After publishing the *[Disaster Recovery Faking, Take Two](https://blog.ipspace.net/2019/10/disaster-recovery-faking-take-two.html)* blog post (you might want to read that one before proceeding) I was severely reprimanded by several people with ties to virtualization vendors for blaming virtualization consultants when it was obvious the firewall clusters stretched across two data centers caused the total data center meltdown.

Let's chase that elephant out of the room first. When you drive too fast on an icy road and crash into a tree who do you blame?

-   The person who told you it's perfectly OK to do so;
-   The tire manufacturer who advertised how safe their tires were?
-   The tires for failing to ignore the laws of physics;
-   Yourself for listening to bad advice

For whatever reason some people love to blame the tires ;)
<!--more-->
Now for [stretched firewall clusters](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html). Building a reliable clustering solution is hard - according to some people it's so hard that non-clustered solutions have higher uptime than clustered ones, because everything else in the system has a lower failure rate than the clustering software.

Ignoring that bit of wisdom, building a 2-node cluster is the worst thing you can do. Getting a majority in a 2-vote system is a bit hard, and most clustering solutions get around that limitation by adding a *witness node* - a fake node that does nothing else but helps the voting algorithm.

{{<note>}}Why don't we build a 3-node firewall cluster? Because nobody wants to pay for the extra node just to have sane clustering behavior.{{</note>}}

In compute clusters the disks usually serve as the witness nodes. In firewall clusters we could use virtual machines (or something else), but that would make the firewall cluster dependent on some other infrastructure, and security engineers wouldn't appreciate that.

{{<note>}}Relying on clustered storage as a witness node for compute clusters is "turtles all the way down" and people doing that sometimes get what they deserve: after a split-brain event, both storage arrays become active, both cluster nodes think they have majority, and do fun stuff with the data. Recovery from that scenario usually involves restores from backup tapes.{{</note>}}

The firewall vendors "solved" the *witness node* problem by using the communication paths between the cluster nodes as the tie-breaker. There are at least three independent connections between the members of a firewall cluster: inside link(s), outside link(s) and cluster link. If a cluster node cannot reach its peer through any of these links, it's safe to assume the peer is dead and take over, right?

Well, that line of reasoning was perfectly valid as long as the three links were independent. When stretching a firewall cluster across multiple sites the three links between the firewalls usually get turned into three VLANs running across shared DCI infrastructure, effectively turning what was supposed to be three independent links into a shared-risk link group. No wonder the solution doesn't work as advertised.

Could we make it better? Sure, change your design. Oh, without that? Sure, make sure the three links are really independent. Oh, without paying for extra links? Wish you luck - I'm out of here...

Then there's the "minor" detail of failure probability. In a cluster made from adjacent devices connected with point-to-point links the links themselves are least likely to fail, and if they fail, they usually fail in a predictable way, so you can assume they are reliable and move on. When stretching the cluster nodes across multiple sites the links between them become the least reliable component and might exhibit all sorts of gray failures. Do you seriously think the firewall vendors can simulate all those failure scenarios?

{{<note>}}Somewhat-related: data center fabric vendors faced the same problems (example: Juniper VCS, HP IRF) but made a sane choice: one node in the cluster has two votes, and the [minority nodes shut down in split-brain scenario](https://blog.ipspace.net/2011/09/long-distance-irf-fabric-works-best-in.html). For whatever reason that was not found acceptable by the firewall vendors.{{</note>}}

That brings me to the final part of this sad story. Any reliability engineer analyzing the whole thing should come to the same conclusion: **Don't ever do it**... but why are the firewall vendors still promoting such solutions? I guess it's always a 737MAX-like story (minus the loss of life): while at least some development engineers know it's not safe to do things the way they are advertised, the product managers and the sales team are doing whatever it takes to sell the gear, and nobody listens to the engineers anyway.

So what can you do? You claim to be an engineer, right? So learn the fundamentals, figure out how things (probably) work and go from there. Some "solutions" are inherently unsafe - it's your job to identify them (don't ever rely on vendors doing that job for you - FAA learned that the hard way), and work with your peers to build a solution that [satisfies the true business needs of your company](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html).

Failing that, [decide how badly you want to fail](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html), for example when you [don't have the budget for a proper solution](https://blog.ipspace.net/2015/10/sometimes-you-have-to-decide-how-badly.html).
