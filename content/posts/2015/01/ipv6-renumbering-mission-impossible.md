---
cdate: 2023-03-10
comment: |
  Due to changes to source IPv6 address selection algorithms made after this blog post was written in 2013, it's [impossible to use ULA addresses](/2022/05/ipv6-ula-made-useless.html) in dual-stack networks, and the potential results of the Homenet working group were never implemented in mainstream networking gear.
date: 2015-01-26 06:18:00+01:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
title: IPv6 Renumbering – Mission Impossible?
url: /2015/01/ipv6-renumbering-mission-impossible.html
---
In one of the discussions on v6ops mailing list [Matthew Petach wrote](https://www.mail-archive.com/grow@ietf.org/msg01768.html):

> The probability of us figuring out how to scale the routing table to handle 40 billion prefixes is orders of magnitude more likely than solving the headaches associated with dynamic host renumbering. That ship has done gone and sailed, hit the proverbial iceberg, and is gathering barnacles at the bottom of the ocean.

Is it really that bad? Is simple renumbering in IPv6 world just another myth? It depends.
<!--more-->
Renumbering is trivial in most residential environments: get a new delegated prefix from the old or new ISP [using IA_PD](/2013/01/dhcpv6-based-address-allocation-on.html), slice-and-dice it, assign it to local LANs, and use SLAAC to renumber the hosts. You should be able to automate the whole process on router operating systems that were built by people who actually understand IPv6 (Cisco IOS comes close, but [didn't have configurable LAN-side prefix lifetime for delegated prefixes](/2011/12/ipv6-multihoming-without-nat-problem.html) the last time I checked its behavior).

{{<note>}}Also, the [IETF Homenet working group](https://tools.ietf.org/wg/homenet/) is making sure the incredibly complex home environments built by über-geeks could be seamlessly patched together, operated and renumbered using an incredibly complex set of protocols.{{</note>}}

Enterprise environment is a totally different beast -- renumbering the network is the least of your problems; there are DNS zones, firewalls, ACLs, application configuration files, static IP addresses required for whatever odd reason ([see RFC 6866 for more details](https://tools.ietf.org/html/rfc6866)), and IP addresses embedded in source code. Most people (who care enough about their enterprise networks to think about the impact of IPv6) consider it Mission Impossible and [go for PI address space](/2011/02/ipv6-provider-independent-addresses.html) or even become a Local Internet Registry (LIR) to get their own chunk of IPv6 universe.

Some people within IETF tried to find reasonable solutions that wouldn't explode the global BGP table the way ubiquitous IPv6 PI space will (even though some vocal IPv6 gurus still live in denial and claim nothing will go wrong with the global BGP table), resulting in [RFC 6879](https://tools.ietf.org/html/rfc6879), which recommends:

-   **Enterprise-wide IA_PD-based prefix delegation**. Good recommendation, but it makes the whole enterprise addressing dynamic and dependent on proper operation of DHCPv6 -- something many enterprise network architects would be extremely reluctant to do.
-   **Usage of FQDN**. Good luck with this one. Anyone who [has to argue with application owners who claim they need live vMotion across the continent because they cannot possibly understand how to use DNS](/2012/01/ip-renumbering-in-disaster-avoidance.html) knows how hopeless this is.
-   **Use of parametrized address configuration**. Yeah, sure. Cisco IOS **ipv6 prefix** configuration command is the only one I'm aware of (please fix my ignorance by writing a comment explaining how other vendors do it -- and I don't consider Junos configuration-search-and-replace to be a solution). The only way to solve this might be to [use an Ansible-like tool to generate network device configurations](/2014/07/network-automation-spotify-on-software.html).
-   [**Use of ULA addresses**](/2014/01/pa-pi-or-ula-ipv6-address-space-it.html). Another good recommendation (until you encounter ULA-haters).
-   **Reduce DNS and RA timers**. Definitely a good one -- but you might need network automation tool (or automatic configuration deployment) to ensure you get all the instances of RA timers (and hope that they're configurable on all L3 devices in your network).

For an even gloomier picture, read [RFC 7010](https://tools.ietf.org/html/rfc7010) which has a long list of missing functionality that would make IPv6 renumbering in an enterprise network as easy as it is in residential environment.

#### More IPv6?

Check out [IPv6 resources](http://www.ipspace.net/IPv6) on ipSpace net (including [numerous IPv6 webinars](http://www.ipspace.net/Roadmap/IPv6_webinars)), enjoy the [IPv6 presentations](http://content.ipspace.net/bin/presentations) on [ipSpace.net content site](http://content.ipspace.net/), or watch [IPv6-Only Data Centers](http://content.ipspace.net/get/IPv6DC) webinar (one of many [free webinars available on ipSpace.net](http://content.ipspace.net/bin/publicWebinars)).
