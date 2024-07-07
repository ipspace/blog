---
title: "Claim: You Don't Have to Be a Networking Expert to Do Kubernetes Network Security"
date: 2021-04-08 06:14:00
tags: [ security, containers ]
---
I was listening to an excellent *container networking* podcast and enjoyed it thoroughly until the guest said something along the lines of:

> With Kubernetes networking policy, you no longer have to be a networking expert to do container network security.

That's not even wrong. You didn't have to be a networking expert to write traffic filtering rules for ages.
<!--more-->
Let's deal with the *Kubernetes* part of the statement first. What Kubernetes brought to the table is:

* Identifying pods by unique IP addresses (no sharing of services under the same IP address)
* Labeling containers and using pod labels or namespace labels instead of IP addresses in network policies.
* Consistent and stable API (more about that later).

But what if you want to be more granular? If you want to block access to specific applications, you still have to specify layer-4 protocol (TCP or UDP) and port numbers in a network policy rule.

How's that different from traditional firewall rules? It's not. In the end, unless you're willing to modify container TCP stack and implement an outside-the-box greenfield solution using certificates (or something similar), you're bound to be doing 5-tuple filtering or spending an enormous amount of CPU cycles trying to reverse-engineer application intent with deep packet inspection. You simply can't beat the laws of physics without moving into another universe.

Using labels instead of hard-coding IP addresses is also nothing new. We had that functionality in firewall management software like Panorama, and virtual microsegmentation solutions like VMware NSX for ages.

**To recap**: The filtering mechanisms haven't changed, the granularity hasn't changed, the way to specify applications hasn't changed, the labeling concepts were there before... but in the old days you needed a networking expert, and now you don't have to know anything about networking to make it work because you can write the rules in YAML? Makes no sense to me.

However, as my friend [Matthias Luft](https://www.ipspace.net/Author:Matthias_Luft) pointed out when I asked him about his view of this challenge, the tools you get with Kubernetes are much better than what you had with traditional firewalls. Instead of [GUI, no CLI, and broken API](/2018/02/anti-automation-from-antimatter-universe/), you get a stable API you could use in your CI/CD pipeline, GitOps, or whatever other automation approach you prefer.

Finally, there's a simple reason we had dedicated teams changing network security rules in traditional enterprise environments: whoever was responsible for security didn't trust the developers to do the right thing instead of inserting a **permit any any** rule to make their broken deploy work and walking away. How's that going to change with Kubernetes network policy?

The only way to tackle that challenge is to change mindsets and processes. Here's what Matthias had to say on that topic:

{{<long-quote>}}
Having a security team change firewall rules because we didn't trust the developers/engineers is a very tricky thing IMO. It reflects a more general issue with your security team culture. 

We invested heavily into engineering relationships and we do not have any process where we are the blocking factor. That led to engineers checking in with us on their own when they thought they performed remotely security-relevant changes. 

Also, we have lots of detection automation in place (see my first point) to catch accidentally insecure changes -- I also touched that overall topic a bit in my [host-based firewall posts](/2020/09/considerations-host-based-firewalls/). 
{{</long-quote>}}
