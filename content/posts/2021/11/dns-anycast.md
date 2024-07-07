---
anycast_tag: use
date: 2021-11-02 06:57:00+00:00
high-availability_tag: external
series:
- anycast
tags:
- DNS
- high availability
title: Where Would You Need DNS Anycast?
---
One of the publicly observable artifacts of the [October 2021 Facebook outage](/2021/10/circular-dependencies-considered-harmful/) was an intricate interaction between BGP routing and their DNS servers needed to support optimal anycast configuration. Not surprisingly, it was all networking engineers' fault according to some opinions[^1]

> There's no need for anycast[^2]/BGP advertisement for DNS servers. DNS is already highly available by design. Only network people never understand that, which leads to overengineering.

It's not that hard to find a counter-argument[^CA]: while it looks like there are [only 13 root name servers](https://root-servers.org/)[^RNS], each one of them is a large set of instances advertising the same IP prefix[^3] to the Internet.
<!--more-->
[^1]: Details removed to protect the overconfidently naive

[^2]: Advertising the same IP address from multiple locations, or having a set of servers accepting queries and responding from the same IP address.

[^3]: Containing the IP address of the root name server

[^CA]: See also the first link in the *Want to Know More?* section

[^RNS]: While recording a podcast with [Corey Quinn](https://twitter.com/QuinnyPig), he pointed out that the "13 root name server" limitation is due to the maximum size of early DNS packets (512 bytes). [More details](https://lists.isc.org/pipermail/bind-users/2011-November/085653.html) from Mark Andrews.

For example, in October 2021, 118 sites advertised the J name server, some of them locally (to adjacent ISPs), others globally. Furthermore, while there are over 1000 instances of root name servers worldwide, at least [RIPE often implements a K name server instance](https://labs.ripe.net/author/romeo_zwart/new-architecture-model-for-k-root-local-instances/) as a cluster of servers advertising the same IP address to the adjacent routers. *Local nodes* are implemented with two servers (even smaller *hosted nodes* have a single server), while the larger *global nodes* always run on a server farm.

I guess there's no doubt root name servers use anycast. It must be the incompetent networking engineers setting them up like that, right? There might be other reasons beyond the maximum size of a DNS reply packet -- the *[Evaluating The Effects Of Anycast On DNS Root Nameservers](https://www.ripe.net/publications/docs/ripe-393)* article (HT: @hugoslabbert) lists three goals of root name server anycast:

* Increased resilience
* Higher (improved) performance
* Reliability (deploying root name servers closer to clients).

There's another reason organizations like CloudFlare use anycast: DDoS prevention. If you advertise the same IP prefix from hundreds of locations, it's hard to build a large-enough botnet to bring them all down.

Closer to the DNS clients, many organizations use anycast DNS servers as recursive resolvers. Google's 8.8.8.8 and CloudFlare's 1.1.1.1 are the obvious examples; I'm positive any decent-sized ISP does the same. [@rot26de described a great reason for that](https://twitter.com/rot26de/status/1445850008444624907):

> In the past I anycasted a (small) ISPs Resolvers. Linux ALWAYS waits for a timeout of the first resolver before asking the second[^4]. That can cause loads of false monitoring timeouts of services relying on reverse DNS.

[^4]: Cisco IOS had the same behavior the last time I looked

OK, so we know root name servers use anycast, and many recursive resolvers use it to ensure better performance for suboptimal clients, but surely an authoritative DNS server for a small organization does not need to use anycast?

Of course not. In the past, I had one name server running within the organization, and a secondary one running somewhere else to increase the resilience of name resolution[^5]. 

[^5]: Even if my web site was down, it was nice to have working MX records to forward the mail to an alternate SMTP server.

To be realistic: those days are long gone, I'm too old for that **** and use hosted DNS service... and all hosted solutions I would consider use anycast. It's amazing how influential those damn incompetent over-engineering networking people got in the meantime.

Finally, consider the amount of DNS traffic any member of the FAANG club must be getting (Facebook claims to have 2.9 billion active users). Highly distributed anycast is the only sane way to survive that onslaught.

### Want to know more? 

* [Best Practices in DNS Service-Provision Architecture](https://meetings.icann.org/en/marrakech55/schedule/mon-tech/presentation-dns-service-provision-07mar16-en.pdf) is a must-read classic[^8]
* [RFC 9199](https://www.rfc-editor.org/rfc/rfc9199.html) will tell you way more than you ever wanted to know about large-scale DNS deployments.
* I covered [anycast as a load balancing technique](https://my.ipspace.net/bin/get/DC30/2.2.3.1%20-%20DNS%20and%20Anycast%20Load%20Balancing.mp4?doccode=DC30) in the _[Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers)_ webinar;
* Nat Morris had a nice [Anycast on a Shoestring](https://ripe69.ripe.net/wp-content/uploads/presentations/36-Anycast-on-a-shoe-string-RIPE69.pdf) presentation at RIPE69[^7] ([video](https://ripe69.ripe.net/archives/video/180/))

[^7]: Hat tip to [Jan Žorž](https://www.linkedin.com/in/janzorz/)

[^8]: Found in a LinkedIn post by Jeff Tantsura

### Lessons learned

* Anycast DNS is used in most large-scale environments to provide resilience, scalability, improved reliability, and other features like geographic load balancing (for more details, listen to the [podcast I did with NS1 in 2015](/2015/04/nsone-data-driven-dns-on-software-gone/)).
* Your network or DNS traffic is not remotely similar to Facebook's (or root name servers).
* Whatever lessons and experience you might have gained running your environment for ages might not be relevant in dissimilar-enough environments.
* Sometimes people do stuff for good reasons. It might be worth figuring out what their reasoning is even if you disagree with them -- that's how we learn and become better engineers.

