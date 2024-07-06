---
date: 2012-10-12 07:02:00+02:00
high-availability_tag: fail
series_weight: 500
tags:
- data center
- high availability
title: If Something Can Fail, It Will
url: /2012/10/if-something-can-fail-it-will.html
---
During a recent consulting engagement I had an interesting conversation with an application developer that couldn't understand why a fully redundant data center interconnect cannot guarantee 100% availability.
<!--more-->
### Background

The customer had a picture-perfect design: layer-3 data center interconnect with two core routers per data center and two inter-DC links from different carriers (supposedly exiting the buildings at different corners and using different paths) \... and yet we were telling the application developers they shouldn't deploy mission-critical services with components spread over both data centers. Mindboggling, isn't it?

{{<figure src="/2012/10/s400-RedundantDCI.png" caption="Fully redundant data center design">}}

### The Problem

What could possibly go wrong with a fully redundant design?

Every component you\'re using has a non-zero failure rate; the probability of redundant components failing at the same time is thus non-zero. However, assuming each component is reasonably reliable (let's say it has 99.9% uptime), the probability of a total failure should be extremely low, right? Wrong. Interconnected things tend to fail at the same time.

An obvious example first: if the software of the core router happens to be susceptible to a killer packet (that causes it to reload), the second core router will probably get the same packet (due to retransmissions) a moment after the first one crashes (see also: [BGP bugs](/2009/02/root-cause-analysis-oversized-as-paths.html))

A slightly less obvious example: almost everyone is using the same maintenance windows. A telco team could start working on one of your links while you're upgrading the router that uses the other link (Yes, we've experienced that. Yes, they forgot to tell us they'd do maintenance, because everything was supposed to be fully redundant anyway).

The application developer still couldn't believe me, so I told him another true story.

> A while ago we were notified that our data center would lose power for two hours due to planned maintenance. No problem, the building we're in has a diesel generator, and we have plenty of UPS capacity. However, once the power was cut at 3AM, the diesel generator failed to start... and it's somewhat impossible to find someone to fix it in the middle of the night. Fortunately we had plenty of time to perform a controlled shutdown, but an hour later our data center was dead, even though we had triple redundancy.

The application developer's response: "Ah, now I get it." After that, it was pretty easy to agree on what needs to be done to make their data centers and services truly robust.
