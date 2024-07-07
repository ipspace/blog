---
cdate: 2023-03-10
comment: 'We made absolutely no progress on this front in over a decade. Small-site
  multihoming is still mission impossible, and in February 2023 another draft was
  created in v6ops working group effectively describing the same problems I described
  in 2010.

  '
date: 2010-12-02 09:17:00.001000+01:00
high-availability_tag: multihoming
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- NAT
- Internet
- high availability
title: 'Small Site Multihoming in IPv6: Mission Impossible?'
url: /2010/12/small-site-multihoming-in-ipv6-mission/
---
**Summary:** I can't figure out how to make small-site multihoming (without BGP or PI address space) work reliably and decently fast (failover in seconds, not hours) with IPv6. I'm probably not alone.

**Problem:** There are cases where a [small site needs (or wants) to have Internet connectivity from two ISPs](/2009/05/small-site-multihoming-tutorial/) without going through the hassle of getting a BGP AS number and provider-independent address space, and running BGP with both upstream ISPs.
<!--more-->
The [primary/backup scenario is very easy to implement with multiple per-interface NAT rules in IPv4 world](/2009/05/small-site-multihoming-tutorial/). With some load balancing trick, you can use both links simultaneously and if you really want to stretch the envelope, you can try to deploy publicly-accessible servers (although I would try every public cloud solution before pulling this stunt).

**Is this realistic?** Sure it is, let me give you a personal example. I usually work from home and Internet is one of my indispensable tools; it's totally unacceptable to have no Internet connectivity for a few hours (or days). I'm positive more and more individuals and small businesses will have similar requirements.

**What's the big deal with IPv6?** The IPv4 approach to this problem involves heavy use of NAT44, which allows us to control the return path (based on source IP address in the outgoing packet). As of today, there's no production-grade NAT66 ([see comments to this post](/2010/11/ipv6-addressing-how-wrong-can-you-get/)), so the same principle cannot be deployed in IPv6 world.

Worst case, if we can't make small-site multihoming work reliably with IPv6, a lot of users will be forced to go down the PI/BGP path and the Internet routing tables will explode even faster than expected. 

{{<note info>}}I'm describing the Internet routing problems in my [*Upcoming Internet Challenges*](http://www.ipSpace.net/InternetChallenges) webinar.{{</note>}}

**Alternative approaches?** Multihoming was supposed to be an integral part of IPv6 (not really, a lot of details are missing -- another topic of my [*Upcoming Internet Challenges*](http://www.ipSpace.net/InternetChallenges) webinar), but maybe the following trick would work for small sites. Please share your opinions in the comments.

### Could This Work?

A CPE router with two uplinks will get delegated prefixes from both ISPs through DHCPv6. You can assign both prefixes to the LAN interface and your IPv6 hosts using stateless autoconfiguration (SLAAC -- [RFC 4862](http://tools.ietf.org/html/rfc4862)) will get an address from each delegated prefix (having multiple IPv6 addresses per interface is a standard IPv6 feature). However, the address selection rules the IPv6 hosts are suppose to use ([RFC 3484](http://tools.ietf.org/html/rfc3484)) don't take in account the path availability.

If one of the upstream links fails, your IPv6 hosts would continue using the IPv6 address from the now-unreachable address space and although the outbound traffic would be forwarded over the remaining link, the return traffic would end up in wrong AS (with the failed link to your site) and would be dropped.

Assuming [DHCPv6 prefix delegation and DHCPv6 clients in CPE routers work as intended](/2010/10/dhcpv6-over-pppoe-total-disaster/), it's possible to detect link loss and subsequent delegated prefix loss, and revoke the IPv6 prefix from router advertisements sent to the LAN interfaces, but that might be a slow process. The minimum valid lifetime of an IPv6 prefix in ND messages used for stateless autoconfiguration is two hours to prevent denial-of-service attacks (see paragraph (e) of section 5.5.3 of RFC 4862), so it could take up to two hours for the IPv6 connectivity to be fully operational after a link loss. Not something I would be happy with.

Last but not least, unless you use some crazy EEM-triggered tricks, your IPv6 hosts will have addresses from both ISPs most of the time. Influencing address selection rules is not trivial ([this is how you can do it on Linux](http://www.davidc.net/networking/ipv6-source-address-selection-linux) and [this is the procedure for Windows](http://technet.microsoft.com/en-us/library/bb877985.aspx)) and unless you're pretty experienced your hosts will select one path or the other based on whatever internal decisions they make, not based on the primary/backup selection you'd like to have.

What do you think? Would the end-users who need redundant connectivity implement this kludge or would they request PI address space, BGP AS number and implement BGP (or just ask both ISPs to install static routes for their PI prefix)... or shall we wait for NAT66?
