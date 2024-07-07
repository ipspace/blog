---
date: 2012-10-03 08:18:00+02:00
tags:
- IPv6
- security
title: You MUST Take Control of IPv6 in Your Network
url: /2012/10/you-must-take-control-of-ipv6-in-your/
---
I'm positive most of you are way too busy dealing with operational issues to start thinking about IPv6 deployment (particularly if you're working in the enterprise world; European service providers using the same "strategy" just [got a rude wake-up call](http://www.ripe.net/internet-coordination/ipv4-exhaustion)). Bad idea -- if you ignore IPv6, it will eventually blow up in your face. Here's how:
<!--more-->
I was writing about the fun you could have [enabling IPv6 on an unprotected wireless network](/2011/11/ipv6-security-getting-bored-bru-airport/) (or campus LAN) a while ago. The same thing can happen in your data center. Most recently-released operating systems have IPv6 enabled by default; the moment someone accidentally (or on purpose) starts sending RA messages, all the servers on the same LAN get auto-configured IPv6 addresses.

{{<figure src="/2012/10/s1600-ServerExposure.jpg" caption="An intruder happily enjoying a free ride on a network that tries to ignore the realities of IPv6">}}

What happens next depends on your firewall strategy and the operating system you're using:

-   If you're not using host-based firewalls, you have a problem anyway (but it's not getting any worse due to IPv6). The moment one of the servers gets pwned, all other servers become an easy target;
-   If you're running Linux, you're probably using **iptables**. IPv6 is using **ip6tables** (you did configure them, didn't you?). Windows is better -- its firewall works on IPv4 and IPv6.
-   If you're protecting your servers with hypervisor-based firewalls like vShield App or Virtual Security Gateway, your VMs might become exposed, as these firewalls don't support IPv6... but then maybe they throw away unknown protocols. Feedback welcome!

{{<note update>}}**Update 2020-12-25**: Recent hypervisor-based firewalls (oops, microsegmentation) like VMware NSX-T or cloud security groups in AWS or Azure are fully IPv6-aware{{</note>}}

So are you safe if you're running Windows on your servers? Actually not, this was just the appetizer. When I was asking [Mrs. Y](http://packetpushers.net/author/securityprincess/), the host of the [excellent Healthy Paranoia security podcast](http://packetpushers.net/category/podcast-post/healthy-paranoia/) whether my ramblings make sense, she immediately got creative:

> But I could see far worse scenarios. I could use a dual stack server environment to exploit trust between hosts, MITM attacks, DNS cache poisoning. I could set up a DHCPv6 stateless server, just setting bogus RDNS options. Or, some hosts will actually get their RDNS options from SLAAC, because they run an RDNSS.
>
> Additionally, are you blocking transition mechanisms at the border? 6to4 and Teredo? I can always use those as exfiltration mechanisms from your servers too. I would have IPS on data center networks looking for IPv6 traffic, even if you aren\'t officially supporting the protocol. I\'m betting there\'s plenty there.

In any case, you have to take control. You can enable RA guard (you did buy switches with IPv6 support and RA guard, didn't you?), but [even that could by bypassed](http://tools.ietf.org/html/draft-gont-v6ops-ra-guard-evasion-01). You could disable IPv6 on all servers, or filter IPv6 ethertype on layer-2 switches. Regardless of what you decide to do, do not ignore IPv6. It will not go away anytime soon.

## Resources to get you started

-   I [wrote a lot about IPv6](/tag/ipv6/).
-   Cisco has IPv6 design guides for [campus](http://www.cisco.com/en/US/docs/solutions/Enterprise/Campus/CampIPv6.html) and [branch](http://www.cisco.com/en/US/docs/solutions/Enterprise/Branch/BrchIPv6.html) networks.
-   Juniper has Junos Day One books: [Exploring IPv6](http://www.juniper.net/us/en/community/junos/training-certification/day-one/networking-technologies-series/exploring-ipv6/) and [Advanced IPv6](https://www.juniper.net/us/en/community/junos/training-certification/day-one/networking-technologies-series/advanced-ipv6-config/).
-   Cisco Press published several excellent IPv6 books, including [IPv6 Security](http://www.amazon.com/gp/product/1587055945/ref=as_li_tf_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1587055945&linkCode=as2&tag=cisioshinandt-20) and [IPv6 for Enterprise Networks](http://www.amazon.com/gp/product/1587142279/ref=as_li_tf_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=1587142279&linkCode=as2&tag=cisioshinandt-20).
-   I've created [several IPv6 webinars](http://www.ipspace.net/IPv6), including the [IPv6 security](http://www.ipspace.net/IPv6Sec) webinar. You can get access to all of them with the [yearly subscription](http://www.ipspace.net/Subscription_to_ioshints_webinars).
