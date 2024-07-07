---
title: "Docker Swarm Services behind the Scenes"
date: 2020-08-26 06:54:00
tags: [ Docker, overlay networks ]
---
Remember the [claim that networking is becoming obsolete](/2020/02/the-never-ending-my-overlay-is-better/) and that everyone else will simply bypass the networking teams ([source](https://twitter.com/martin_casado/status/1227793721019600897))?

> Good news for you – there are many fast growing overlay solutions that are adopted by apps and security teams and bypass the networking teams altogether.

That sounds awesome in a VC pitch deck. Let's see how well that concept works out in reality using Docker Swarm as an example (Kubernetes is [probably even worse](https://speakerdeck.com/thockin/kubernetes-and-networks-why-is-this-so-dang-hard)).
<!--more-->
It took me a long while to decode what Docker is doing behind the scenes (documentation lacking critical details didn't exactly help), but finally I got there with copious help of detailed third-party blog posts. Here's a diagram documenting the Linux networking constructs a packet must traverse to get from an Ethernet NIC to a container deployed as a simple Docker Swarm service:

{{<figure src="/2020/08/Docker-Swarm-Service.jpg" caption="The path to reach a service container in Docker Swarm" >}}

- - -
Legend:
* Gray boxes are namespaces (from host TCP stack to container namespace);
* Bridges are Linux bridges;
* Routers are full-blown Linux TCP/IP stacks;
* Vertical boxes are **iptables** tables.
- - -
All it takes to get Docker Swarm service up and running are three Linux bridges, three full-blown TCP stacks, two sets of NAT iptables, a mangle iptable, and a kernel-based load balancer. To make it even more fun, Docker hides most of these constructs in three network namespaces that are not visible unless you remap /var/run directories. What could be more fun to troubleshoot? How about the same service spread across multiple Docker hosts (omitting the host TCP stack transporting VXLAN packets)?

{{<figure src="/2020/08/Docker-Swarm-Multihost-Service.jpg" caption="The path to reach a service container on another Docker Swarm node" >}}

For a step-by-step deep dive into behind-the-scenes packet processing, register for the [Docker Networking Deep Dive](https://www.ipspace.net/Docker_Networking_Deep_Dive) live session on September 1st 2020.
