---
date: 2021-06-24 07:13:00+00:00
dr_tag: stretch
high-availability_tag: dr
series:
- dr
tags:
- high availability
- data center
- design
title: 'Stretched VLANs: What Problem Are You Trying to Solve?'
---
One of ipSpace.net subscribers sent me this interesting question:

>  I am the network administrator of a small data center network that spans 2 buildings. The main building has a pair of L2/L3 10G core switches. The second building has a stack of access switches connected to the main building with 10G uplinks. This secondary datacenter has got some ESX hosts and NAS for remote backup and some VM for development and testing, but all the Internet connection, firewall and server are in the main building. 
>
> There is no routing in the secondary building and most of the VLANs are stretched. Do you think I must change that (bringing routing to the secondary datacenter), or keep it simple like it is now?

As always, _it depends_, this time on _what problem are you trying to solve?_
<!--more-->
There are numerous valid reasons why someone would want to have their data center resources in multiple locations:

* They ran out of space and had to expand into a different location[^1]
* They want to have a backup location in case something bad happens to the primary location
* They want to build an active-active architecture[^2]

Assuming our subscriber needs more space, the current approach works reasonably well as long as there's enough bandwidth between the two locations, and as the two locations are effectively a single data center, we shouldn't be too concerned about stretched VLANs. The setup might be good enough to fool an incompetent auditor into ticking off the "redundant location" box. Mission accomplished.

For whatever reason, most organizations want to have a second data center location for resiliency/redundancy purposes, in which case you should start thinking about failure scenarios -- you wouldn't want to be in a situation where a disaster happens, and the IT team discovers [their backup plans have no chance of working](/2013/01/long-distance-vmotion-stretched-ha/). The first question to ask is thus: _what do you plan to protect against?_

Fire, flood, power outage caused by roadworks… the second location will save the day. One of the buildings can burn down, and as long as the other one is not affected, you’re good to go… assuming you have sufficient infrastructure in the second building. Unfortunately, in the specific case mentioned above, all Internet connections and firewalls are in the first building, so the second building makes absolutely no sense from the resiliency perspective.

However, I've seen more network meltdowns than burned buildings[^3], and a [single VLAN is always a single packet forwarding failure domain](/2012/05/layer-2-network-is-single-failure/). There are no safeguards like TTL checks or routing tables within a VLAN. A single endpoint going crazy can bring down the whole VLAN, and if you [stretch a single VLAN across multiple locations](/2020/09/disaster-recovery-vendor-marketing/), a single problem can bring down both locations. You could use modern technologies like VXLAN (and maybe EVPN) to eliminate some of the sore points, but not all -- both locations will [still be a single availability zone](/2019/12/disaster-recover-and-failure-domains/).

Want to do it right? I described the concepts in _[Designing Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers)_ webinar, and focused on interesting details in [numerous blog posts](/tag/high-availability/).

[^1]: I've met a customer that had two sites literally across the street, with several large fiber cables (with dozens of strands) connecting them.

[^2]: Hopefully one that will work outside the PowerPoint sandbox.

[^3]: That might have something to do with me being a network engineer and not a firefighter, but I'm digressing.
