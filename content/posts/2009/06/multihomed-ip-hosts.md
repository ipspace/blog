---
date: 2009-06-03 07:17:00.001000+02:00
lastmod: 2020-12-26 14:04:00
multihoming_tag: server
series:
- multihoming
tags:
- IP routing
- LAN
title: Multihomed IP Hosts
url: /2009/06/multihomed-ip-hosts/
---
IP host (workstations, servers or communication equipment) is *multihomed* if it has more than one IP address. An IP host can be multihomed in numerous ways, using one or more layer-3 interfaces for network connectivity. Some multihoming scenarios are well understood and commonly used, while others (multiple physical layer-3 interfaces in the same IP subnet) could be hard to implement on common operating systems.

{{<note>}}A host having a routable IP address on an external interface and on or more IP addresses on internal interfaces like the *loopback* interface is not considered multihomed.{{</note>}}
<!--more-->
### Multihoming Scenarios

[RFC 1122](https://tools.ietf.org/html/rfc1122) (Requirements for Internet Hosts) documents three multihoming scenarios:

-   **Multiple logical networks.** A host connected to a single layer-2 networks with multiple IP subnets may have an IP address in each subnet (*secondary IP addresses* in Cisco IOS terminology).

{{<figure src="/2009/06/MHIP_LogicalNetworks.png" caption="Multiple logical networks">}}

-   **Multiple logical hosts.** A host has multiple IP addresses in the same IP subnet. These IP addresses might be configured on the same or different layer-2 interfaces.

{{<figure src="/2009/06/MHIP_LogicalHosts_MultiIf.png" caption="Multiple logical hosts; two interfaces">}}

{{<figure src="/2009/06/MHIP_LogicalHosts.png" caption="Multiple logical hosts; single interface">}}

-   **Simple multihoming**. A host is connected to multiple layer-2 networks (and thus multiple IP subnets) and has one (or more, see *Multiple logical hosts*) IP address in each IP subnet.

{{<figure src="/2009/06/MHIP_Simple.png" caption="Simple IP host multihoming">}}

Multihomed IP hosts face two significant challenges:

-   **Session endpoint addressing**: which IP address is used as the source IP address in outgoing IP datagrams?
-   **Datagram forwarding**: which interface is used to send outbound IP datagrams?

These challenges are well documented in RFC 1122 (see also the discussion below). Some operating systems or add-on networking software (for example, stateful host firewalls) might impose additional limitations.

### Session Endpoint Addressing

A multihomed host could use any one of its IP addresses as the source IP address of outgoing IP datagrams carrying TCP or UDP packets. To ensure that the remote host is able to match its side of a TCP or UDP session with the received IP datagram, RFC 1122 imposes the following rules on IP address selection:

-   All segments in the same TCP session **must** use the same IP address (section 4.2.3.7, TCP multihoming).
-   A reply to an incoming UDP packet **should** use the same IP address to which the incoming UDP packet has been sent (section 4.1.3.5, UDP multihoming).
-   Application can specify the IP address of the first packet in a session if the session is initiated from the multihomed host.
-   If the application does not specify the IP address of the first packet in a TCP or UDP session, the TCP/UDP stack **must** ask IP layer to select the source IP address for the outgoing datagram. The source IP address is usually the IP address of the outgoing interface (section 3.3.4.3, Choosing a Source Address</a>).

A server running on a multihomed host should therefore use the destination IP address of the request packet as the source IP address of the reply packet. The IP address selection is automatic for TCP-based services (where the TCP stack enforces the correct IP address) and a UDP server should ensure the correct IP address is used in the reply packets.

On some operating systems, the client application on a multihomed host can specify the source IP address of the TCP or UDP session ([socket library example](http://mail.python.org/pipermail/python-list/2006-October/582995.html)).

### Datagram Forwarding

RFC 1122 documents datagram forwarding to local subnets and datagram forwarding to default gateways (it also allows hosts to use static routes), but does not address the interface selection rules when a multihomed host has multiple default gateways or multiple interfaces in the same IP subnet (*Multiple logical hosts*). These decisions are implementation dependent and many IP stacks use the first-match rule, sending majority of the outbound datagrams through a single interface.

Some operating systems (or add-on networking software) allow the administrator to define load sharing or policy routing rules. For example, the Linux **iproute2** package allows you to  [configure a policy where the source IP address selects the outgoing interface](http://www.linuxjournal.com/article/7291)

### Multiple Logical Hosts Issues

Even though the *multiple logical hosts* design (a host with two interfaces in the same IP subnet) is documented in RFC 1122, you could experience significant roadblocks when trying to use multiple IP addresses from the same IP subnet on multiple physical interfaces with modern operating systems, including:

-   **Interaction with host firewall.** Default IP datagram forwarding mechanisms in the host operating system often result in asymmetrical routing. Stateful firewalls might drop asymmetrically forwarded packets.
-   **Duplicate MAC addresses.** An operating system that uses the same MAC address on multiple interfaces could cause significant problems in a switched LAN environment, as packets sourced from the same MAC address through two physical interfaces might confuse the LAN switches.
-   **Proxy ARP replies.** A host with two interfaces connected to the same layer-2 network receives two copies of each ARP request. The host might decide to answer both ARP requests (one of them due to the *proxy ARP* mechanism), resulting in suboptimal IP-to-MAC address mappings in remote hosts.

{{<note>}}An intrusion detection system might interpret dual reply to an ARP request as an indication of ARP spoofing attack.{{</note>}}

-   **Link loss issues.** If a multihomed host loses one of its attachments to the IP subnet, the IP address configured on the failed interface might still be active although its corresponding MAC address is no longer reachable. If you want to use a *multiple logical hosts* implementation in a high-availability design, you should deploy a load balancing device with server loss detection mechanism in front of a multihomed host.

{{<note>}}Some operating systems avoid the link loss issues by supporting transfer of IP and MAC addresses between physical interfaces.{{</note>}}

### More Details

* [Redundant Server-to-Network Connectivity](https://www.ipspace.net/Redundant_Server-to-Network_Connectivity)
* [Redundant Layer-3-Only Data Center Fabrics](/kb/Layer3Fabrics/)
* *[Network Addressing](https://my.ipspace.net/bin/list?id=Net101#ADDR)* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar
* *[Advanced Docker Networking Options](https://my.ipspace.net/bin/list?id=DockerNet#ADV2016)* describing ipvlan and macvlan interfaces 