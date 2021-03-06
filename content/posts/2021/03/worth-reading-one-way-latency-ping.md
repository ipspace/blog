---
title: "Worth Reading: Splitting the Ping"
date: 2021-03-21 08:06:00
tags: [ network management ]
---
I hope you're aware that the venerable **ping** (and most of its variants) measures *round-trip-time* -- how long it takes to get to the destination *and back* -- but is there a way to measure one-way latency or find out asymmetric transit times? 

Ben Cox found a way to use ICMP timestamps together with reasonably accurate NTP-derived time to do just that. More details in [Splitting the ping](https://blog.benjojo.co.uk/post/ping-with-loss-latency-split) (HT: Drew Conry-Murray).

