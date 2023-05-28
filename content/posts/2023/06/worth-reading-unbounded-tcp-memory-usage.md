---
title: "Worth Reading: Unbounded TCP Memory Usage"
date: 2023-06-03 06:23:00
tags: [ worth reading, TCP ]
---
Another phenomenal detective story published on Cloudflare blog: 
[Unbounded memory usage by TCP for receive buffers, and how we fixed it](https://blog.cloudflare.com/unbounded-memory-usage-by-tcp-for-receive-buffers-and-how-we-fixed-it/).

**TL&DR:** Moving TCP window every time you acknowledge a segment doesn't work well with scaled window sizes.

The interesting takeaways:
<!--more-->
* People are still finding quirks in TCP
* It takes an enormous amount of data to find the anomalies, and tons of experimentation to get to the root cause
* The solution was explicitly documented in an RFC mandating it MUST be supported, it's just that Linux didn't use it.
* Fixing such anomalies is unrewarding hard work, unless you're working in an environment where due to its scale rare anomalies cost tons of money.

**Corollary:** Expect people to pursue an easier path to glory: invent another solution-in-search-of-a-problem while preaching how broken networking is.
