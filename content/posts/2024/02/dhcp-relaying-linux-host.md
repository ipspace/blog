---
title: "DHCP Relaying on a Linux Host"
date: 2024-02-28 07:02:00
tags: [ DHCP ]
pre_scroll: True
series: [ dhcp-relay ]
lastmod: 2024-03-02 20:33:00+01:00
---
Markku Leiniö sent me an interesting observation after writing a series of [DHCP-relaying-related blog posts](https://majornetwork.net/2023/06/dhcp-relay-part-3-two-relays-two-servers/):

> I was first using VyOS, but it uses the ISC DHCP relay, and that software relays unicast packets. The DHCP procedures eventually worked fine, but getting sensible outputs and explanations was a nightmare.

I quickly reproduced the behavior, but it took me almost half a year to turn it into a blog post. Engaging in a round of yak shaving (I wanted to [implement DHCP in netlab first](https://netlab.tools/module/dhcp/)) didn't exactly help, either.
<!--more-->
### The Setup

I used the simplest possible topology:

* A single client (Cumulus Linux container) is connected to a DHCP relay (a Linux router running `isc-dhcp-relay`).
* The other interface of the Linux router is connected to a DHCP server (a Linux container running `dnsmasq`).

Here's the corresponding *netlab* topology file (it uses the DHCP module and thus requires [release 1.8](https://netlab.tools/release/1.8/#release-1-8-0)):

```
module: [ dhcp ]

nodes:
  relay:
    module: [ dhcp ]
    role: router
    device: linux
  c1:
    device: cumulus
    provider: clab
  s1:
    device: dnsmasq
    provider: clab
    dhcp.server: true

links:
- c1:
    ipv4: dhcp
  relay:
    dhcp.server: s1
- relay-s1
```

Here's the lab diagram in ASCII format:

{{<ascii>}}
┌──────┐ ┌──────┐ ┌──────┐
│Client│ │Relay │ │Server│
└──┬───┘ └─┬───┬┘ └───┬──┘
   │       │   │      │   
───┴───────┴─ ─┴──────┴───
 Downstream      Upstream 
{{</ascii>}}

Here's the lab addressing overview:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **c1** |
| swp1 | DHCP |  | c1 -> relay |
| **relay** |  10.0.0.1/32 |  | Loopback |
| eth1 | 172.16.0.1/24 |  | relay -> c1 |
| eth2 | 172.16.1.1/24 |  | relay -> s1 |
| **s1** |
| eth1 | 172.16.1.3/24 |  | s1 -> relay |
{.fmtTable}

And here's what Microsoft Copilot (and DALL-E) thinks my lab looks like[^PU] 😂:

{{<figure src="/2024/02/dhcp-relay-lab.jpg">}}

[^PU]: The prompt I used: "Draw a diagram of a network having a DHCP client connected to a DHCP relay, with the same DHCP relay being connected to a DHCP server."

### The Experiment

After starting the lab, I started `tcpdump` on both links. The two links connect a container with a VM and are thus implemented as Linux bridges. It's easy to find their names with `brctl show`:

```
$ brctl show
...
virbr2    8000.5254002742d5 yes   c1_swp1
                                  vgif_relay_1
virbr3    8000.5254009d41ea yes   s1_eth1
                                  vgif_relay_2
```

The initial DHCP exchange looked reasonable, but the lease renewals were decidedly weird. Here's what you can see on the client-to-relay link[^PAFC]: the DHCP client sends a single request that results in two replies.

```
$ sudo tcpdump -i virbr2 -v udp
tcpdump: listening on virbr2, link-type EN10MB (Ethernet), snapshot length 262144 bytes
17:03:23.679907 IP (tos 0x0, ttl 64, id 48880, offset 0, flags [DF], proto UDP (17), length 334)
    172.16.0.254.bootpc > 172.16.1.3.bootps: BOOTP/DHCP, Request from aa:c1:ab:eb:3f:89 (oui Unknown), length 306, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)

17:03:23.691245 IP (tos 0xc0, ttl 63, id 59023, offset 0, flags [none], proto UDP (17), length 329)
    172.16.1.3.bootps > 172.16.0.254.bootpc: BOOTP/DHCP, Reply, length 301, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Your-IP 172.16.0.254
	  Server-IP 172.16.1.3
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)

17:03:23.691255 IP (tos 0x10, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 329)
    172.16.0.1.bootps > 172.16.0.254.bootpc: BOOTP/DHCP, Reply, length 301, hops 1, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Your-IP 172.16.0.254
	  Server-IP 172.16.1.3
	  Gateway-IP 172.16.0.1
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)
```

[^PAFC]: Printout abridged for clarity reasons

And here's the printout from the relay-to-server link: the single DHCP request sent to the relay resulted in two copies of the same request sent to the DHCP server, which sent back two DHCP replies:

```
$ sudo tcpdump -i virbr3 -v udp
tcpdump: listening on virbr3, link-type EN10MB (Ethernet), snapshot length 262144 bytes
17:03:23.680184 IP (tos 0x0, ttl 63, id 48880, offset 0, flags [DF], proto UDP (17), length 334)
    172.16.0.254.bootpc > 172.16.1.3.bootps: BOOTP/DHCP, Request from aa:c1:ab:eb:3f:89 (oui Unknown), length 306, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)

17:03:23.680227 IP (tos 0x0, ttl 64, id 6880, offset 0, flags [DF], proto UDP (17), length 334)
    172.16.1.1.bootps > 172.16.1.3.bootps: BOOTP/DHCP, Request from aa:c1:ab:eb:3f:89 (oui Unknown), length 306, hops 1, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Gateway-IP 172.16.0.1
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)

17:03:23.690910 IP (tos 0xc0, ttl 64, id 59023, offset 0, flags [none], proto UDP (17), length 329)
    172.16.1.3.bootps > 172.16.0.254.bootpc: BOOTP/DHCP, Reply, length 301, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Your-IP 172.16.0.254
	  Server-IP 172.16.1.3
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)

17:03:23.690974 IP (tos 0xc0, ttl 64, id 52632, offset 0, flags [none], proto UDP (17), length 329)
    172.16.1.3.bootps > 172.16.0.1.bootps: BOOTP/DHCP, Reply, length 301, hops 1, xid 0x8db31446, Flags [none]
	  Client-IP 172.16.0.254
	  Your-IP 172.16.0.254
	  Server-IP 172.16.1.3
	  Gateway-IP 172.16.0.1
	  Client-Ethernet-Address aa:c1:ab:eb:3f:89 (oui Unknown)
```

Amazingly, the whole thing works. The DHCP specifications (and most implementations) are robust enough to survive a lot of abuse, including duplicate packets.

### What's Going On?

The root cause of this weird behavior turns out to be IP forwarding enabled on the Linux relay. When you turn off IP forwarding with `sudo sysctl net.ipv4.ip_forward=0`, the duplicate packets disappear.

[^IPv6K]: Don't get me started on IPv6 kernel options ;)

**isc-dhcp-relay** is one of the most [underdocumented](https://www.youtube.com/watch?v=oebqlzblfyo&t=341s) bits of [Linux networking software](https://blog.ipspace.net/2020/09/grasping-linux-networking.html) I've seen so far[^IPv6K], so I can only guess what exactly they wanted to achieve. However, Sebastian Schrader [provided a great explanation of the observed behavior](https://blog.ipspace.net/2024/02/dhcp-relaying-linux-host.html#2119) in the comments (slightly reworded):

{{<long-quote>}}

When a client has no IP address, a raw socket is needed on the client and the server side to send and receive raw IP packets.

The observed difference between the upstream and downstream direction is because ISC DHCP Relay needs to open a raw socket toward the downstream interface, whereas a regular UDP socket is used in the upstream direction. `dhcrelay` seems to capture all DHCP traffic destined toward port 67 on the downstream side, instead of checking the destination IP address.
{{</long-quote>}}

With that explanation in mind, the packet traces make perfect sense:

* When the Linux relay receives a unicast DHCP packet (sent from a DHCP client to a DHCP server) on a downstream interface, it *routes* the packet toward the server. That's the first packet seen on the upstream interface.
* `dhcrelay` captures the same packet on its raw socket and *relays* it toward the same DHCP server. That explains the `Gateway-IP` field in the second DHCP request packet.
* The DHCP server replies to both packets, sending one directly to the DHCP client and the other to the gateway IP address.
* `dhcrelay` receives a response from the DHCP server on its `Gateway-IP` address and forwards it to the DHCP client.

### Does That Work as Designed?

Sort of. We have to analyze three scenarios:

* `dhcrelay` is running on a Linux host *in parallel* to a router that does not have DHCP relaying functionality. `dhcrelay` will receive the initial DHCP broadcast packet but not the subsequent unicast packets (as they will be sent to a different MAC address). There will be no duplicate packets.
* `dhcrelay` is running *on a router*. Expect duplicate requests followed by multiple replies.
* A Linux host running `dhcrelay` acts like a bastion host between two otherwise unconnected subnets. This is where the fun starts.

The last scenario works only with tons of static routes, as the DHCP relay host is not a router. To make the packet forwarding of unicast DHCP packets work in both directions, you need:

* On the DHCP client: a static route for the DHCP server pointing to the DHCP relay host. Admittedly, you can solve that with the Static Route DHCP option (option 121, defined in [RFC 3442](https://www.rfc-editor.org/rfc/rfc3442)), but I have better things to do with my time.
* On the DHCP server: a static route for the DHCP relay's *downstream* IP interface pointing its *upstream* interface.

It would be better to implement this scenario with inter-VRF relaying using the [Link Selection suboption](https://datatracker.ietf.org/doc/html/rfc3527) designed specifically for that use case. Interesting, that RFC is implemented in **isc-dhcp-relay** but FOR A SINGLE DOWNSTREAM INTERFACE. Whoever wrote that code probably considered it good enough to expect a separate bastion host for every subnet. After all, VMs are cheap these days.

In any case, I guess it's simpler to tell people to automate a whole bunch of ~~crap~~ system parameters to work around software deficiencies.

### Why Is That a Problem?

Well, it's not, as long as you use `isc-dhcp-relay` outside of the forwarding path or don't care about duplicate requests and responses.

Unfortunately, a lot of smaller networking companies adopted the "_let's grab some open-source Linux tools and slap some UI in front of that_" approach to building Linux-based networking devices[^SDWAN], and so `isc-dhcp-relay` started appearing on Linux routers[^SW]. Those routers have to forward IP packets (or they wouldn't be routers), so we get the *duplicate packet* mess every time someone configures a DHCP relay on VyOS or Cumulus Linux 4.x[^CL] *assuming the unicast DHCP packets reach the control-plane CPU.* That's definitely the case on software routers like VyOS; I have no idea what happens when you put a forwarding ASIC in front of the control-plane CPU (for example, when using Cumulus Linux on an NVIDIA data center switch).

[^SW]: You're allowed to call them *switches* if you work for a marketing department or when creating a PowerPoint slide deck.

[^CL]: I did not try out how Cumulus Linux 5.x behaves because I'm trying to [stay as far away from NVUE](https://blog.ipspace.net/2022/10/cumulus-linux-nvue.html) as I can these days, and nobody seems to be willing to step up and write the _netlab_ NVUE configuration templates.

[^SDWAN]: And if you connect those Linux-based routers to WAN interfaces, you get SD-WAN because the behavior of the whole thing is *defined* by whatever *software* you threw together in a hurry to get VC funding or to get acquired.

### Revision History

2024-03-02
: Rewrote large parts of the "What's Going On?" section and conclusions based on readers' comments.
