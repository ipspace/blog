---
title: "Claim: You Don't Have to Be a Networking Expert to Do Kubernetes Network Security"
# date: 2021-03-27 10:14:00
tags: [ security, containers ]
draft: True
intro: |
  Claiming that kubernetes network security solves a process problem is totally wrong.
---
I was listening to an excellent *container networking (TBD)* podcast and enjoyed it thoroughly until the guest said something along the lines of:

> With Kubernetes networking policy, you no longer have to be a networking expert to do container network security.

That's not even wrong. You didn't have to be a networking expert to write traffic filtering rules for ages.

Let's deal with the *Kubernetes* part of the statement first. What Kubernetes brought to the table is:

* Identifying pods by unique IP addresses (no sharing of services under the same IP address)
* Labeling containers and using pod labels or namespace labels instead of IP addresses in network policies.

But what if you want to be more granular? If you want to block access to specific applications, you still have specify layer-4 protocol (TCP or UDP) and port numbers in a network policy rule.

How's that different from traditional firewall rules? It's not. In the end, unless you're willing to modify container TCP stack and implement an outside-the-box greenfield solution using certificates (or something similar), you're bound to be doing 5-tuple filtering or spending an enormous amount of CPU cycles trying to reverse-engineer application intent with deep packet inspection. You simply can't beat the laws of physics without moving into another universe.

Using labels instead of hard-coding IP addresses is also nothing new. We had that functionality in firewall management software like Panorama, and virtual microsegmentation solutions like VMware NSX for ages.

**To recap**: The filtering mechanisms haven't changed, the granularity hasn't changed, the way to specify applications hasn't changed, the labeling concepts were there before... but in the old days you needed a networking expert, and now you don't have to know anything about networking to make it work because you can write the rules in YAML? Makes no sense to me.

Also, there's a simple reason we had dedicated teams changing network security rules in traditional enterprise environments: whoever was responsible for security didn't trust the developers to do the right thing instead of inserting a **permit any any** rule to make their broken deploy work and walking away. How's that going to change with Kubernetes network policy? Beats me...