---
date: 2018-10-25 07:51:00+02:00
tags:
- automation
- intent-based networking
title: What’s the Big Deal with Validation?
url: /2018/10/whats-big-deal-with-validation/
intent-based-networking_tag: related
---
*This blog post was initially sent to subscribers of my mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*

In his [Intent-Based Networking Taxonomy](https://blogs.juniper.net/en-us/enterprise-cloud-and-transformation/intent-based-networking-automation-taxonomy) blog post Saša Ratković mentioned *real-time change validation* as one of the requirements for a true intent-based networking product.

Old-time networking engineers would instinctively say "_sure, we need that_" while most everyone else might be totally flabbergasted. After all, when you create a VM, the VM is there (or you'd get an error message), and when you write to a file and sync the file system the data is stored, right?

As is often the case, networking is different.
<!--more-->
Let's start with the real challenges. A network is a [tightly coupled distributed system](/2013/09/openflow-fabric-controllers-are-light/) built from unreliable components (I'm talking about links, not software we have to deal with -- that's topic for another time). Validating that all components are still operating as expected makes perfect sense.

At this point it's worth mentioning that most other IT systems ignore the reality of unreliable components (see also: [fallacies of distributed computing](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)) or at least don't do that well. Servers crash when they lose connectivity to storage or encounter parity error, software crashes when it encounters an exception that might be [triggered by cosmic rays](https://en.wikipedia.org/wiki/Soft_error)...

Then there's the other kind of validation -- the WTF one. In January 2018 I was sitting in a presentation where a major networking vendor explained how their network assurance engine validates that the configuration requests made through their SDN controller are properly implemented on their proprietary closed hardware fabric. The whole thing became so ridiculous that we had to ask the obvious question "_Are you telling us we should buy additional software to check whether your software is bug-free?_"

Why would we ever have to do something as crazy as that? Ignoring the subpar software quality for the moment the root cause is often the unreliable mechanism we have to use to configure network devices -- from CLI that was designed for hands and eyes of an operator not automation scripts, to NETCONF implementations that don't support candidate configurations or can't even rollback on error. Finally, there are always edge cases where the device software tries to squeeze too much into device hardware and fails without reporting the failure.

As long as customers are not willing to vote with their wallets and buy gear that [properly implements mechanisms needed for somewhat-reliable network automation](/2016/10/network-automation-rfp-requirements/) there's little we can do apart from:

-   **Use _Trust but Verify_ approach** -- every time you make a change to a networking device, use **show** commands (not device configuration) to validate that the changes were implemented. Bonus points for using real traffic instead of **show** commands.
-   **Minimize the changes made to networking devices** -- [configuring a gazillion features on network edge](/2013/08/temper-your-macgyver-streak/) to solve [higher-level incompetence](/2013/04/this-is-what-makes-networking-so-complex/) is a sure recipe for a disaster;
-   **Minimize the blast radius** -- old-time service providers built separate *transport* and *services* infrastructure for a good reason. That lesson somehow got lost in various converged crazes. Hardware networking vendors [fighting nail and tooth to avoid irrelevance](/2013/06/network-virtualization-and-spaghetti/) don't help either.

We covered the first topic in some details in [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course, and discussed various aspects of the third one in virtualization webinars (all of them available with [ipSpace.net subscription](https://www.ipspace.net/Subscription)) and [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
