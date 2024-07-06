---
date: 2009-11-10 07:28:00.009000+01:00
tags:
- QoS
title: 'Solution: Bandwidth+Police actions in CB-WFQ'
url: /2009/11/summary-bandwidthpolice-actions-in-cb.html
---
Most of the respondents to my [last week's challenge](/2009/11/challenge-cb-wfq-bandwidthpolice.html) got it almost right. The minor (common) error was the assumption that **police rate percent 50** would result in a TCP session getting 50% of the bandwidth. Eyal got that right: the TCP throughput is always significantly lower than that due to frequent drops caused by low burst sizes assumed by the **police** command and resulting TCP restarts (the most I was able to push through was around 90 kbps; half of the bandwidth would be 128 kbps).
<!--more-->
Many respondents got the third case (**bandwidth** class, **police** class and **default-class** all active at the same time) wrong. Vaidotas was guessing in the right direction and Petr knows the correct answer, but did not want to spoil the fun. Here's the surprising result: the **bandwidth** class gets almost all the bandwidth. Sometimes the TCP sessions in other classes wouldn't even start.

To understand that behavior, we'd need to go deep into the bowels of Weighted Fair Queuing. Topic for another blog post... in the meantime I found an [old article by Petr Lapukhov](https://web.archive.org/web/20150219073651/http://blog.internetworkexpert.com/2008/08/17/insights-on-cbwfq/) on Internet Archive.

### Recommendation

If a single class in an outbound **service-policy** uses the **bandwidth** action, all the other classes should use the **bandwidth** action as well. The classes without the **bandwidth** action and the default class might get starved during congestions.
