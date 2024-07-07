---
date: 2013-09-17 07:22:00+02:00
tags:
- network management
- cloud
- web
title: Monitor Public SaaS Providers with ThousandEyes
url: /2013/09/monitor-public-saas-providers-with/
---
If you've ever tried to troubleshoot web application performance issues, you've probably seen it all -- browser waterfall diagrams, visual traceroute tools, network topologies produced by network management systems ... but I haven't seen them packaged in a comprehensive, easy-to-use and visually compelling package before. Welcome to [ThousandEyes](http://www.thousandeyes.com).
<!--more-->
### What is it?

**Short summary**: cloud-based application performance monitoring system. Nothing new.

Here's an elevator pitch summary of how it all works:

-   Create an account on their web site;
-   Deploy their agent software on Linux servers (or download mini VM in OVA format) at your sites;
-   Configure URLs you want to monitor;
-   Agents start periodic application-level probes (TCP or HTTP(S) probes) combined with smart traceroute (using TCP instead of ICMP to get the same treatment as the actual traffic). Web probes use Chrome browser for their timing, so you get HTTP connection time as well as DOM ready time (at which point the JavaScript code usually starts running) and total page load time (including all the graphics).
-   Agents report their results to ThousandEyes cloud-based servers, which alert you when the agents experience performance problems;
-   The agent reports are combined with public BGP feeds (example: RIPE feeds) to create a visual representation of the state of the global Internet at the time the agent(s) encountered performance problems, allowing you to identify the true root cause of the problem.

Sounds boring, right? We've been doing all this one way or another. You have to test the product or watch NDF6 videos to grasp the true magic of ThousandEyes. Here are the videos (watch all of them, these guys weren't boring):

-   [Introduction](http://www.youtube.com/watch?v=M4TQz5AqkS4&list=PLObjX_zORJMCT_E1iKhvw1FzSr2hQnaY-&index=7)
-   [Product overview](http://www.youtube.com/watch?v=8qteZDYpYpg&list=PLObjX_zORJMCT_E1iKhvw1FzSr2hQnaY-&index=8)
-   [Technology deep dive](http://www.youtube.com/watch?v=3Np_AW_K4Ok&list=PLObjX_zORJMCT_E1iKhvw1FzSr2hQnaY-&index=9) (must-see)
-   [Use cases: SaaS provides and financial institutions](http://www.youtube.com/watch?v=MK8CvrGp7ts&list=PLObjX_zORJMCT_E1iKhvw1FzSr2hQnaY-&index=10) (cool use cases!)
-   [Enterprise use cases](http://www.youtube.com/watch?v=y_XsRuGRCIs&list=PLObjX_zORJMCT_E1iKhvw1FzSr2hQnaY-&index=11)

### And now for the crazy ideas

We've been mentioning several obvious ideas (monitor internal web servers) and a few crazy ones when talking with ThousandEyes during NFD6 (so go watch the videos). Most of them would require additional functionality, so if you find them interesting (and you're big enough), go talk with ThousandEyes and push them in this direction.

-   Package ThousandEyes server as an appliance that could be deployed within a security-conscious enterprise environment. One of the major hurdles we experienced when deploying a similar solutions was the interaction between internal probes and our management system -- every decent CISO gets upset initially.
-   Interact with internal BGP routing to get BGP-based visibility into internal network as well as global Internet.
-   It would be really cool if they could (somehow) import data from your xVPN-over-Internet configurations to get the transport endpoints and then map those into their BGP-based visualization to give you true hop-by-hop path analysis.
-   Implement an automatic baselining system. You can configure absolute HTTP connection and page load timeouts, but it would be great to be able to get reasonable thresholds (per agent location) automatically.

### Would I use them?

Absolutely. If you're a business heavily relying on SaaS products (Salesforce, Dropbox, Google Docs, Gmail ...) something like ThousandEyes is a must-have. Even if you can't do a thing when an ISP two hops down the road scrambles their BGP configs, you'll have at least an insurance policy when unhappy users start shouting at you ... and a plausible reason why it might be a good idea to switch ISPs and pay someone else a bit more for a more reliable service.

### Disclosure

ThousandEyes was a sponsor of Networking Tech Field Day 6 and so indirectly covered some of my travel expenses.
