---
date: 2014-03-03 07:06:00+01:00
multihoming_tag: session
series:
- multihoming
tags:
- what went wrong
- Internet
- load balancing
title: iOS uses Multipath TCP – Does It Matter?
url: /2014/03/ios-uses-multipath-tcp-does-it-matter.html
---
When Apple launched the new release of iOS last autumn, networking gurus realized [the new iOS uses MP-TCP](http://appleinsider.com/articles/13/09/20/apple-found-to-be-using-advanced-multipath-tcp-networking-in-ios-7), a recent development that allows a single TCP socket (as presented to the higher layers of the application stack) to use multiple parallel TCP sessions. Does that mean we're [getting closer to fixing the TCP/IP stack](https://blog.ipspace.net/2010/07/tcpip-is-like-mainframe-you-cant-change.html)?

TL&DR summary: Unfortunately not.
<!--more-->
### Why Is MP-TCP Interesting?

**Use case #1 -- mobile networks**: Mobile devices are often connected to WiFi and mobile (3G/4G) networks concurrently, but cannot use both connections simultaneously for the same data transfer -- a TCP session is limited to a single set of IP endpoints, and since you cannot share an IP address between 3G and WiFi interface, a single TCP session cannot use both links (at least not in the inbound direction).

**Use case #2 -- data centers**: Modern data center fabrics are commonly using highly parallel Clos fabric architecture. There might be tens of alternate paths between any two servers ... and yet the servers cannot use more than one of them for a single TCP session due to 5-tuple load balancing restrictions ([Brocade fares a bit better](https://blog.ipspace.net/2011/04/brocade-vcs-fabric-has-almost-perfect.html)).

### How Does MP-TCP Solve These Problems?

[MP-TCP](http://tools.ietf.org/html/rfc6824) introduces a shim layer between the TCP's application-facing API ([socket API in most cases](https://blog.ipspace.net/2009/08/what-went-wrong-socket-api.html)) and the traditional TCP stack. The shim layer establishes multiple traditional TCP sessions between the client's and server's IP endpoints, and multiplexes data of a single application session across them.

Multiple TCP sessions below the MP-TCP shim layer allow a mobile device to use all its interfaces to transfer data of a single application session (this is why Apple implemented it). [Servers can use multiple TCP sessions to get more bandwidth](http://multipath-tcp.org/pmwiki.php?n=Main.50Gbps) or access to less loaded alternate paths -- new TCP sessions using different source and destination TCP port numbers might be placed on a different set of ECMP paths.

### Will MP-TCP Fix the TCP Stack?

No. A typical application still has to use [*getaddrinfo*](http://linux.die.net/man/3/getaddrinfo) calls to get a list of IP addresses for a given host name, and try to connect to one of them (sequentially or [somewhat more intelligently](https://blog.ipspace.net/2013/03/happy-eyeballs-happiness-defined-by.html)). A server (or service) must thus still be [exposed as a single IP address](http://blog.ipspace.net/2009/08/what-went-wrong-tcpip-lacks-session.html); MP-TCP will not remove the need for Application Delivery Controllers (known as load balancers outside of marketing departments) or traditional multi-homing.
