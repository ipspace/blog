---
title: "Deploying Plug-and-Pray Software in Large-Scale Networks"
tags: [ IP routing ]
date: 2021-06-16 07:45:00
lastmod: 2021-06-18 15:46:00
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

Unfortunately, this is not the only _Service Discovery is breaking my network_ scenario. [Erik Auerswald](https://www.unix-ag.uni-kl.de/~auerswal/) sent me this one:

---

This interesting phenomenon came to light because of really large layer-2 domain combined with the fact that the switches the customer used sent every link-local multicast packet (groups in 224.0.0.0/24) to the CPU. 

After changing the configuration of the wireless access points used by the customer, the switch CPU utilization would be a constant 100% for about an hour or two, observable in the NMS. No networking problem was detectable during those high CPU usage times, but it would generate alarms and might interfere negatively with troubleshooting network problems. 

Here's what was going on: 

* The APs performed a reboot to apply new configuration.
* After booting, they started sending MDNS (224.0.0.251) and LLMNR (224.0.0.252) requests. 
* Lots of end-systems would answer, because of the large layer-2 two domain, and use of common end-system operating systems.
* The APs seemed to ignore the answers, and queried again, according to the retry mechanisms of MDNS and LLMNR.
* The end-systems would answer those queries as well, the answer seemed to be ignored, additional queries generated and on and on and on.

All those link-local multicast packets were sent to the switch CPUs, processed, and ignored. This kept the CPU load at 100% for quite some time. 

The amount of MDNS & LLMNR messages per second eventually decreased, because the APs seemed to follow the exponential backoff algorithm specified for those protocols, so that they would "retry" once per hour, which did not result in switch CPU usage spikes noticeable in the NMS software (couple of minutes polling interval). 

The implemented workaround was to stop the multicast packets from reaching the CPU via ACL (or [control plane] policy or whatever you may want to call it) without restricting forwarding of those packets. 

To close the loop to SSDP: the APs did send SSDP queries as well, but since those are not link-local (239.255.255.250), they were not processed by the CPU (IGMP snooping was implemented by the switch ASIC). Thus I did not need to do anything about them. 

The customer, of course, did not know if MDNS, LLMNR, and SSDP were actually needed by the end-systems. 

Since MDNS & LLMNR use link-local multicast groups, they are not flooded over all of a routed multicast domain, thus they usually do not create problems there, opposed to SSDP. 

---

### Revision History

2021-06-18
: Added another SSDP / MDNS / LLMNR example by Erik Auerswald