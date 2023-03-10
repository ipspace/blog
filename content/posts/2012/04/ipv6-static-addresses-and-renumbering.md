---
cdate: 2023-03-10
comment: |
  Due to changes to source IPv6 address selection algorithms made after this blog post was written in 2013, it's [impossible to use ULA addresses](https://blog.ipspace.net/2022/05/ipv6-ula-made-useless.html) in dual-stack networks.
date: 2012-04-04 06:54:00+02:00
multihoming_tag: server
series:
- multihoming
tags:
- IPv6
title: IPv6 Static Addresses and Renumbering
url: /2012/04/ipv6-static-addresses-and-renumbering.html
---
The proponents of [Network Prefix Translation for IPv6 (NPT66)](https://blog.ipspace.net/2011/12/we-just-might-need-nat66.html) usually claim it's required for one of the two reasons: to implement [multihoming without BGP](https://blog.ipspace.net/2010/12/small-site-multihoming-in-ipv6-mission.html) ([valid](https://blog.ipspace.net/2009/05/lack-of-ipv6-multihoming-elephant-in.html)) and to avoid renumbering inside network(s) when the ISP assigns you a new IPv6 prefix. Let's focus on the renumbering claim today.
<!--more-->
A lot of IPv6-focused enterprise engineers have long advised medium-to-large networks to get their own IPv6 address space. Greg Ferro [compiled a long list of good reasons](http://etherealmind.com/importance-provider-independent-ipv6-addresses/) to do that, and having your own PI space is not overly expensive anyway -- [50€ per year in RIPE region](http://www.ripe.net/lir-services/member-support/info/billing/billing-procedure-and-fee-schedule-for-lirs-2011).

### Network Renumbering

There are two reasons you might have to renumber your IPv6 network (assuming it's using public IPv6 addresses like it should):

-   You're using DHCP prefix delegation with your ISP;
-   You've been assigned a static IPv6 prefix but decided to change ISPs (or your ISP decided they have nothing better to do than to annoy their customers).

Most hosts are renumbered automatically if you use SLAAC (it might take a while, so if you're renumbering your static IPv6 prefix take advance precautions like lowering RA prefix lifetimes), configurations of layer-3 forwarding devices (routers, layer-3 firewalls) and the hosts with static IPv6 addresses have to be changed manually.

{{<figure src="/2012/04/s1600-GoodEnough.jpg">}}

Assuming you have a small network with a single layer-3 device (that also acts as a firewall), you can usually perform all renumbering automatically based on IPv6 prefix delegated via DHCPv6 (checking whether your edge router supports that might be a good idea if you're buying new gear).

If you have more than one layer-3 device in the network, you'll probably have to do the renumbering process manually (one would hope that vendors would eventually implement hierarchical prefix delegation, but I haven't seen it implemented yet), but even there a bit of planning goes a long way -- [general prefixes make life easy for Cisco IOS users](http://ccietobe.blogspot.com/2009/01/renumbering-ipv6-with-ease-via-ipv6.html) (Junos has a regex search/replace that you can use to replace patterns, including parts of IPv6 addresses, throughout the configuration).

{{<note>}}Ah, so your preferred vendor doesn't support easy IPv6 renumbering? Yell at them or vote with your wallet and buy something else.{{</note>}}

### Server Renumbering

Automatic IPv6 host renumbering works only if the hosts use SLAAC. Hosts with static IPv6 addresses have to be renumbered manually, but even there you could use [Unique Local Addresses](http://en.wikipedia.org/wiki/Unique_local_address) (ULA -- [RFC4193](http://tools.ietf.org/html/rfc4193)) to avoid most of the renumbering hassle -- assign a global IPv6 prefix and an ULA prefix to every subnet, use static ULA addresses for your inside servers, and use ULA addresses for all internal communications.

Servers that are not reachable from the Internet don't have to have static public IPv6 addresses -- they should have a static ULA address that their clients can use, and a dynamic public IPv6 address they use to access the Internet if needed (example: software patches).

![](/2012/04/s500-MythBusted.gif)

But what about publicly reachable servers? Technology doesn't provide a good answer here and so we enter the realms of layer-10 (religious layer). Some people claim it makes perfect sense to have your own public servers even in networks that are so small they can't justify paying for their own IPv6 address space \... and thus invoke the magic of NPT66 to avoid server renumbering (because it's so hard to renumber the only server you have in your organization after manually changing its public DNS entry whenever you decide to change your ISP).

I would rather [spend \$4.95 a month](http://myhosting.com/personal-website-hosting/) and have a server hosted by someone with reliable infrastructure, which might also increase my web site availability, but that's just me.

### Summary

Properly-designed IPv6 networks will use public IPv6 addresses in combination with ULA addresses (when needed). Get used to it. If you're big enough, get your own IPv6 address space; if you're too small, buy networking gear that supports easy renumbering.

In my personal opinion, the need for NPT66 to avoid server renumbering in single-homed networks without their own PI IPv6 address space is a totally bogus claim. Organizations this small should not have public-facing servers -- web hosting is cheap enough these days.

If you're an IT geek who wants to be able to hug all his servers, that's perfectly fine with me -- just don't complain if you have to take care of them every now and then. I prefer to have a web site that keeps running even when I'm on vacation.

### More Information

If you've just started considering the impact of IPv6 on your network, my [*Enterprise IPv6 -- The First Steps*](http://www.ipspace.net/Roadmap/IPv6_webinars) webinar will get you started. [*Building Large IPv6 Service Provider Networks*](http://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar will give you numerous design guidelines that are also applicable to large enterprise networks ([IPv6 for Enterprise Networks](http://www.amazon.com/gp/product/1587142279/ref=as_li_tf_tl?ie=UTF8&tag=cisioshinandt-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=1587142279) is also a pretty good book).

A few more [IPv6 webinars](http://www.ipspace.net/Roadmap/IPv6_webinars) are planned for this year and you can get access to all of them with the [yearly subscription](http://www.ipspace.net/Subscription).

2012-04-04 11:30 GMT: Added information from Sebastian\'s comment --- Junos search/replace functionality.
