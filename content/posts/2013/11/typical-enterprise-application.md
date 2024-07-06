---
date: 2013-11-20T07:00:00.000+01:00
tags: [ data center, overlay networks, virtualization ]
title: Typical Enterprise Application Deployment Process is Broken
---
As one of their early marketing moves, VMware started promoting VMware NSX with a catchy “fact” – you can deploy a new VM or virtual disk in minutes, but it usually takes days or more before you can get a new VLAN or a firewall or load balancer rule from the networking team.

Ignoring the [complexity of network virtualization](/2013/09/why-is-network-virtualization-so-hard.html), they had a point, and the network services rigidity really bothered me … until I finally realized that we’re dealing with a broken process.
<!--more-->
You see, regardless of how an application is developed and tested, the side effects of application development usually include a build recipe – a process that builds application environment from known initial state (or from scratch). The build process is hopefully used to generate QA, UAT and production environments … and it almost never includes the networking infrastructure or services.

{{<note warn>}}If your application development team doesn’t have something similar in place, network services are the least of your problems.{{</note>}}

Imagine car designers ignoring air drag or boat designers testing boats in wind tunnels instead of the water. That’s how typical enterprise application development process works … and then the designers blame the mechanics when their concoction fails after being exposed to laws of physics.

Even worse, the networking team is usually engaged when the developers throw their shiny new product across the Dev/Ops wall (because nobody could possibly predict the application requirements in advance). Server team is ready to deploy (they have virtual disk images from the build process) when the networking team gets the first whiff of the application (having a list of IP addresses and TCP port numbers the application uses is usually wishful thinking). [Waterfall application development](http://en.wikipedia.org/wiki/Waterfall_model) at its extreme.

![](worked-fine-in-dev-ops-problem-now.jpg)  

But wait, you might say, isn’t everyone moving toward [DevOps](http://en.wikipedia.org/wiki/Devops) these days? Isn’t that a solution? DevOps is definitely the step in the right direction and exposes application developers to real-life constraints, so they might consider the lessons learned in Ops part of their life when coding the next application … but it doesn’t ensure we’ll get the results we’re looking for.

The only way to fix the application deployment process is to include the networking aspects of the application stack in all stages of application deployment, from development (where the developers MUST use multiple application instances, load balancers, firewalls, and artificial bandwidth limiters and latency injection) through QA/UAT (where the testers MUST test the applications with final configuration of load balancers, firewalls and other network services elements) to production deployment (which becomes exceedingly simple because you already have all network services elements).

Obviously it’s hard to change the application development process while being tied to physical appliances – it’s usually hard to get dedicated appliances for Dev/QA/UAT environments, and it’s always fun to merge changes and additions to firewall or load balancer configurations. The only reasonably straightforward solution is to dump physical appliances and use [per-application virtual ones](/2013/11/make-every-application-independent.html). Throw overlay virtual networks into the mix (they can be provisioned in seconds without touching the physical gear) and you get an environment that just might work.

#### More information

[Network virtualization webinars](http://www.ipspace.net/Roadmap/Virtualization_webinars) describing the concepts mentioned in this post include:

-   [Overlay Virtual Networking](http://www.ipspace.net/Overlay_Virtual_Networking)
-   [Cloud Computing Networking](http://www.ipspace.net/Cloud_Computing_Networking)
-   [Virtual Firewalls](http://www.ipspace.net/Virtual_Firewalls)
-   [VMware NSX Technical Deep Dive](http://www.ipspace.net/NSX)
