---
date: 2014-02-13 06:49:00+01:00
ha-cloud_tag: private
high-availability_tag: cloud
series:
- ha-cloud
tags:
- firewall
- cloud
- virtualization
- high availability
title: Combine Physical and Virtual Appliances in a Private Cloud
url: /2014/02/combine-physical-and-virtual-appliances.html
---
I was running fantastic *Network Security in a Private Cloud* workshops in early 2010s and a lot of the discussions centered on the mission-impossible task of securing existing underdocumented applications, rigidity of networking team and their firewall rules and similar well-known topics.

The [*make all firewalls virtual and owned by the application team*](https://blog.ipspace.net/2013/11/typical-enterprise-application.html) idea also encountered the expected resistance, but enabled us to start thinking in more generic terms.
<!--more-->
### Keep the Physical Firewalls

Nobody was willing to get rid of the physical firewalls separating the private cloud from the Internet. The idea of [connecting the outside network straight to a set of servers](https://blog.ipspace.net/2013/07/cloud-as-appliance-design.html) (even though they might be in a separate cluster and running solely VM-based firewall appliances) was simply too radical.

However, we also quickly agreed that it doesn't make sense to maintain thousands of firewall rules on the Internet-facing physical firewalls. Those firewalls should do the basic traffic scrubbing and potentially some content inspection. They could also be combined with IDS/IPS systems or traffic monitoring systems. Most importantly, these devices wouldn't do any application-specific filtering. Their ruleset would be kept simple and thus easy to monitor and audit.

{{<note>}}If you're building a perimeter defense for a dedicated private cloud infrastructure that does not rely on external services, [you might not need firewalls at all](https://blog.ipspace.net/2010/08/i-dont-need-no-stinking-firewall-or-do.html). Simple packet filters are more than good enough to block unwanted incoming traffic; [stateful firewalls](http://blog.ipspace.net/2013/03/the-spectrum-of-firewall-statefulness.html) add value primarily in scenarios where inside clients access outside servers.{{</note>}}

The outside perimeter built with trusted physical appliances would thus separate the Internet Wild West from a scrubbed (but still not very trusted) DMZ segment. Proxy servers, shared caching servers and some load balancers could connect straight to that segment.

{{<figure src="/2014/02/s1600-2Level_FW.png" caption="Multi-level firewalling">}}

### Add the Applications

Individual application stacks would connect to the scrubbed DMZ segment through [application-specific firewalls implemented in virtual machines](https://blog.ipspace.net/2013/05/simplify-your-disaster-recovery-with.html) (an approach known in Roman times as *divide* *et impera*).

The application teams could use NSX-T edge firewalls and load balancers, F5 BIG-IP VTM or any other VM appliance that offers firewalling and load balancing in the same VM instance, and the simpler single-VM applications might use [VM NIC firewalls](https://blog.ipspace.net/2012/11/virtual-firewall-taxonomy.html) (available in one form or another in most private cloud ecosystems). Each VM appliance would contain the rules specific to the protected application, [making configuration, monitoring and auditing relatively simple](http://blog.ipspace.net/2013/12/omg-who-will-manage-all-those-virtual.html).

Most importantly, the security team would generate sample VM images that the application teams could deploy from a central catalog, making sure the application teams start with a well-configured initial state that they could use as-is or modify it for their own needs (obviously taking full responsibility for any deviation from the baseline).

### Need More Information?

For more technical details, check out the [ipSpace.net cloud infrastructure resources](http://www.ipspace.net/Cloud), in particular the [Designing Private Cloud Infrastructure](http://www.ipspace.net/BCloud) webinar.
