---
date: 2020-10-07 06:05:00+00:00
series:
- host-firewalls
tags:
- firewall
- data center
- design
title: Fixing Firewall Ruleset Problem For Good
---
Before we start: if you're new to my blog (or stumbled upon this blog post by incident) you might want to read the [Considerations for Host-Based Firewalls](/2020/09/considerations-host-based-firewalls/) for a brief overview of the challenge, and my explanation why [flow-tracking tools cannot be used to auto-generate firewall policies](/2020/09/flow-tracking-halting-problem/).

As expected, the "_you cannot do it_" post on LinkedIn [generated numerous comments](https://www.linkedin.com/posts/ivanpepelnjak_using-flow-tracking-to-build-firewall-rulesets-activity-6714427175409348608-Vvj1/), ranging from good ideas to borderline ridiculous attempts to fix a problem that has been proven to be unfixable (see also: [perpetual motion](https://en.wikipedia.org/wiki/Perpetual_motion)).
<!--more-->
{{<series single="1">}}

**You could use flow-tracking tools for discovery purposes**. Absolutely true. Is it worth the price of a Tetration installation? You tell me...

**You could use flow-tracking tools to find unexpected flows**. Another good one. Assuming your desired firewall policy is documented in a machine-readable way, you could automatically check whether the observed flows should be permitted, and point out the discrepancies. Is this idea practical? As always it depends.

**You could use observed flows as the starting point to build your firewall ruleset**. In theory, yes. In practice, you wouldn't know whether all the observed flows are legitimate, and you'd still need an in-depth understanding of application architecture to transform the observed flows into firewall rules that would be able to deal with failure scenarios like the ones I described in the [original blog post](/2020/09/flow-tracking-halting-problem/). Let me remind you that the only reason we started walking down this intractable path was

> I have NEVER found a customer application team that can tell me all the servers they are using, their IP addresses, let alone the ports they use.

At this point, you could go back to the drawing board and try to add another layer of convolution to your perpetual motion machine (after all, [ingenious people tried to solve the original problem for over a thousand years](https://en.wikipedia.org/wiki/History_of_perpetual_motion_machines)), or you could admit that you have a people/process problem that cannot be solved by throwing heaps of magic technology at it.

> Insanity: doing the same thing over and over again and expecting different results.

The only way (I can see) to have sane, consistent, and up-to-date firewall rules is to [fix the application deployment process](/2013/11/typical-enterprise-application/) and embed the required security rules in application deployment recipes ([example](/2020/09/aws-security-example/)).

**But the application teams have no idea what they need**. No problem. You have network security experts on hand, and they can work with the application team to come up with the required security rules. All you need to make this work is a firm rule enforced by top-level IT management: "_no automated deployment recipe, no deployment_".

**But they will put "permit any any" in the security rules to make it work**. I hope your application development process includes code review (and if it doesn't, you have bigger problems on your hands anyway). Make deployment recipe review mandatory part of code review process.

**But everyone will scream at the OPS team, and the applications will be deployed anyway**. If you're big enough to have this problem (and it cannot be solved over a beer and a pizza), you probably have some sort of [risk assessment and management](https://en.wikipedia.org/wiki/IT_risk_management) in place. Maybe it's time to submit a report to that team and make it their problem?

But even though you could eventually clean up the Augean Stables of application deployment, what should you do with the legacy applications? [Letting them gradually disappear](/2017/02/q-migrating-to-modern-data-center/) would be the ideal solution. If that doesn't work ask a simple question: "_Is that problem worth solving?_", and if you think it is, the next question should be "_What would be the simplest good-enough solution?_". Without the answers to these two questions you'll be an easy mark for the next snake-oil vendor with a glitzy slide deck.