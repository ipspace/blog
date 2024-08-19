---
title: "BGP Session and Address Family Parameters"
date: 2024-08-19 06:45:00+0200
tags: [ BGP ]
---
As I was doing the [final integration tests](https://blog.ipspace.net/2024/05/netlab-integration-tests/) for [netlab release 1.9.0](https://netlab.tools/release/1.9/#release-1-9-0), I stumbled upon a fascinating BGP configuration quirk: where do you configure the **allowas-in** parameter and why?

### A Bit of Theory

BGP runs over TCP, and all parameters related to the TCP session are configured for a BGP neighbor (IPv4 or IPv6 address). That includes the source interface, local AS number (it's advertised in the per-session OPEN message that negotiates the address families), MD5 password (it uses MD5 checksum of TCP packets), GTSM (it uses the IP TTL field), or EBGP multihop (it increases the IP TTL field).
<!--more-->
BGP can run multiple *address families* over a single TCP transport session. For example, you can run IPv4, VPNv4, VPNv6, and EVPN address families over the same TCP session (that's easy; [things can get way more complex](https://blog.ipspace.net/2022/01/bgp-af-nerd-knobs/)).

[Multiprotocol BGP](https://datatracker.ietf.org/doc/html/rfc4760) is sending updates *for individual address families* (using MP_REACH_NLRI or MP_UNREACH_NLRI), so you should apply any configuration parameter that changes or filters BGP updates (for example, route maps) to an address family, including changes to the AS_PATH attribute.

### Meanwhile on Planet Earth

Most vendors got the basics right -- route maps, prefix lists, and AS path filters (where available) are applied to BGP neighbors *within address families*.

Unfortunately, some vendors decided to implement shortcuts; for instance, on earlier Arista EOS releases, you [had to apply the **next-hop-self** parameter to a BGP neighbor](https://blog.ipspace.net/2022/10/arista-route-reflector-woes/), which changed how *all address families* behaved[^ERM]. You could also apply a route map directly to a BGP neighbor, which would apply the route map to all address families enabled for that neighbor[^TBS].

[^ERM]: As a workaround, you can change the BGP next hop in a route map and apply that route map to an individual address family. Arista fixed that quirk in the meantime.

[^TBS]: Hint: trying to be smart and taking a shortcut often ends badly 🤷‍♂️

What about changes to the AS path? The AS_PATH attribute is attached to individual multiprotocol BGP updates. Thus, the advertised or received AS path clearly belongs to a single address family and any AS path manipulation should be done there.

That's not how some engineers decided to implement BGP. Here's what I found on more than one platform[^CCT]:

* AS-path prepending is usually implemented in a route map that is applied to a neighbor within an address family.
* AS override (that modifies outgoing AS path in a slightly different manner than AS-path prepending) or removal of private AS numbers from the AS path are applied to a neighbor, not an address family.
* Disabling AS-path loop checks (*allowas-in*) is applied to individual address families and has to be applied to the EVPN address family if you want to use an EBGP-only design with the same BGP AS number on all leaf switches[^RT]

Just for the giggles: some platforms allow you to configure some AS-manipulation parameters only on the IPv4/IPv6 address families but not on (for example) the EVPN address family.

Isn't it great that an already arcane protocol got even more confusing?

[^RT]: That's what brought me down this rabbit trail.

[^CCT]: Want to know who does what? Check the [configuration templates](https://github.com/ipspace/netlab/tree/dev/netsim/extra/bgp.session) for the **[bgp.session](https://netlab.tools/plugins/bgp.session/)** _netlab_ plugin