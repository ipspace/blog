---
kb_section: NTP
minimal_sidebar: true
title: Summary
url: /kb/Internet/NTP/60-summary/
---
Having accurate time on the network devices is very important if you use public key infrastructure (where the time is needed to check the certificate validity) or if you want to perform a distributed analysis of a security incident or a routing problem.

Cisco IOS devices (router and switches) can be configured to use the Network Time Protocol (NTP) to synchronize with a reliable time source. They can also act as NTP servers allowing you to build a hierarchical time synchronization infrastructure. Any NTP client can synchronize with a router providing NTP services; you can thus minimize the impact of workstations’ time synchronization from remote sites and increase the time accuracy on these sites by providing the time services locally.

Low-end routers that do not support NTP can be configured to use SNTP (a stripped-down version of NTP that provides only the basic client functionality). SNTP client can also be configured on some mid-range routers (even if they support NTP) in the recent IOS releases.

### More to Explore

* MUST READ: [The NTP Bible](https://weberblog.net/ntp/) by [Johannes Weber](https://weberblog.net/about/)
* [NTP v3 (RFC 1305)](https://datatracker.ietf.org/doc/html/rfc1305)
* [NTP v4 (RFC 5905)](https://datatracker.ietf.org/doc/html/rfc5905)
* [Simple Network Time Protocol (RFC 4330)](https://datatracker.ietf.org/doc/html/rfc4330) (obsoleted by NTPv4)
* [Logging to a local file system](http://blog.ipspace.net/2007/09/logging-to-flash-disk.html)
* [Pros and cons of using NTP logging](/2007/10/log-ntp-events/) (read the comments)
* [More NTP-related hints](/tag/ntp/)
