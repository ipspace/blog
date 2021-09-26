---
title: "Watch Out: ISR Performance License"
date: 2021-09-29 07:03:00
tags: [ performance ]
---
Bill Dagy sent me an annoying ISR gotcha. In his own words: 

> Since you have a large audience I thought I would throw this out here. Maybe it will help someone avoid spending 80 man hours troubleshooting network slowdowns.

Here's the root cause of that behavior:

> Cisco is now shipping routers that have some specified maximum throughput, but you have to buy a "boost license" to run them unthrottled. Maybe everyone already knew this but it sure took us by surprise.

Don't believe it? Here's a snapshot from [Cisco 4000 Family Integrated Services Router Data Sheet](https://www.cisco.com/c/en/us/products/collateral/routers/4000-series-integrated-services-routers-isr/data_sheet-c78-732542.html):
<!--more-->
{{<figure src="/2021/09/ISR-performance.png" caption="Cisco 4000 ISR performance licenses">}}

It's also worth noting that the *boost license* throughput applies only to onboard Gigabit Ethernet interfaces, and that the ISR 4461 has two onboard 10GE ports, and a maximum throughput of *over 7 Gbps* (one has to wonder whether that's with [IMIX](https://en.wikipedia.org/wiki/Internet_Mix) or maximum-MTU packets).

Have you encountered any other gotchas? Please write a comment!
