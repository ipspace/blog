---
title: "Deploying Plug-and-Pray Software in Large-Scale Networks"
tags: [ IP routing ]
date: 2021-06-16 07:45:00
---
One of my readers sent me a sad story describing how Chromium service discovery broke a large multicast-enabled network.

---

The last couple of weeks found me helping a customer trying to find and resolve a very hard to find "network performance" issue. In the end it turned out to be a combination of ill conceived application nonsense and a setup with a too large blast radius/failure domain/fate sharing. The latter most probably based upon very valid decisions in the past (business needs, uniformity of configuration and management). 
<!--more-->
Somewhere in the murky past it was deemed necessary to 
enable multicast routing. All I could gather was that it probably had something to do with deploying proprietary appliances. The number of mroutes or amount of traffic isn't impressive, but when you add the burden of frequent SSDP join/leave messages, you quickly get into trouble.

However, one thing that seriously irks me is that once again we got stung by someone at Google and Microsoft deciding to keep using a badly designed protocol for service discovery (SSDP). Not only will Microsoft Windows enable it by default, all Chromium engine based browsers, including Edge, will send a lot of join/leave aka discovery messages via SSDP. Multiply this by 30000 and you end up with a real problem. Even putting aside all the serious security issues with SSDP and amplication risks, one has to ask _WHY?_ Find your Chromecast is fine within a 
small home LAN, deciding that multicast is a great way to be able to span (V)LANs at a larger scale is dumb (again). 

Why do we keep ending up with solutions like this? Keep it simple for simple use cases, and have people put some thought into deploying something at scale. After all, this is what Microsoft and Google undoubtedly do within their own (cloud) infrastructure. Service discovery at scale should be solved in a robust way, at the application level. Using the network at the application level (Edge) is not the same. 

Luckily I've passed through the very grumpy phase already and have prompted the customer to see this as an opportunity to accelerate existing plans. 

---

For whatever reason, this story reminds me of a handset OS vendor who refuses to implement DHCPv6 because *they know better*. Who cares about doing the right thing when we can persuade the users of our gadgets that it's the infrastructure teams' fault no matter what.