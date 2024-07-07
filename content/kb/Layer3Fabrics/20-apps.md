---
kb_section: Layer3Fabrics
minimal_sidebar: true
title: Applications Using Multiple IP Addresses
url: /kb/Layer3Fabrics/20-apps/
---
The optimal approach to any distributed systems challenge is to solve the complex problems at the edge[^1], and using the network core as a simple transport mechanism.

We could use this approach to build simple layer-3-only transport fabrics, and solve the redudancy issues within the end-hosts:

* IP subnet assignments closely follow the physical network topology. The size of layer-2 domains is kept to a minimum;
* The network provides a unique IP address to every endpoint network interface (uplink);
* Multiple IP addresses assigned to redundantly connected endpoints (hosts/servers) could belong to different subnets;
* Clients running on redundantly connected endpoints can use multiple IP addresses, potentially establishing multiple sessions (one per interface) with the same server and distributing requests across all the sessions;
* Service endpoints are available on multiple (server) IP addresses and the clients try to connect to every service endpoint until a successful connection is established.

{{<figure src="/kb/Layer3Fabrics/Redundant-App-Sessions.png" caption="Redundant client-server application sessions established across multiple subnets">}}

Well-known solutions using this approach include:

* SCTP transport protocol[^2] that is unfortunately rarely used[^3], for example, in SS7 signaling.
* Multipath TCP[^4] that allows a client TCP stack to open multiple TCP sessions to the same server and use them concurrently (including load balancing) while giving the appearance of a single TCP session to the application[^5].

{{<note info>}}Multipath TCP allows the client to use multiple IP addresses, but does not address the problem of service being available on multiple IP addresses.{{</note>}}

* Multipath I/O in iSCSI implementations that allows the servers to use all uplinks for storage traffic[^6].

Very few other solutions, applications or products can use the same approach due to challenges faced when implementing this approach on commonly deployed TCP/IP stacks.

[^1]: [Host-to-Network Multihoming Kludges](https://blog.ipspace.net/2016/04/host-to-network-multihoming-kludges.html)

[^2]: [Stream Control Transmission Protocol](https://en.wikipedia.org/wiki/Stream\_Control\_Transmission\_Protocol) (Wikipedia)

[^3]: [What Went Wrong: SCTP](https://blog.ipspace.net/2009/08/what-went-wrong-sctp.html)

[^4]: [Multipath TCP](https://en.wikipedia.org/wiki/Multipath\_TCP) (Wikipedia)

[^5]: [iOS Uses Multipath TCP; Does It Matter?](https://blog.ipspace.net/2014/03/ios-uses-multipath-tcp-does-it-matter.html)

[^6]: [Load Balancing Elephant Storage Flows](http://blog.ipspace.net/2015/01/load-balancing-elephant-storage-flows.html)
