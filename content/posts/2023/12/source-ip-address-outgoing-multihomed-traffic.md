---
title: "Setting Source IP Address on Traffic Started by a Multihomed Host"
date: 2023-12-20 08:39:00+01:00
tags: [ IP routing, TCP ]
---
In the [Path Failure Detection on Multi-Homed Servers](/2023/05/failure-detection-server-dual-homing.html) blog post, I mentioned [running BGP on servers](/2016/02/running-bgp-on-servers.html) as one of the best ways to detect server-to-network failures. As always, things aren't as simple as they look, as [Cathal Mooney quickly pointed out](/2023/05/failure-detection-server-dual-homing.html#1855):

> One annoyance is what IP address gets used by default by the system for outbound traffic. It would be nice to have a generic OS-level way to say, "This IP on lo0 should be default for outbound IP traffic unless to the connected link subnet itself."

That's definitely a tough nut to crack, and Cathal described a few solutions he used in the past:
<!--more-->
> Obviously, some software allows you to specify the source IP to use, but again more complexity in config. And some doesn't. I've solved it before with an iptables/nft SNAT rule for everything not on the connected subnet, but again, it's messier than one would like.

You can also try a few other tricks, including:

**Use multipath-aware software.** iSCSI immediately comes to mind. For more details, read the [Applications Using Multiple IP Addresses](/kb/Layer3Fabrics/20-apps.html) part of the [Redundant Layer-3-Only Data Center Fabrics](/kb/Layer3Fabrics/) document.

**Use Multipath TCP.** Assuming you're worried about clients running on the multihomed servers[^SBL], you could use Multipath TCP to use all available external IP addresses. Once the parallel TCP sessions are established, Multipath TCP survives the loss of any one IP address. QUIC has similar capabilities but requires changes in the applications using it because we [borked the socket API](/2009/08/what-went-wrong-socket-api.html) (that's why [SCTP got nowhere](/2009/08/what-went-wrong-sctp.html)[^NICHE]).

[^SBL]: With server/daemon applications listening to incoming TCP requests on the loopback IP address.

[^NICHE]: OK, I know it's successfully used in niche applications, and some of those niches could be significant, but so is every other networking technology ever invented.

**Use the same IP Address on all interfaces.** Linux doesn't care if you use the same IP address on all interfaces and will happily use it. Unfortunately, you cannot run BGP with two ToR switches in this setup, hoping it will just work[^SIP]. You can run BGP over IPv6 LLA addresses, though (that trick is often called *unnumbered BGP* because that sounds better).

[^SIP]: You can configure secondary IP addresses on physical interfaces if your BGP daemon allows you to specify the source IP address to use in outgoing TCP sessions. Alternatively, you could make server BGP daemons passive and let the ToR switches connect to whatever address they like. The opportunities for enhanced job security are endless.

**Specify the source IP address in the routing table.** Yes, you can do that on Linux -- the **ip route add** command accepts the next hop and the source IP address parameters. If you cannot use the same trick with routes derived from a routing protocol[^SRC], use a workaround: your servers could receive a viable next hop via BGP and then use a default route pointing to the BGP-derived next hop[^MJS].

[^MJS]: I told you, improving your job security has never been easier ;)

[^SRC]: FRR has a **set src** route map option, but I couldn't find it in the [FRR route-map documentation](https://docs.frrouting.org/en/latest/routemap.html). Maybe I will create a lab one of these days to figure out how it works.

**Use iptables**, the duct tape of Linux networking. Bonus points: you'll be the only one understanding your network.

**Keep calm and carry on.**[^NPT] The "What source IP address will be used?" challenge applies only to client sessions (outgoing sessions established by the multihomed server). If these sessions tend to be short-lived (for example, HTTP requests in a multi-tier application), and if your application survives an occasional failure[^IBD], you're trying to [solve an imaginary problem](https://dev.to/ben/solving-imaginary-scaling-at-scale-the-talk).

[^IBD]: It better does; otherwise, you have a bigger problem on your hands.

[^NPT]: See also: [Don't Panic Towel](https://en.wikipedia.org/wiki/Towel_Day).

Finally, if you want to figure out which source IP address an application uses, the [blog post by Michael Kashin](https://networkop.co.uk/post/2023-09-linux-src/) might be handy.
