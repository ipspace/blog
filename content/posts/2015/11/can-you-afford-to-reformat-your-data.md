---
date: 2015-11-23 09:57:00+01:00
dr_tag: vendor
high-availability_tag: dr
series:
- dr
tags:
- SDN
- data center
- virtualization
- high availability
title: Can You Afford to Reformat Your Data Center?
url: /2015/11/can-you-afford-to-reformat-your-data/
---
I love listening to the Datanauts podcast (Ethan and Chris are fantastic hosts), starting from the [very first episode](http://packetpushers.net/podcast/podcasts/datanauts-001-hyper-convergence-with-scott-d-lowe/) (hyper-converged infrastructure) in which Chris made a very valid comment along the lines of "*with the hyper-converged infrastructure it's possible to get so many things done without knowing too much about any individual thing...*" and I immediately thought "*... and what happens when it fails?*"
<!--more-->
### It Looks Easier and Easier

The ever-simpler GUI and wizards that come with well-executed hyper-converged offerings allow typical data center administrator (one would expect a single person to work with compute, storage and network in a hyper-converged world) to set up and operate a reasonably-sized data center without knowing much about anything -- like in every other IT discipline the [knowledge-versus-complexity](/2012/03/knowledge-and-complexity/) curve looks more and more like the hockey stick.

![](/2015/11/s500-Knowledge-Complexity-Hockey-Stick.png)

However, the simplistic façade hides ever-increasing pile of complexity, and because a typical administrator never had to build the skills necessary to master it (including the troubleshooting skills), he has absolutely no chance of fixing things when they break beyond the simple alarms displayed by the GUI, and often the VAR- or vendor support engineers fare no better.

![](/2015/11/s500-Knowledge-Complexity-Dragons.png)

### It's Not Just the Hyperconverged Infrastructure

Cisco ACI seems to offer similar experience -- it's extremely easy to operate (and hope it doesn't break) once it's set up. This is the feedback I got from one of the network architects testing the product:

> Other than assigning a BGP ASN (which has no real world meaning in BGP peering), ACI really isn\'t networking. They made a point several times to explain that you still need networking experts who understand the underlying flows for troubleshooting and such - and I agree with that - but when I stop viewing this like a network architect and start viewing it like a CIO, I could have a staff of entry-level folks learn menus and dropdowns run the whole thing after it\'s set up. As long as the Security team approves what is in the Policies (Contracts) between the EPGs, the rest of it can be automated anyway.

### It's the Same All over the Place

Data centers are obviously not the only area facing this problem. We stopped fixing PCs, laptops, or tablets long ago. It's easier to reformat them or replace them with a shinier model.

I've seen the same unfortunate trend in many other industries. A few years back my car's engine developed crazy hiccups that were impossible to diagnose using the standard diagnostic tools, and an army of mechanics worked on the problem for weeks futilely trying to replace one component after another... until an old grunt decided to ignore the automated diagnostics, started looking at the schematics and the measurement points, and identified a leaky air pipe.

The whole process looked exactly like the TAC engineers telling you to reload the box or upgrade the software without even trying to identify the root cause of the problem.

### Can You Afford It?

It's easy to tell an unfortunate user he has to reformat the laptop (and hope the data restore process will work). You can afford to drive around in clunky replacement car for weeks while computer operators (formerly known as mechanics) try out random combinations of old and new components. Can you afford to go through the same experience with your data center?

**Summary:** Sooner or later you'll have to deal with a product that will behave like a black box (regardless of whether it's called *EVO:\*, hyperconverged infrastructure* or *SDN*), and unless I'm missing something, you have only two options: either (A) reduce the black box size to [acceptable unit of loss](http://kontrolissues.net/2015/03/27/sometimes-size-matters-im-sorry-but-youre-just-not-big-enough/) or (B) prepare for an all-out disaster with a good disaster recovery plan.

### Did I Mention Disaster Recovery?

We discussed various aspects of disaster recovery and active-active data centers in the [*Designing Active-Active and Disaster Recovery Data Centers*](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.
