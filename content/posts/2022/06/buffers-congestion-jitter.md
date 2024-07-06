---
title: "Repost: Buffers, Congestion, Jitter, and Shapers"
date: 2022-06-27 06:15:00
tags: [ switching, QoS ]
---
_[Béla Várkonyi](https://www.linkedin.com/in/belavarkonyi/) left a [great comment](/2022/06/beware-vendors-bringing-whitepapers.html#1309) on a blog post discussing (among other things) whether we need large buffers on spine switches. I don't know how many people read the comments; this one is too valuable to be lost somewhere below the fold_

---

You might want to add another consideration. If you have a lot of traffic aggregation even when the ingress and egress port are roughly at the same speed or when the egress port has more capacity, you could still have congestion. Then you have two strategies, buffer and suffer jitter and delay, or drop and hope that the upper layers will detect it and reduce the sending by shaping.
<!--more-->
But you are right, deep buffers mean high jitter that might be converted into high delay at some point by dejitter buffers. If you have a traffic pattern that is a kind of distribution into multiple directions, then you do not need to concern about congestion and deep buffers. Even if the distributing interfaces might have less speed but they still fit to the disaggregation patterns. For example, fast ethernet access ports and gigabit uplinks. There are many situations like that. As usual, an optimum network design requires the knowledge of your traffic patterns. Otherwise, you can just overdesign as much as allowed by your budgets.

It is also important to take into account the policer/shaper chaining rules. If you want to reduce congestion, then there must be a shaper at the sender for complying with the policer at the receiver. The physical capacity of the link is a natural policer, even if you have not configured a policer explicitly. Inside the router/switch you have a similar pairing, you just have to count with the aggregation factor, too.

Such a chain of shapers is very difficult to manage, so a backpressure mechanism edge-to-edge or end-to-end would be needed for the rescue. Unfortunately, some traffic does not have backpressure, such as certain UDP streams. Then you have a bad luck and either configure all the shapers based on a traffic patterns, or make a compromise by tolerating packet loss and jitter.

I have seen a lot of problems in networks when shapers were forgotten... You cannot make wonders, so you have to consider them...