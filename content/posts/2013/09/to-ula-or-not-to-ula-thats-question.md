---
cdate: 2023-03-10
comment: |
  Due to changes to source IPv6 address selection algorithms made after this blog post was written in 2013, it's [impossible to use ULA addresses](https://blog.ipspace.net/2022/05/ipv6-ula-made-useless.html) in dual-stack networks. The current recommendation for small multihomed sites with PI address space is to use PA prefix from primary provider and NAT66 toward the backup provider.
date: 2013-09-30 07:57:00+02:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- NAT
title: To ULA or Not to ULA, That’s the Question
url: /2013/09/to-ula-or-not-to-ula-thats-question.html
---
Ed Horley, an awesome IPv6 geek I had the privilege to meet at NFD6, wrote an interesting blog post [arguing against IPv6 ULA usage](http://www.howfunky.com/2013/09/ipv6-unique-local-address-or-ula-what.html) (particularly when combined with NPT66). We would all love to get rid of NAT, however \...
<!--more-->
### Meanwhile in the SMB world

It makes perfect sense to use public IPv6 addressing in your private network and get rid of NAT forever *if and only if*:

-   You're big enough to have your own PI address space;
-   You're willing to buy high-end business-class Internet connection for every single remote site (to persuade the upstream ISP to route a /48 prefix belonging to your PI address space);

\... or if you have a single L3 device (which also acts as a simple firewall) in your network.

In other words, if you're a residential user with a single SOHO router/CPE or a Fortune 500 company, you'll do just fine and you really shouldn't use ULAs. Unfortunately, these are the [only two markets most vendors and ISPs care about](http://telecomoccasionally.wordpress.com/2012/02/20/mid-market-innovators-dilemma/); in most other cases, [you'll end up with a total operational nightmare](http://blog.ipspace.net/2012/04/ipv6-legends-and-myths-more-opinions.html):

-   Remote sites having IPv6 prefixes (somewhat) randomly assigned by their ISPs (which will do wonders to your VPN routing);
-   Widespread renumbering every time you change an ISP.

Do I have to mention that although renumbering a single IPv6 segment works really well (for residential users that don't mind a short outage), and [renumbering multiple segments connected to a single router is still manageable](http://blog.ipspace.net/2012/04/ipv6-static-addresses-and-renumbering.html) (assuming the router is running Cisco IOS, most other vendors start sucking at this point), renumbering anything beyond that becomes an exercise in futility.

Of course you can decide to pay €50/year and have your own PI address space. Good for you, but it [sucks for everyone else](http://blog.ipspace.net/2013/03/predicting-ipv6-bgp-table-size.html).

Add access lists and firewall rules into the mix and you'll quickly discover the huge gap between rainbow-colored IPv6 heavens promoted by IPv6 evangelists and operational reality. I could [hack around the access list issues](http://blog.ipspace.net/2013/08/temper-your-macgyver-streak.html) by marking high-order bits in the IPv6 prefix as don't-care-bits (so renumbering wouldn't affect them) \... but that's not how you [configure IPv6 access lists in Cisco IOS](http://www.cisco.com/en/US/docs/ios/ipv6/command/reference/ipv6_10.html#wp2653677) -- the don't care bits are gone; all you can specify is the prefix length.

Oh, and then there's the [small site IPv6 multihoming with PA space](http://blog.ipspace.net/2009/05/lack-of-ipv6-multihoming-elephant-in.html) problem, where it took five years to get to the stage of having an [Internet draft](http://tools.ietf.org/html/draft-troan-homenet-sadr-01) that\'s implemented in the latest Linux kernel. Who knows how long we'll have to wait for the first commercial products to appear.

Just for the record -- I'm not a NAT hugger. I would love to get rid of NAT as much as everyone else, but the sad reality of IPv6 is that the academic theories started meeting the real-life operational needs only a few years ago, and we still have a very long way to go to get the protocol suite we need. In the meantime, [we'll have to use kludges like NAT66 and ULAs in mid-market IPv6 implementations](http://blog.ipspace.net/2011/12/we-just-might-need-nat66.html), not because we love them, but because they're the best tools we have at our disposal.

Unfortunately, the following two quotes from Randy Bush ([replying to another IPv6 architectural beauty contest](http://www.ietf.org/mail-archive/web/v6ops/current/msg14625.html)) still apply to most IPv6 conversations we have:

> It is cheering to see that the IPv6 ivory tower still stands despite years of attack by reality.

> And how much of good people\'s time do you plan to waste on this windmill?

### Just in Case You're New to the IPv6 World

Need to know more about IPv6? Start with my [Enterprise IPv6 -- the first steps](http://www.ipspace.net/Enterprise_IPv6_-_the_First_Steps) webinar (there's also a [service provider version](http://www.ipspace.net/Service_Provider_IPv6_Introduction)) or one of the [more-advanced IPv6 webinars](http://www.ipspace.net/Roadmap/IPv6_webinars) that cover [IPv6 network design](http://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks), [IPv6 security](http://www.ipspace.net/IPv6_security) and [IPv6 transition mechanisms](http://www.ipspace.net/IPv6_Transition_Mechanisms).
