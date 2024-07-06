---
date: 2014-04-30 10:28:00+02:00
tags: [ SDN, intent-based networking ]
title: Declarative and Procedural Programming (and How I Got It all Wrong)
url: /2014/04/declarative-and-procedural-programming.html
intent-based-networking_tag: declarative
series_weight: 300
---
During a recent NetOps-focused discussion trying to figure out where Puppet/Chef/Ansible/... make sense in the brave new SDN-focused networking world I made this analogy: "*Puppet manifest is like* [*Prolog*](http://en.wikipedia.org/wiki/Prolog)*, router configuration is like Java or C++*." It's a nice sound bite. It's also totally wrong.

{{<note info>}}If you never met Prolog, you might consider yourself lucky. Or you might [want to figure out what it is](http://www.cs.toronto.edu/~sheila/384/w11/simple-prolog-examples.html) (warning: it might make your head explode). Just joking, I actually quite liked it in my programming days.{{</note>}}
<!--more-->
### Declarative versus Procedural Programming

In a nutshell, [*declarative* programming](http://en.wikipedia.org/wiki/Declarative_programming) languages allow you to tell **what** needs to be done, not **how** to do it (which is what [*procedural* programming](http://en.wikipedia.org/wiki/Procedural_programming) languages are all about).

Unfortunately nothing good just happens to happen (at least not in IT world, or it might have to do with the second law of thermodynamics), you need *something* that will make the transition (or find a path) from where we are now to the final state (the **what**). The *something* might be a language interpreter (in Prolog's case performing an exhaustive search of the solution tree to figure out if it can satisfy the requirements specified in the declarative program) or a Puppet agent that:

-   Compares the current state of the system (example: web server) with the desired state (Puppet manifest);
-   Figures out the differences;
-   Applies changes (modifying configurations, creating files, executing commands...) that have to be made to transition the system from the current state to the desired state.

It's obvious router configurations aren't procedural programs -- they tell a device (or software) **what** needs to be done not **how** that behavior should be implemented. In most cases you cannot influence the implementation details; EEM applets are an obvious exception, but the only reason they reside in router configuration is the lack of decent text editing tools on network devices convenience of manipulating router configuration as compared to anything else.

### So What's the Difference?

The real difference between Puppet manifests and router configurations is the level of abstraction. Puppet manifests *should* focus on resources (example: VLANs) and desired state of resources (example: VLAN 10 present on port GigabitEthernet0/1) not on the [implementation details](http://networkenhancers.blogspot.com/2011/01/vlan-configuration-comparision-cisco.html).

Did I say *implementation details*? Isn't that procedural programming? No, we're still in the realm of declarative programming (we never tell the switches **how** to implement VLANs, do we?), but working at a lower level of abstraction and dealing with how individual devices (or vendors) expect things to be declared.

Confusing? Sure it is, but don't worry. It's no more confusing than [other things we have to deal with](http://en.wikipedia.org/wiki/OSI_model). You just need a bit of practice... and don't forget to [focus on principles, not implementation details](/2008/09/knowledge-or-recipes.html).
