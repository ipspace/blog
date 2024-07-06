---
date: 2019-04-17 16:31:00+02:00
high-availability_tag: fail
series_weight: 450
tags:
- design
- data center
- WAN
- high availability
title: Decide How Badly You Want to Fail
url: /2019/04/decide-how-badly-you-want-to-fail.html
---
Every time I'm running a data center-related workshop I inevitably get pulled into *stretched VLAN* and *stretched clusters* discussion. While I always tell the attendees what the *right* way of doing this is, and explain the challenges of stretched VLANs from all perspectives (application, database, storage, routing, and broadcast domains) the sad truth is that sometimes there's nothing you can do.

{{<note info>}}You'll find a generic version of that explanation in [Building Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.{{</note>}}

In those sad cases, I can give the workshop attendees only one advice: face the reality, and figure out how badly you might fail. It's useless pretending that you won't get into a split-brain scenario - redundant equipment just [makes it less likely](/2012/10/if-something-can-fail-it-will.html) unless you over-complicated it in which case [adding redundancy reduces availability](/2014/04/should-we-use-redundant-supervisors.html). It's also useless pretending you won't be facing a forwarding loop.
<!--more-->
Be an [engineer](https://en.wikipedia.org/wiki/Engineer), do your job, and figure out how things are going to fail and under what conditions:

-   Start by identifying all potential failure scenarios;
-   Try to figure out how likely they are. A [forwarding loop is probably more likely than a major earthquake](/2012/04/stp-loops-strike-again.html) (unless you're in California or a few other places) or similar natural disaster, yet most everyone focuses on having geographic redundancy and believes in the magic powers of \$vendor unicorn dust;
-   Evaluate how the whole application stack will behave under each failure scenario. Figure out whether a particular failure results in a working application stack or not (hint: how will routing toward a split subnet work?);
-   Don't focus just on networking. In some scenarios, the disaster recovery plans that seem great in PowerPoint never work in practice because [someone forgot considering a "small" component like storage](/2013/01/long-distance-vmotion-stretched-ha.html);
-   Once you KNOW (or think you know) what's about to happen, test it. Usually there's a gap between theory and reality.
-   Don't forget to test applications that are supposed to be migrated to another data center on-the-fly under general panic/increased latency/reduced bandwidth conditions. It might turn out they would be useless anyway, so it's safer to shut them down and restart them.

Unfortunately you can't rely on vendors engineers to get the job done for you, or expect to find vendor blog posts (or white papers) explaining how their products fail. The only material on that topic I found were explanations on how VSS, vPC or HP IRF would fail under split brain scenarios, but nobody ever touched on the whole picture, with the notable exception of Duncan Epping's *[How to Test Failure Scenarios](http://www.yellow-bricks.com/2019/03/14/how-to-test-failure-scenarios/)*, but even there he focused exclusively on non-networking VMware components

Once you have all that data in place, sit down with everyone else who should be involved in the discussion (application, server, virtualization, storage and security teams) and figure out what the best solution would be *for your company* not for individual teams or beloved \$vendors. Sometimes you'll need to [step back and change quite a few things](/2011/01/sometimes-you-need-to-step-back-and.html).

{{<note info>}}
It will be hard to get the last bit done without a serious backing from the management, so maybe you should start there.
{{</note>}}
