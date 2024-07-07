---
title: "Network Automation Considered Harmful"
date: 2022-10-25 06:22:00
tags: [ automation ]
---
Some of the blog comments never cease to amaze me. Here's one [questioning the value of network automation](/2022/10/repost-whats-wrong-network-automation/#1421):

> I think there is a more fundamental reason than the (in my opinion simplistic) lack of skills argument. As someone mentioned on twitter
>
> "Rules make it harder to enact change. Automation is essentially a set of rules."
>
> We underestimated the fact that infrastructure is a value differentiator for many and that customization and rapid change don't go hand in hand with automation.

Whenever someone starts using MBA-speak like _value differentiator_ in a technical arguments, I get an acute allergic reaction, but maybe he's right.
<!--more-->
Introducing network automation in a small company network with a single router and one or two access points is an obvious overkill. But then we were told only last year that we should [embrace single points of failure](/2021/07/network-design-tricycles-carriers/); manual processes are the obvious next step[^1].

[^1]: Although Ubiquity is still selling it's Software-Defined (not really) cloud-based network management system. They must have awesome marketing.

I'm assuming that most of my readers run networks slightly larger than the one described above. I'm also assuming that for some of them "_Unless you're breaking stuff you're not moving fast enough_"[^2] remains a soundbite worthy of Mark Zuckerberg[^3] instead of their company culture. I was told that in environments that care about service availability manual processes still represent a huge drawback because every change has to be planned, approved, and executed in a maintenance window, while every major cloud provider and residential ISP provisions new tenants or customers 24 hours a day.

Even worse, you have to go through the same processes when making *identical changes* because you can never be sure that the infrastructure is configured in exactly the same way. Obviously that results in rubber-stamping and complacency until you hit a bit of infrastructure that's a different-enough snowflake, and then all hell breaks loose anyway.

I spent almost a decade writing about, talking about, and practicing network automation (resulting in over [380 blog posts](/tag/automation/), dozens of hours of [video content](https://my.ipspace.net/bin/list?id=NetOps), and a bunch of [GitHub repositories](https://github.com/ipspace)). If someone seriously wants to dig into various arguments we had during that time, you'll have plenty of stuff to read and watch. In the meantime, I'll conclude with a [wonderful reply left on that comment](/2022/10/repost-whats-wrong-network-automation/#1422):

[^2]: They were definitely [moving fast enough in October 2021](/2021/10/circular-dependencies-considered-harmful/) when their outage caused Sky News to invent Bridging the Gap Protocol.

[^3]: Or a lame excuse for your borked Pull Request

---

> We underestimated the fact that infrastructure is a value differentiator for many and that customization and rapid change don't go hand in hand with automation.

Which, if sold right, can be a good thing. I've called this "inflexible flexibility". We can do absolutely anything, but it'll take some effort to add it to the data model and tool chain that generates the configurations. After that, it'll be 100% supported and won't ever be something that only the one engineer that implemented the one instance knows about, catching someone else off guard at 2am when it breaks. It means no more one-offs, and that changes are inherently documented at the very least by merit of being part of a codebase with a commit that can be tracked down.

I have sometimes gotten some pushback on how this is inherently less nimble since it takes longer than just throwing a manual config at a problem, but so far haven't had any issues with the counterargument that we don't want untested configuration changes, and that developing a new feature for the automation process doesn't take much longer than properly testing a new configuration in a lab before rolling it out. The additional time is easily made up by the increased reliability of the change being executed a second time (where I mean reliability in the sense of "the customer expected the change to work the first time"). Of course, this partly depends on how your exact automation process. Ours is amenable to fairly rapid changes, because our campus network is quite dynamic.

Yes, having to run everything through an automation pipeline is less rapid than just ssh'ing into a box and typing away. But it doesn't have to be much less rapid if your staff is skilled, and raising the bar to entry for a change can often mean an opportunity for evaluation on whether the work should be done, which is a very different question than whether it can be done.

---

Finally, there must be some networking engineers running large networks who shun automation as much as the original commenter. I have great news for them: most vendors will gladly sell them all the licenses they need to [build a _Digital Twin_ of their network](/2019/09/if-you-have-to-simulate-your-whole/) to practice on.