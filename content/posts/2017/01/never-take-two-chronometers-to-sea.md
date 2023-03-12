---
date: 2017-01-23 08:24:00+01:00
ha-cluster_tag: overview
high-availability_tag: ignore
series:
- ha-cluster
tags:
- design
- firewall
- data center
- high availability
title: Never Take Two Chronometers to Sea
url: /2017/01/never-take-two-chronometers-to-sea.html
---
One of the quotes I found in the [Mythical Man-Month](https://blog.ipspace.net/2017/01/worth-reading-mythical-man-month.html) came from the pre-GPS days: "*never go to sea with two chronometers, take one or three*", and it's amazing the networking industry (and a few others) never got the message.
<!--more-->
### Wait, What?

If you're not a naval history buff, you probably have no idea what I'm talking about, so here's the TL&DR version:

**What is a chronometer?** The [mechanic version of Stratum 0 NTP server](https://en.wikipedia.org/wiki/Marine_chronometer) ;) -- a very precise clock.

**Why did they need it?** It's relatively easy to measure latitude while on open seas. It's [really hard to measure longitude](https://en.wikipedia.org/wiki/History_of_longitude), and the marine chronometers were the best (although expensive) solution.

{{<note info>}}[Lunar distance navigation](https://en.wikipedia.org/wiki/Lunar_distance_(navigation)) is a must-read for true geeks ;){{</note>}}

**Why should you take three?** Two things can go wrong with a chronometer: it can fail or it can be imprecise. If you have two chronometers, it's impossible to figure out which one is imprecise and should be disregarded. You might decide to use one as primary and the other one as backup based on whatever criteria, but then you're acting as the third party (witness) in this protocol.

If you have three, you take the average time of the two that are closer together.

**Long story short**: it's impossible to get a reliable high-availability solution with two components (or even number of components).

### Why Is This Relevant?

Have you ever deployed redundant firewalls or load balancers? How many nodes are in a typical cluster? Got my point?

How about data center switches [implementing MLAG](/series/mlag.html)? Or stackable switches like HP IRF or Juniper Virtual Chassis that support at most 4 or 10 nodes (depending on the model)?

There's a good reason the server clustering solutions with two nodes use a disk as a witness. Networking industry obviously never got the memo, the obvious exceptions being VMware NSX controller (because it was designed by people who actually understood voting protocols) and Cisco ACI controller.

### Meh, You're Just Spreading FUD

Sure. I've seen enough real-life failures to [believe in simpler solutions](https://blog.ipspace.net/2016/11/reliability-of-clustered-solutions.html), but of course you shouldn't trust anything you read in a blog post. For a long list of split-brain failures from production environments, read [this ACM queue article](http://queue.acm.org/detail.cfm?id=2655736). Enjoy!
