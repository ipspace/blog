---
title: "Classification of BGP Route Leaks (RFC 7908)"
date: 2023-06-12 06:13:00
tags: [ BGP, security ]
---
While preparing the *[Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security)* webinar, I stumbled upon [RFC 7908](https://www.rfc-editor.org/rfc/rfc7908.html), containing an excellent taxonomy of BGP route leaks. I never checked whether it covers every possible scenario[^EPS], but I found it a handy resource when organizing my thoughts.

Let's walk through the various leak types the authors identified using the following sample topology:
<!--more-->
{{<figure src="/2023/06/bgp-leak-topology.png">}}
[^EPS]: Also: In a chat during the [ITNOG7 conference](https://www.itnog.it/itnog7/), [Lefteris Manassakis](https://manassakis.net/) told me things are always more complex in the Wild West called The Internet than we can imagine.

**Hairpin turn**: a customer lacks output filters and propagates routes between two service providers (example: Cust-AB propagates ISP-A routes to ISP-B). Depending on the upstream connectivity of the ISPs, the path through the customer AS might result in the shortest AS path. Even worse, many service providers prefer customer routes over peer routes regardless of AS path length[^BW]

[^BW]: ... resulting in interesting BGP wedgies documented in [RFC 4264](https://www.rfc-editor.org/rfc/rfc4264.html).

**Lateral leak**: a service provider is leaking peer routes (example: ISP-B forwards ISP-A prefixes to ISP-C), and its peers usually accept them as best routes:

-   AS path on a lateral leak is shorter than the paths going through the transit providers
-   Nobody in their right mind would prefer transit routes (where they're paying for traffic or bandwidth) over settlement-free peer routes.

Everyone involved in a lateral leak should be grateful that a kind soul provides free transit connectivity. Unfortunately, that kind soul usually forgets to provision its peer links accordingly, resulting in congestion and customer complaints.

**Peer-transit leaks**: a service provider is leaking peer routes to its upstream transit provider (or vice versa). In our topology, ISP-B would leak routes between ISP-A and Trans-2. The transit provider would often prefer leaked routes (coming from its customer), and the peer ISP would probably choose them due to the shorter AS path length.

As before, karma punishes the kind soul providing free transit with extra traffic charges, and everyone gets yelled at due to inevitable link congestion. Not exactly a fun day in the office.

Lack of routing policies (= filters) on EBGP sessions usually cause the abovementioned leaks. Now for some heavy hitters:

**Prefix re-origination**: an autonomous system advertises third-party prefixes as belonging to itself:

-   When someone leaks hundreds of thousands of prefixes, we're probably dealing with a [two-way redistribution gone wrong](https://blog.ipspace.net/2020/10/redistributing-bgp-into-ospf.html).
-   Dozens or hundreds of more-specific prefixes from different autonomous systems? Probably a gift from a [friendly BGP optimizer running with insecure default settings](https://blog.cloudflare.com/how-verizon-and-a-bgp-optimizer-knocked-large-parts-of-the-internet-offline-today/).
-   Just a few prefixes? "Temporary" static routes redistributed into BGP or a malicious hijack.

Finally, there's the **accidental leak of internal-** or **more-specific prefixes**, usually resulting from a missing route map in an IGP-to-BGP redistribution point. We're probably dealing with this type of leak when someone[^AM] [announces an additional 20.000 routes and revokes them a few minutes later](https://www.bgpmon.net/what-caused-todays-internet-hiccup/). Bonus points for style[^OBS] if those routes bring the [size of the global BGP table over a hardware limit of core Internet routers](https://labs.apnic.net/index.php/2014/09/30/whats-so-special-about-512/).

In the next blog posts in this series we'll discuss individual leak types and tools you can use to avoid them. In the meantime, read [RFC 7908](https://www.rfc-editor.org/rfc/rfc7908.html) and watch the *[Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security)* webinar.

[^AM]: hint: a service provider already mentioned in this blog post.

[^OBS]: ... and observability 😜