---
date: 2007-07-17 07:23:00+02:00
tags:
- security
title: Totally Stealthy Router
url: /2007/07/totally-stealthy-router/
---
In response to the post detailing router response to port scans, one of my readers asked an interesting question:

> "I was wondering if there was a way to prevent the router from sending those TCP RST packets administratively prohibited ICMP messages back to scanners for TCP and UDP respectively. I basically want my router to drop all packets period without replying back in any way, shape, form, or fashion."

Here\'s how you do it:
<!--more-->
-   No TCP RST packets should be sent as responses to port scans. Inbound access list dropping all IP packets achieves that.
-   Outbound traffic, both from the protected LAN as well as from the router itself (ping, telnet, DNS, NTP \...) should be allowed. Configure **ip inspect** with **router-traffic** option.
-   Disable generation of ICMP unreachables with the **no ip unreachables** interface configuration command.

The relevant parts of router configuration are included below:

```
ip inspect name Internet tcp router-traffic
ip inspect name Internet udp router-traffic
ip inspect name Internet icmp router-traffic
!
interface FastEthernet0/0
 ip address a.b.c.d x.y.z.w
 ip access-group Internet in
 no ip unreachables
 ip inspect Internet out
!
ip access-list extended Internet
 deny ip any any
```

**Notes:**

- The sample router configuration is taken from a SOHO router doing PAT on the public interface. You might have to adjust the *Internet* access-list to your needs.
- **ip inspect** functionality has been replaced by zone-based firewall feature.