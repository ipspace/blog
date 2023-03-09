---
date: 2013-01-30 09:00:00.001000+01:00
dr_tag: intro
high-availability_tag: dr
series:
- dr
tags:
- data center
- vMotion
- high availability
title: Long-Distance vMotion, Stretched HA Clusters and Business Needs
url: /2013/01/long-distance-vmotion-stretched-ha.html
---
During a recent [vMotion-over-VXLAN](http://www.yellow-bricks.com/2013/01/29/vmotion-over-vxlan-is-it-supported/) discussion Chris Saunders made a very good point: "*Folks should be asking a better question, like: Can I use VXLAN and vMotion together to meet my business requirements.*"

Yeah, it's always worth exploring the actual business needs.

### Based on a true story \...

A while ago I was sitting in a roomful of extremely intelligent engineers working for a large data center company. Unfortunately they had been listening to a wrong group of virtualization consultants and ended up with the picture-perfect disaster-in-waiting: two data centers bridged together to support a [stretched VMware HA cluster](https://blog.ipspace.net/2011/06/stretched-clusters-almost-as-good-as.html).
<!--more-->
{{<note>}}Actually, the disaster was no longer "in-waiting", they had already experienced a perfect bridging storm that took down both data centers.{{</note>}}

During the discussion I tried not to be prejudicial grumpy L3 guru that I'm known to be (at least in vendor marketing circles) and focused on figuring out the actual business needs that triggered that [oh-so-popular design](https://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html).

*Q:* "So what loads would you typically vMotion between the data centers?"

*A:* "We don't use long-distance vMotion, that wouldn't work well... the VM would have to access the disk data residing on the LUN in the other data center"

{{<note>}}Before you write a comment telling me how you could use storage vMotion to move the data and the vMotion to move the VM, do me a favor and [do some math](https://blog.ipspace.net/2011/09/long-distance-vmotion-for-disaster.html).{{</note>}}

*Q:* "So why do you have stretched HA cluster?"

*A:* "It's purely for disaster recovery -- when one data center fails, the VMs of the customers (or applications) that pay for disaster recovery get restarted in the second data center."

*Q:* "And how do you prevent HA or DRS from accidentally moving a VM to the other data center"

*A:* "Let's see..."

{{<note info>}}At this point you'd usually get one of these answers: (A) we use affinity rules... and hope nobody has a fat-finger day or (B) we have the hosts in the second data center in maintenance mode.{{</note>}}

*Q:* "OK, so when the first data center fails, everything gets automatically restarted in the second data center. Was that your goal?"

*A:* (from the storage admin) "Actually, I have to change the primary disk array first -- I wouldn't want a split-brain situation to destroy all the data, so the disk array failover is controlled by the operator"

*Q:* "Let's see -- you have a network infrastructure that exposes you to significant risk, and all you wanted to have is the ability to restart the VMs of some customers in the other data center using an operator-triggered process?"

*A:* "Actually, yes"

*Q:* "And is the move back to the original data center automatic after it gets back online?"

*A:* "No, that would be too risky"

*Q:* "So the VMs in subnet X would never be active in both data centers at the same time?"

*A:* "No."

*Q:* "And so it would be OK if you would move subnet X from DC-A to DC-B during the disaster recovery process?"

*A:* "Yeah, that could work..."

*Q:* "OK, one more question -- how quickly do you have to perform the disaster recovery?"

*A:* "Well, we'd have to look into our contracts \..."

*Q:* "But what would the usual contractual time be?"

*A:* "Somewhere around four hours"

*Q:* "Let's summarize -- you need a disaster recovery process that has to complete in four hours and is triggered manually. Why don't you reconfigure the data center switches at the same time to move the IP subnets from the failed data center to the backup data center during the disaster recovery process? After all, you have switches from vendor (C\|J\|A\|D\|\...) that could be reconfigured from a DR script using NETCONF."

*A:* (from the network admin) "Yeah, that's probably a good idea."

Does this picture look familiar (particularly the business consultant part)?

{{<figure src="s1600-project.jpg" caption="Source: www.projectcartoon.com">}}
