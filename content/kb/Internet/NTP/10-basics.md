---
kb_section: NTP
minimal_sidebar: true
title: NTP Basics
url: /kb/Internet/NTP/10-basics/
---
The Network Time Protocol (NTP, [RFC 1305](http://tools.ietf.org/html/rfc1305)) is a simple protocol using UDP port 123. The RFC describes the protocol itself as well as the architectural framework and in-depth implementation recommendations.

The NTP architectural framework specifies a hierarchy of time servers using *stratum* values from one to sixteen to indicate their relative accuracy. The most accurate servers using external clocks (GPS receivers are commonly used due to their low cost) are *stratum one* servers and any server synchronizing itself to a *stratum X* server advertises itself as *stratum X+1* server.

Two NTP servers communicate in client-server or peer-to-peer mode (the desired peering mode is configured manually on the servers and indicated in the outgoing NTP packets). The fundamental difference is the synchronization behavior: an NTP server can synchronize to a peer with better stratum, whereas it will never synchronize to its client (regardless of the client’s stratum).

The upstream NTP *servers* have to be defined manually in the *client* NTP server (or the NTP client); there is no auto-discovery mechanism in the client-server relationships. If you use NTP on the Cisco IOS, the NTP peers have to be defined only on one side; the IOS implementation of the NTP server automatically creates a peer-to-peer association when it receives an incoming NTP packet indicating the remote IP host wants to establish a peering relationship.

{{<note warn>}}This behavior is a potential threat in security-conscious environments that can easily lead to denial-of-service attacks. It’s thus highly recommended that you protect the IOS NTP servers with NTP authentication or access lists.{{</note>}}

NTP clients are no different from the NTP servers (from the protocol or implementation perspective). The typical NTP client implementations can synchronize to multiple NTP servers, select the best server and synchronize with it or even set the local clock to the averaged value returned by the servers.

Low-end time synchronization implementations (for example, Windows 2000) typically choose to use Simple Network Time Protocol (SNTP) [defined in RFC 4330](http://www3.tools.ietf.org/html/rfc4330). SNTP is a small subset of NTP. It interoperates with NTPv3 servers (there is no need to deploy another time synchronization infrastructure to use SNTP) but forgoes the complex time synchronization algorithms of RFC 1305 and replaces them with a simple stateless request-reply protocol, resulting in lower accuracy.

Some low-end Cisco routers support only SNTP client. Mid-range routers can be configured to use either NTP or SNTP. If you want to use a router as an NTP server, it has to synchronize with upstream routers via NTP; if you only need pretty accurate local time, SNTP is a good choice for remote locations.
