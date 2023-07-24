---
date: 2011-04-28 07:29:00.001000+02:00
dmvpn_tag: quirk
tags:
- DMVPN
title: DMVPN Spoke NHRP Behavior Changed in IOS Release 15.0M
url: /2011/04/dmvpn-spoke-nhrp-behavior-changed-in.html
---
In the good old days, we (thought we) knew how Phase 2 DMVPN works and what happens when the spoke-to-spoke session cannot be established. As I discovered when developing the lab configurations for the [*DMVPN: New Features in IOS Release 15*](https://www.ipspace.net/DMVPN150) webinar, that behavior has forever changed (and not for the better) sometime in the 12.4T (or 15.0M) release. I blame the introduction of NAT awareness in IOS release 12.4(15)T, but it could be another totally unrelated change.
<!--more-->
I've set up a small lab network (actually reused the lab configurations you get as part of the [DMVPN - From Basics to Scalable Networks](https://www.ipspace.net/DMVPN:_From_Basics_to_Scalable_Networks) or [DMVPN New Features](https://www.ipspace.net/DMVPN_New_Features) webinars) shown in the following diagram to illustrate the change in the behavior. After OSPF populated the routing tables on all routers, I pinged the loopback interface of R3 from R2.

{{<figure src="s1600-DMVPN_NHRP_Lab.png">}}

### The Old Behavior

A spoke (R2) sends a NHRP request asking for other spoke's IP address to the hub router. The hub router propagates the NHRP request to the other spoke (R3), which then tries to respond (and build a spoke-to-spoke IPsec tunnel).

If the spoke-to-spoke IPsec tunnel fails to materialize, the two spokes have *incomplete* (and thus unusable) NHRP entries and the traffic continues to flow over the hub router(s).

``` code
R2#sh ip nhrp 192.168.0.6
192.168.0.6/32, Tunnel0 created 00:00:44, expire 00:02:20
  Type: incomplete, Flags: negative
  Cache hits: 2
```

``` code
R3#sh ip nhrp 192.168.0.5
192.168.0.5/32, Tunnel0 created 00:01:02, expire 00:02:02
  Type: incomplete, Flags: negative
  Cache hits: 2
```

### The New Behavior

As before, a spoke (R2) sends a NHRP request asking for other spoke's (R3) IP address to the hub router and the hub router propagates the request to the other spoke. At the same time, the sending spoke (R2) creates *a fake NHRP entry pointing to the hub router.* The fake NHRP entry has a fixed 3-minute expiration time which cannot be changed (with non-hidden commands, at least) and which does not depend on the configured NHRP timers.

The receiving spoke (R3) gleans its peer IP address and builds its own NHRP entry. If the spoke-to-spoke IPsec tunnel establishment fails to materialize, the sending spoke (R2) retains the fake NHRP entry (pointing to the hub); the receiving spoke (R3) has a regular but unusable NHRP entry in *no socket* state (because the IPsec tunnel is not there).

``` code
R2#sh ip nhrp 192.168.0.6
192.168.0.6/32 via 192.168.0.6
   Tunnel0 created 00:00:17, expire 00:02:47
   Type: dynamic, Flags: used temporary
   NBMA address: 10.0.7.17
```

``` code
R3#sh ip nhrp 192.168.0.5
192.168.0.5/32 via 192.168.0.5
   Tunnel1 created 00:00:29, expire 00:00:30
   Type: dynamic, Flags: router implicit
   NBMA address: 10.0.7.9
    (no-socket)
```

As you can see, the expiration time of the fake NHRP entry is 3 minutes, while the expiration time of the gleaned NHRP entry corresponds to the **ip nhrp holdtime** value.

### Is This a Problem?

Yes it is; it's a huge problem in some redundant network designs. [Read this blog post](https://blog.ipspace.net/2013/04/the-impact-of-changed-nhrp-behavior-in.html) for more details; they are also explained in my [DMVPN webinars](http://www.ipspace.net/DMVPN_trilogy).
