---
kb_section: Layer3Fabrics
minimal_sidebar: true
title: Conclusions
url: /kb/Layer3Fabrics/50-conclusions/
---
Implementing resilient applications on top of redundant layer-3-only fabrics (without resorting to tricks like loopback interfaces on servers) is a hard problem that has been successfully solved only in niche domains like SS7 signaling or iSCSI fabrics.

Most application developers are unaware of the complexities involved in designing resilient applications[^1], resulting in applications that expect to connect to a single IP address per service[^7], pushing the problems down to the network layer where they are usually solved in one of these ways:

* Single IP subnet stretched across multiple top-of-rack switches to support server IP addresses floating across multiple redundant uplinks;
* Multi-chassis link aggregation (MLAG), connecting a server to multiple top-of-rack switches while pretending to bundle the redundant server uplinks into a single Ethernet link;
* Running routing protocols on servers and advertising loopback IP address as the service endpoint;
* Using load balancers in front of servers to make application service available on a single virtual IP address. 

While it's easy to blame application developers for the sad state of resilient application architectures, we should keep in mind that:

* TCP/IP protocol stack design is broken as it lacks a session layer[^2];
* Socket API is broken[^3] as it requires the application to specify the transport protocol (example: TCP). SCTP adoption would be much higher if it wouldn't require application rewrites;
* Solutions like happy eyeballs[^4] are kludges that solve "_what IP address should I connect to_" challenge, but not "_how do I recover from failures_" one;
* Virtualization vendors like VMware never really understood networking challenges as amply demonstrated by their recommended designs that heavily rely on stretched VLANs or MLAG[^5];
* There is no off-the-shelf library (apart from some Happy Eyeballs implementations[^6]) that application developers could use to develop resilient applications.

[^1]: [Moving Complexity to Application Layer?](https://blog.ipspace.net/2017/12/moving-complexity-to-application-layer.html)

[^7]: [Saved: TCP Is the Most Expensive Part of Your Data Center](https://blog.ipspace.net/2019/10/saved-tcp-is-most-expensive-part-of.html)

[^2]: [What went wrong: TCP/IP lacks a session layer](https://blog.ipspace.net/2009/08/what-went-wrong-tcpip-lacks-session.html)

[^3]: [What went wrong: the Socket API](https://blog.ipspace.net/2009/08/what-went-wrong-socket-api.html)

[^4]: [Happy Eyeballs – Happiness Defined by Your Perspective](https://blog.ipspace.net/2013/03/happy-eyeballs-happiness-defined-by.html)

[^5]: [Do We Need Complex Data Center Switches for VMware NSX Underlay](https://blog.ipspace.net/2020/02/do-we-need-complex-data-center-switches.html)

[^6]: [Happy Eyeballs v2 (and how I Was Wrong Again)](https://blog.ipspace.net/2018/05/happy-eyeballs-v2-and-how-i-was-wrong.html)



