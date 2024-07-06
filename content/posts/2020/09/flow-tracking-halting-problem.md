---
date: 2020-09-23 06:37:00+00:00
series:
- host-firewalls
tags:
- firewall
- security
title: Using Flow Tracking to Build Firewall Rulesets... and Halting Problem
---
Peter Welcher identified the biggest network security hurdle faced by most enterprise IT environments in [his comment](/2020/09/considerations-host-based-firewalls.html#111) to [Considerations for Host-based Firewalls (Part 1)](/2020/09/considerations-host-based-firewalls.html) blog post:

> I have NEVER found a customer application team that can tell me all the servers they are using, their IP addresses, let alone the ports they use.

His proposed solution: use software like Tetration (or any other flow collecting tool) to figure out what's really going on:
<!--more-->
> This has made me a big believer in products like Tetration and getting the actual flows documented to secure the servers and be ready in advance of application troubleshooting.

Knowing what's out there is good. Being prepared is even better. Using collected flow information to build firewall rulesets (the idea promoted by Cisco's Tetration team and VMware NSX-T team) is dangerous as I pointed out during several Networking Field Day presentations.

In two words: [Halting Problem](https://en.wikipedia.org/wiki/Halting_problem).

Short summary in case you can't be bothered to read the Wikipedia article: as early as 1936 Alan Turing proved that it's impossible to figure out whether an algorithm will produce a result (= halt) for a given input (or more generically, for all inputs). It's easy to demonstrate that an algorithm halts for a specific input (you run it, it completes, problem solved), but it's impossible to demonstrate what happens if it takes _forever_ (unless you keep track of complete state of the machine executing the algorithm, and prove that it got back to a previous state, so it must be stuck in an infinite loop... but I'm digressing).

Back to networking: collecting flow information for any reasonable amount of time does not guarantee that you have seen all potential flows. Without analyzing the application code (and if you could do that you wouldn't have to collect the flow information in the first place), it's impossible to figure out whether the application has experienced all edge cases and generated all potential flows.

I usually use _end-of-quarter_ and _end-of-year_ processes to illustrate this point, and the usual (academically somewhat correct, but totally impractical) response to that argument I get from the vendors presenting their magic tool is "_well, you collect flow information for several quarters before using it to create firewall rules._" Yeah, sure...

However, there's an even more worrisome example: handling failure scenarios. Imagine a simple relational database setup with a read/write and two read/only replicas, one of them in the same data center (for quick failover), the other one in a remote data center (for disaster recovery purposes). 

During the normal operation, the flow-collecting tool would see flows between the read/write replica and both read/only replicas, but nothing between the read/only replicas. Building firewall ruleset based on that information would not allow any traffic between read/only replicas. So far so good... until the read/write replica fails, the on-premises read/only replica takes over... and (best case) you lost georedundancy or (worst case) your data should another disaster strike while everyone keeps ignoring the frantic database error logs. Good job.

**Long story short**:

* Collecting flow information is never a bad idea (it might be expensive though);
* Using collected flow information to _automaticaly_ build firewall rules (sprinkle some AI/ML magic on top for dramatic effects) might give you the results you deserve.