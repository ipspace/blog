---
title: "Deploying Plug-and-Pray Software in Large-Scale Networks"
# date: 2021-03-22 16:29:00
tags: [ IP routing ]
draft: True
intro: |
  A story of how Chromium service discovery breaks large network with IP multicast enabled
---
The last couple of weeks found me helping a customer trying to find 
and resolve a very hard to find "network performance" issue. In the 
end it turned out to be a combination of ill conceived application 
nonsense and a setup with a too large blast radius/failure domain/fate 
sharing. The latter most probably based upon very valid decisions in 
the past (business needs, uniformity of configuration and management). 
Not very wise in the long run, and yes there's tons of useful material 
-like that- I can come up with after the efforts we went through the 
last couple of weeks, both technical, as well as a lot of struggling 
with procedures, communication, management involvement, etc. 

However, one thing that seriously irks me is that once again we got 
stung by someone at Google and Microsoft deciding to keep using a 
badly designed protocol for service discovery (SSDP). Not only will 
Microsoft Windows enable it by default, all Chromium engine based 
browsers, including Edge, will send a lot of join/leave aka discovery 
messages via SSDP. Multiply this by 30000 and you end up with a real 
problem. Even putting aside all the serious security issues with SSDP 
and amplication risks: why ? Find your Chromecast is fine within a 
small home LAN, deciding that multicast is a great way to be able to 
span (V)LANs at a larger scale is dumb (again). 
Why do we keep ending up with solutions like this ? Keep it simple for 
simple use cases, have people put some thought into deploying 
something at scale. After all, this is what Microsoft and Google 
undoubtedly do within their own (cloud) infrastructure. And suprise, 
suprise, multicast in the public cloud..... 
Service discovery at scale should be solved in a robust way, at the 
application level. 
Using the network at the application level (Edge) is not the same. 

Luckily I've passed through the very grumpy phase already and have 
prompted the customer to see this as an opportunity to accelerate 
existing plans. 

---

> Do I get it right that you had a flat network with way too many 
> nodes on it, and chatty hosts using IP multicast for service 
> discovery didn’t make the situation any better? 

Not in a strict L2 sense, but with regard to failure domain/blast zone/fate sharing wise it kinda is: a classic N7K(L3 core) <--> N5K(L2 access) campus with a L3 connection to the data center (N5K6 fabricpath). 

Somewhere in the murky past it was deemed necessary to 
enable multicast routing. All I could gather now that it was probably something to do with deploying workstations and a couple of medical  appliances. The number of mroutes or amount of traffic isn't impressive, but the burden of frequent SSDP join/leave messages where causing the troubles. 

The irony (well not in the strict sense, but you get my drift) is that besides helping them with automation I co-wrote a roadmap with a focus on reducing blast zones/failure domains, i.e. zoning the network. 

Which was/is a whole other story with plenty of battles of it's own (don't you love enterprise IT). In a sense the whole situation is a wonderful demonstration of why we want to implement zero trust, micro segmented architecture :-/ 

