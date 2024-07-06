---
date: 2019-12-16 08:38:00+01:00
tags:
- design
- bridging
- WAN
title: Figure Out What Problem You’re Trying to Solve
url: /2019/12/figure-out-what-problem-youre-trying-to.html
---
A long while ago I got into an hilarious Tweetfest (note to self: don't... not that I would ever listen) starting with:

> Which feature and which Cisco router for layer2 extension over internet 100Mbps with 1500 Bytes MTU

The knee-jerk reaction was obvious: OMG, not again. The ugly ghost of BRouters (or is it RBridges or WAN Extenders?) has awoken. The best reply in this category was definitely:

> I cannot fathom the conversation where this was a legitimate design option. May the odds forever be in your favor.

A dozen "*this is a dumpster fire*" tweets later the problem was rephrased as:
<!--more-->
> Is TCP MSS option available when using bridging over VXLAN?

Ahem, not in any sane implementation. Bridging (by definition) works on layer 2 (Ethernet) and any sane implementation of bridging does not touch fields two layers above it. I'm positive there's someone right now "[exploring the opportunity](/2019/10/the-cost-of-disruptiveness-and.html)" of doing something as stupid as intercepting TCP packets and setting MSS on a Linux bridge (or equivalent). I hope they never get funded (but then there's Flannel, so my argument is invalid).

Finally, the problem was rephrased along the lines of "I need the same subnet on both sides of the WAN link" which can be [solved quite trivially with smart application of host routes](/2019/11/stretched-layer-2-subnets-in-azure.html) (or [LISP](/2017/09/why-is-cisco-pushing-lisp-in-enterprise.html) if you believe in yet another layer of indirection).

Moral of the story: it took an amazingly long time to answer the fundamental question: **What problem are we trying to solve?** Turns out it wasn't bridging over Internet, it was [IP address mobility](/2018/01/revisited-need-for-stretched-vlans.html) (or *[how to emulate what CLNS had forever within the limitations of IP forwarding model](/2015/05/reinventing-clns-with-l3-only-forwarding.html)*).

Whenever you're faced with a similar conundrum start with simple question:

**What problem are we solving?** (see above)

**Why are we solving this problem?** Quite often because [someone else didn't get their job done right](/2013/04/this-is-what-makes-networking-so-complex.html).

**What guarantees do we have that this is a temporary fix?** Hint: None, regardless of what you fervently hope for.

**What will happen the next time someone will do a similarly stupid thing?** Hint: most probably you will be told "*You solved it the last time, do it again*" The moment you decide to become the [hero of the duct tape](/2013/08/temper-your-macgyver-streak.html), you're [stuck forever](/2013/09/layer-2-extension-otv-use-cases.html) in ever-expanding vicious circle of kludges, technical debt and general stupidity... and you'll be blamed every time [the whole thing explodes](/2019/05/real-life-data-center-meltdown.html).

In most cases, the right answer is "*WE DON'T DO THAT, and this is how you should do things the right way*", potentially accompanied with a document documenting the risks and the technical debt that would be created to solve the stupidity... sent to the CIO for personal approval.

{{<note>}}
Never say NO. Saying "*we have no properly architected and tested solution addressing this requirement*" sounds way more professional ;)
{{</note>}}

OK, let's say this approach doesn't work. That means we're solving a **[real business issue](/2013/01/long-distance-vmotion-stretched-ha.html)** that costs the company **real money** instead of covering for someone else's incompetence.

**How much money are we talking about?** If there's no answer to this question you know how serious the problem is.

**How does that lost money translate into extra budget I need to solve this problem?** If there's no extra budget, tell them to get lost. Obviously the problem is not serious enough.

Finally, once every dozen blue moons you might get into a situation where someone is ready to throw real money at the problem. At that moment it helps if:

-   You understand the fundamental challenge you're trying to solve (not "bridging over WAN" but "IP address mobility")
-   You know the potential ways of solving the problem (host routes, LISP)
-   You have a vague idea which tool might be the right one to solve the problem (most routers should do a decent job, I would prefer Cumulus Linux due to its *Redistribute ARP* functionality)
-   You understand the requirements of the underlying infrastructure. For example, if you're trying to do this trick between your data center and a public cloud you're bound to figure out a few interesting public cloud packet forwarding details.

Long story short: [master the fundamentals](/2015/03/you-must-understand-fundamentals-to-be.html) (so you know what you're talking about and understand how a problem could be solved) and be prepared for the unexpected. Lots of networking engineers got prepared with [ipSpace.net webinars](https://www.ipspace.net/Webinars/) and [online courses](https://www.ipspace.net/Courses). Give them a try - maybe they will work for you as well.
