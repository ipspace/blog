---
title: "DHCP Relaying on a Linux Host"
date: 2024-02-28 11:02:00
tags: [ DHCP ]
draft: True
---
Btw, when writing the blog posts I was first using VyOS, but it uses the ISC DHCP relay, and it relays also unicast packets. The DHCP procedures work still eventually fine, but getting sensible outputs and explanations was a nightmare, the posts were heavily turning into disclaimers and notes and warnings... so I used CSR1kv instead, it only relays the broadcast packets as expected. I don't know if you found similar unicast relay cases in your testing.
<!--more-->
---

- sudo sysctl net.ipv4.ip_forward=1

I might have forgotten to turn this on (have to check what the defaults are)
- /etc/default/isc-dhcp-relay: OPTIONS="-iu ens224 -id ens256", SERVERS=“10.0.41.10”

Will try to use upstream/downstream interfaces
So, here it works the same with isc-dhcp-relay on Debian and VyOS 1.4-rolling

I'm running Ubuntu, so that might explain the difference.

---

So:

-   I reproduced the behavior. I used Cisco IOSv as the DHCP client because it creates very predictable traffic every time you execute **renew dhcp **command, and dnsmasq as the DHCP server because I managed to pilfer a working configuration from another example.
-   As you observed, the DHCP relay goes bonkers if you don’t specify upstream/downstream interfaces. I have a weird feeling that only happens with unicast packets (need to go deeper into the woods).
-   Things work as they “should” if the IP forwarding is turned off (and the upstream/downstream interfaces are configured correctly).
-   dnsmasq DHCP server politely ignores the request coming from the “wrong” giaddr if that subnet is not configured, or tells the relay agent to get lost otherwise.

Anyway, it seems to me that the intended use case for dhcrelay is something like a bastion host relaying DHCP requests to a server in the management network, or a Linux host in parallel with a router. I have to test it, but it could be that even a one-arm mode would work. 

It would be nice if the above paragraph would be documented somewhere, but one should not complain about open-source gifts, right?

What I couldn’t figure out is how the dhcrelay intercepts packets that should clearly be forwarded, unless it uses interface tapping.

Blog post coming in September, I’m shutting down for the summer. I’ll probably write it in the next few days though, otherwise I’ll spend way too much time recreating the short-term memory.
