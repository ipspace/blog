---
date: 2017-12-20 09:38:00+01:00
tags:
- IPv6
title: Unique IPv6 Prefix Per Host – How Complex Do You Want IPv6 to Be?
url: /2017/12/unique-ipv6-prefix-per-host-how-complex.html
---
In December 2017, IETF published [RFC 8273](https://tools.ietf.org/html/rfc8273) created by the v6ops working group (which means there must have been significant consensus within the working group that we need the solution and that it makes at least marginal sense).

The RFC specifies a mechanism by which the first-hop router allocates a unique /64 IPv6 prefix *for every host attached to a subnet* and uses unicast *and multicast* RA responses sent to *unicast MAC addresses* to give every host the impression that it's the sole host on its own subnet.

The first thought of anyone even vaguely familiar with [how complex IPv6 already is](https://insinuator.net/2015/05/ipv6-complexity/) should be "WTF???" Unfortunately, there are good reasons we need this monstrosity.
<!--more-->
### Why Do We Need This?

There are legal and commercial reasons why Internet Service Providers need to be able to identify individual customers based on their IPv6 addresses. Whenever the ISP is using a P2P access network (DSL or anything that [looks like dialup](/2008/10/internet-access-russian-dolls.html)), each customer gets an IPv6 prefix (or a combo of a /64 access prefix and another delegated prefix) anyway.

There was no such mechanism available for shared access networks like switched Ethernet, PON, or WiFi.

### Hey, Ever Heard of DHCPv6 IA_NA?

Yes, I did. So did everyone else. Unfortunately, ISPs can't use it to control client address allocation due to what can only be viewed as religious opposition from a major mobile OS vendor refusing to implement a DHCPv6 client.

The only way forward, considering that that OS vendor has a huge market segment, was to implement yet another kludge. Hooray!

### But Isn't Prefix-per-Host More Secure Than IA_NA?

No.

Although RFC 8273 hints at increased customer separation (because it was obviously a non-starter saying *we had to do this because \$vendor refuses to acknowledge our perfectly valid needs*), there's no real gain in using /64-per-client from the security perspective.

You could always use RA and DHCPv6 to tell compliant hosts that they should send all traffic through the first-hop router so it can be properly inspected. Non-compliant hosts can always bypass those measures on layer-2 access networks as long as they can figure out the MAC addresses of other hosts (which they can because IPv6 hosts still send multicast ICMPv6 messages during DAD).

### So What's the Impact of This Idea?

You mean beyond wasting half of the address bits and [reverting IPv6 to how it was originally designed](/2017/09/coming-full-circle-on-ipv6-address.html) (the first proposal used 64-bit addresses) after wasting two decades arguing about nuances of SLAAC and ND?

Admittedly, this change keeps the client stack simpler (because there's no need to run DHCPv6) but does not reduce any complexity on the first-hop router. Someone still needs to keep a stateful mapping between clients and their prefixes, and if you have two or more first-hop routers you still have to synchronize the mapping between them.

### Note in the Margin

I have a vague feeling that the state synchronization between redundant first-hop routers would be even more complex than it was before, but the margins of this blog post are not wide enough to elaborate... ;)


### An Alternative Perspective

I sent the draft of this blog post to my good friend Gunther Van De Velde (who, among other things, pushed me to participate in writing my [one-and-only RFC](/2015/02/rfc-7454-bgp-operations-and-security.html)). Here's his perspective on the topic

---

RFC8273 spec created indeed a bit more dust and bits-on-wire-in-v6ops as anticipated, in many different ways... and i agree with your cynicism. This specification is for sure not the result of a protocol beauty contest, but more the complex embodiment of mixed industry support of an incompatible IPv6 address management technologies on UEs (SLAAC vs DHCPv6) bringing operator subscriber management nightmare.

Within the IPv6 community, the consensus for this particular idea has been rather rough, even for v6ops WG. Just count the number of emails exchanged on this topic in last two months and that gives an idea on \"roughness\". I believe that is mainly because many people are not aware about what is \"subscriber management\", and what it exactly achieves, what the purpose is of subscriber management or how it works (even for IPv4). For IPv4 this is as you are aware, mainly done by DHCP or PPPoE subscriber management on a WLAN GW or on a BNG. We as vendor would love to use that experience, and apply that almost identical to IPv6. We have been doing subscriber management very well for IPv4 for a very long time already. Reality is however on universal support of DHCPv6 on UEs is different. 

You agree that IPv6 addressing is a much more complex beast as IPv4 addressing. Also, the adoption of DHCPv6 is not as universal as DHCPv4 on host devices. If DHCPv6 would be as popular and supported as DHCPv4, then for sure RFC8273 would serve little value and is obsolete. However, reality is different, and DHCPv6 support is not a given in all UE's and at same time IPv6 has some fancy addressing methods providing auto-addressing (SLAAC, CGAs, etc...) making subscriber management (legal and commercial) a non-trivial matter. 

In cases where UE subscriber management is executed on a BNG or WLAN-GW, there is a central repository already keeping track and synchronization of UE vs location vs commercial contract vs IP-addresses. This is in this environment already happening, often using some vendor mechanisms or radius attributes. From that perspective, IPv6 is not more or less complex as IPv4. In IPv6 there are however, potentially more addresses to track, because the UE can auto-generate more explicit addresses (CGA, SLAAC, etc).

We started with this work as a solution for community WIFI service at Comcast. For this to be a quality and profitable service, it has to work for the largest denominator of devices trying to make usage of the service. Hence, the simplest method for giving a device an address is found the one that is best supported. This is the plain old simple SLAAC using Neighbor Discovery. So, we decided to tune SLAAC within the limits of the specification without breaking any existing specs of NDP and use that on the WLAN-GW. This was tested successful and worked the best and at scale at Comcast (most devices could do SLAAC and for the UE there is no change at all because all magic happens on the WLAN-GW or the BNG). So we decided to share this experience to the community because Comcast assumed more operators would be looking at exactly the same problem space. 

BTW, a nice summary of the problem that were raised in the many many emails on v6ops mailing list can be [seen in an email from OPS area director](https://www.ietf.org/mail-archive/web/v6ops/current/msg28625.html).
