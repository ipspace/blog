---
title: "ARP and Static Routes"
date: 2023-08-31 06:30:00
tags: [ ARP ]
pre_scroll: True
---
A few days ago, I [described how ARP behaves when the source- and destination IP addresses are not on the same subnet](/2023/08/arp-details.html) (TL&DR: it doesn't care). Now, let's see how that works with static routes.

We'll run our tests in a small virtual lab with two Linux hosts and an Arista vEOS switch. The link between H1 and RTR is a regular subnet. H2 has an IP address on the Ethernet interface, but RTR uses an unnumbered interface.
<!--more-->
This is the *[netlab](https://netlab.tools/)* topology I'm using:

```
---
defaults.device: eos

groups:
  hosts:
    members: [ h1, h2 ]
    device: linux
    role: target

nodes:
  h1:
  h2:
  rtr:
    id: 1

links:
- h1:
  rtr:
- h2:
  rtr:
    ipv4: True
```

The physical lab topology is as simple as I could make it:

{{<figure src="/2023/08/arp-static.png" caption="Lab topology">}}

The following table contains the lab addressing details:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **h1** |  10.0.0.2/32 |  | Loopback |
| eth1 | 10.1.0.1/30 |  | h1 -> rtr |
| **h2** |  10.0.0.3/32 |  | Loopback |
| eth1 | 10.1.0.5/30 |  | h2 -> rtr |
| **rtr** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 10.1.0.2/30 |  | rtr -> h1 |
| Ethernet2 | True |  | rtr -> h2 |
{.fmtTable}

## Static Route with a Next Hop

We'll use a simple static route on RTR to reach the loopback address of H1:

```
rtr(config)#ip route 10.0.0.2/32 10.1.0.1
```

Arista EOS uses a recursive lookup to resolve the next hop into an interface/next-hop pair:

```
rtr#show ip route 10.0.0.2/32|begin ^ S
 S        10.0.0.2/32 [1/0] via 10.1.0.1, Ethernet1
```

When trying to reach 10.0.0.2, the router sends the IP packet toward the next hop 10.1.0.1, and sends an ARP request for 10.1.0.1. The source IP address in the ARP request is the IP address of the outgoing interface (10.1.0.2).

```
$ sudo tcpdump -i eth1 -n -vv arp
tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 262144 bytes
14:40:50.211774 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 10.1.0.1 tell 10.1.0.2, length 28
14:40:50.211791 ARP, Ethernet (len 6), IPv4 (len 4), Reply 10.1.0.1 is-at 52:54:00:97:60:5b, length 28
```

## Static Route Pointing to an Interface

We cannot use a simple next-hop-only static route to reach H2. The interface connecting RTR with H2 is unnumbered -- RTR does not know how to reach any of the IP addresses of H2 and needs more information. We need to specify the outgoing interface in the static route:

```
rtr(config)#ip route 10.1.0.5/32 ethernet 2
```
  
Because the static route has no next-hop information, Arista EOS assumes the target IP addresses are directly connected[^CCS]:

```
rtr#show ip route 10.1.0.5|begin ^ S
 S        10.1.0.5/32 is directly connected, Ethernet2
```

[^CCS]: A static route pointing to an interface can cover any IP prefix you wish including the default route. You [DO NOT want to do that though](https://blog.ipspace.net/2009/10/follow-up-interface-default-route.html).

When trying to reach 10.1.0.5, the router attempts to reach a directly connected IP address and sends an ARP request for 10.1.0.5. The source IP address in the ARP request is the IP address of the loopback interface that is loaning the IP address to the outgoing interface (10.0.0.1). With the default `arp_ignore` *sysctl* settings, the Linux host has no problem replying to that ARP request.

```
$ sudo tcpdump -i eth1 -n -vv arp
tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 262144 bytes
14:46:10.352583 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 10.1.0.5 tell 10.0.0.1, length 28
14:46:10.352618 ARP, Ethernet (len 6), IPv4 (len 4), Reply 10.1.0.5 is-at 52:54:00:97:b1:88, length 28
```

## Static Route with an Outgoing Interface and a Next Hop

Can we combine outgoing interfaces and next hops? Absolutely. Even more interestingly, could we use a next-hop not in the IP routing table (as the router will only use it for ARP resolution)? You can try and I wish you good luck ;)

Anyway, the easy bit first. We'll add a static route for the loopback interface of H2:

```
rtr(config)#ip route 10.0.0.3/32 ethernet 2 10.1.0.5 
```

Both static routes are in the IP routing table, ARP and ping work (after I fixed the return static route on the Linux host), but we didn't expect anything else, did we:

```
rtr#show ip route
...
Gateway of last resort is not set

 C        10.0.0.1/32 is directly connected, Loopback0
 S        10.0.0.3/32 [1/0] via 10.1.0.5, Ethernet2
 C        10.1.0.0/30 is directly connected, Ethernet1
 S        10.1.0.5/32 is directly connected, Ethernet2
```

Now for the fun part: we'll remove the static route for H2 Ethernet IP address and leave only the static route for H2 loopback interface with a next hop that is not in the IP routing table.

```
rtr(config)#no ip route 10.1.0.5/32 ethernet 2
rtr(config)#ip route 10.0.0.3/32 ethernet 2 10.1.0.5
```

Arista EOS accepts the configured static route but does not install it in the Linux kernel. That might mean the static route would work for ASIC-forwarded packets but not for local traffic; it's obviously impossible to test on an EOS VM.

```
rtr#show ip route
WARNING: Some of the routes are not programmed in
kernel, and they are marked with '%'.
...

Gateway of last resort is not set

 C        10.0.0.1/32 is directly connected, Loopback0
 S%       10.0.0.3/32 [1/0] via 10.1.0.5, Ethernet2
 C        10.1.0.0/30 is directly connected, Ethernet1
```

Anyway, EOS tries to resolve the next hop of the static route and (as expected) sends an ARP request for 10.1.0.5 from 1.0.0.1. The Linux host obligingly replies to it:

```
$ sudo tcpdump -i eth1 -n -vv arp
tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 262144 bytes
15:06:31.104491 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 10.1.0.5 tell 10.0.0.1, length 28
15:06:31.104524 ARP, Ethernet (len 6), IPv4 (len 4), Reply 10.1.0.5 is-at 52:54:00:97:b1:88, length 28
```

However, as the route is not in the Linux kernel routing table, **ping** does not work.

Cisco IOS-XE has no problem with the concept of an IP route with a weird next hop. Configuration syntax is almost identical:

```
rtr(config)#ip route 10.0.0.3 255.255.255.255 gig 3 10.1.0.5
```

Even the route appears in the IP routing table as a perfectly normal route:

```
rtr#show ip route 10.0.0.3
Routing entry for 10.0.0.3/32
  Known via "static", distance 1, metric 0
  Routing Descriptor Blocks:
  * 10.1.0.5, via GigabitEthernet3
      Route metric is 0, traffic share count is 1
```

However, when trying to send a packet to 10.0.0.3:

* IOS XE sends an ARP request for 10.1.0.5 from 10.0.0.1
* Linux replies to the ARP request
* IOS XE gets confused and claims the ARP reply is unexpected.

```
IP ARP: creating incomplete entry for IP address: 10.1.0.5 interface GigabitEthernet3 tableid 0
 In ip_arp_sendrequest_internal: ELse case using src: 10.0.0.1
IP ARP: sent req src 10.0.0.1 5254.00ec.a616,
                 dst 10.1.0.5 0000.0000.0000 GigabitEthernet3
IP ARP rep filtered src 10.1.0.5 5254.009b.f007, dst 10.0.0.1 5254.00ec.a616 wrong cable, interface GigabitEthernet3 tableid 0
```

**Lesson learned**: don't stretch things too far or they might break.

## Baron Munchausen Drops By

[Baron Munchausen](https://en.wikipedia.org/wiki/Baron_Munchausen) famously [pulled himself and his horse out of a mire by his hair](https://en.wikipedia.org/wiki/M%C3%BCnchhausen_trilemma). We can do the same trick with static routes: the next hop of a static route can be within the IP prefix defined in the static route:

```
rtr(config)#ip route 10.1.0.5/32 ethernet 2 10.1.0.5
```

The IP route appears as a perfectly legal static route in the EOS IP routing table and the underlying kernel IP routing table, and everything works:

```
rtr#show ip route 10.1.0.5 detail
...
 S        10.1.0.5/32 is directly connected, Ethernet2 rtr -> h2

rtr#bash

Arista Networks EOS shell

[vagrant@rtr ~]$ ip route
blackhole 0.0.0.0/8 proto gated scope nowhere
10.1.0.0/30 dev et1 proto kernel scope link src 10.1.0.2
10.1.0.5 dev et2 proto gated scope link
blackhole 127.0.0.0/8 proto gated scope nowhere
127.254.254.1 dev fwd0 proto gated scope link metric 1024
```

And now you know another trick that will make your router configurations harder to understand and increase your job security ;) Have fun.
