---
title: "DHCP Relaying on a Linux Host"
date: 2024-02-28 07:02:00
tags: [ DHCP ]
pre_scroll: True
series: [ dhcp-relay ]
---
Markku Leiniö sent me an interesting observation after writing a series of [DHCP-relaying-related blog posts](https://majornetwork.net/2023/06/dhcp-relay-part-3-two-relays-two-servers/):

> I was first using VyOS, but it uses the ISC DHCP relay, and that software relays unicast packets. The DHCP procedures eventually worked fine, but getting sensible outputs and explanations was a nightmare.

I quickly reproduced the behavior, but it took me almost half a year to turn it into a blog post. Engaging in a round of yak shaving (I wanted to implement DHCP in netlab first) didn't exactly help, either.
<!--more-->
### The Setup

I used the simplest possible topology:

* A single client (Cumulus Linux container) is connected to a DHCP relay (a Linux router running `isc-dhcp-relay`).
* The other interface of the Linux router is connected to a DHCP server (a Linux container running `dnsmasq`).

Here's the corresponding *netlab* topology file (it uses the DHCP module and thus requires release 1.8):

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

**isc-dhcp-relay** is one of the most [underdocumented](https://www.youtube.com/watch?v=oebqlzblfyo&t=341s) bits of [Linux networking software](https://blog.ipspace.net/2020/09/grasping-linux-networking.html) I've seen so far[^IPv6K], so I can only guess what they wanted to achieve. Still, I suspect it was supposed to be used on bastion hosts to implement an application-level relay between isolated subnets -- the DHCP relay forwards DHCP packets received on *downstream* interfaces to *upstream* interfaces and vice versa *even when those packets are not sent to a local IP address*. We get duplicate packets because the same packets get forwarded by the Linux IP forwarding code, and I can't figure out why the duplication happens in the upstream- but not in the downstream direction.

### Does That Work as Designed?

Yes, it does, with tons of static routes. Remember, the _relay_ host is not supposed to be a router, so you need:

* A static route for the DHCP server pointing to the DHCP relay on the DHCP client. Admittedly, you can solve that with the Static Route DHCP option (option 121, defined in [RFC 3442](https://www.rfc-editor.org/rfc/rfc3442)), but I have better things to do with my time.
* On the DHCP server, you also need a static route for the *downstream* IP interface of the DHCP relay pointing to the *upstream* interface.

Would it be so hard to implement it properly with something like inter-VRF relaying? The [Link Selection suboption](https://datatracker.ietf.org/doc/html/rfc3527) was designed specifically for that use case, and it's implemented in **isc-dhcp-relay** FOR A SINGLE DOWNSTREAM INTERFACE. Whoever wrote that code probably considered it good enough to expect a separate bastion host for every subnet. After all, VMs are cheap these days.

In any case, I guess it's simpler to tell people to automate a whole bunch of ~~crap~~ system parameters to work around software deficiencies.

### Why Is That a Problem?

Well, it's not, as long as you use `isc-dhcp-relay` the way it was supposed to be used. Unfortunately, a lot of smaller networking companies adopted the "_let's grab some open-source Linux tools and slap some UI in front of that_" approach to building Linux-based networking devices[^SDWAN], and so `isc-dhcp-relay` started appearing on Linux routers[^SW]. Those routers have to forward IP packets (or they wouldn't be routers), so we get the *duplicate packet* mess every time someone configures a DHCP relay on VyOS or Cumulus Linux 4.x[^CL].

[^SW]: You're allowed to call them *switches* if you work for a marketing department or when creating a PowerPoint slide deck.

[^CL]: I did not try out how Cumulus Linux 5.x behaves because I'm trying to [stay as far away from NVUE](https://blog.ipspace.net/2022/10/cumulus-linux-nvue.html) as I can these days, and nobody seems to be willing to step up and write the _netlab_ NVUE configuration templates.

[^SDWAN]: And if you connect those Linux-based routers to WAN interfaces, you get SD-WAN because the behavior of the whole thing is *defined* by whatever *software* you threw together in a hurry to get VC funding or to get acquired.
