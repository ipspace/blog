---
date: 2016-04-22 17:28:00+02:00
high-availability_tag: fail
series_weight: 400
tags:
- bridging
- data center
- WAN
- high availability
title: 'Some People Don’t Get It: It Will Eventually Fail'
url: /2016/04/some-people-dont-get-it-it-will/
---
Mark Baker left [this comment](/2015/11/stretched-firewalls-across-layer-3-dci/#c1267210791129657664) on my [*Stretched Firewalls across Layer-3 DCI*](/2015/11/stretched-firewalls-across-layer-3-dci/) blog post:

> Strange how inter-DC clustering failure is considered a certainty in this blog.

Call it experience or exposure to a larger dataset. Anything you build will [eventually fail](/2012/10/if-something-can-fail-it-will/); just because you haven't experienced the failure yet doesn't mean that the system will never fail but only that you were lucky so far.
<!--more-->
Let me use a trivial example from real world to illustrate the point. When I was a kid, we didn't use seat belts, because everyone knew that a traffic accident couldn't possibly happen to him (or his dad/mom). When I was a teenager, I was fortunate enough to use a seat belt (even though it wasn't common), or I wouldn't be writing this blog post.

The whole *stretched whatever* debate is really a question of *risk management* and balancing *convenience* (in Mark's case the management burden) against inevitable crash. The two real questions to consider are "*How often does that happen?*" and "*What happens after the failure?*" (or "*How much will a failure cost me?*").

Unfortunately, many people promoting next-big-thingy don't consider the risks involved and never go through the exercise of identifying all possible failure scenarios and their consequences, and all I'm trying to do is to point out that *there's non-zero risk* and that *the consequences could be fatal.*

However, once you went through the above exercise, and understand all the implications of what you're doing, go ahead and choose the option that makes most sense to you; we'll explore quite a few of them during the design sessions in the [Building Next-Generation Data Center online course](http://www.ipspace.net/Building_Next-Generation_Data_Center).
