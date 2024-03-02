---
title: "netlab 1.8.0: Control-Plane Daemons, BIRD, dnsmasq"
series_title: "Control-Plane Daemons, BIRD, dnsmasq (Release 1.8.0)"
date: 2024-03-04 08:25:00+01:00
tags: [ netlab ]
netlab_tag: release
---
I wanted to include open-source networking-related software into _netlab_ topologies since (at least) the days I was writing the [DHCP relaying saga](https://blog.ipspace.net/series/dhcp-relay.html). It turned out to be a bit more complex than I anticipated (more about that in another blog post), but I hope you'll find it useful. [_netlab_ release 1.8.0](https://netlab.tools/release/1.8/) includes [*dnsmasq* running as a DHCP server](https://netlab.tools/platforms/#platform-daemons) and BIRD [running OSPF and BGP](https://netlab.tools/caveats/#bird-internet-routing-daemon). ExaBGP and GoBGP are already on the wish list; if you have any other ideas, please start a GitHub discussion.

I had a hard time finding reasonable container images for BIRD;  the BIRD team does not publish them, and everything else I found looked either abandoned or a hobby project. The solution turned out to be exceedingly simple: you cannot run the containers without Docker anyway, which means the **docker build** command is just a few keystrokes away. I added *Dockerfiles* needed to build those containers to the *netlab* source code and implemented the **netlab clab build** command as a thin wrapper around **docker build**. It takes just a few seconds (plus the time it takes to download the Ubuntu container image) to build the containers you need.
<!--more-->
Talking about DHCP: release 1.8.0 added [DHCP clients, relays, and servers](https://netlab.tools/module/dhcp/). You can also use inter-VRF relays on Cisco IOS and Arista EOS and a VRF-aware DHCP server on Cisco CSR 1000v (I couldn't find any other DHCP server supporting [RFC 6607](https://www.rfc-editor.org/rfc/rfc6607.html)).

Release 1.8.0 includes a bunch of other nifty features:

-   [BGP configuration module](https://netlab.tools/module/bgp/#module-bgp) supports 4-octet BGP AS numbers and [large BGP communities](https://netlab.tools/module/bgp/#bgp-community-propagation).
-   [Validation plugins](https://netlab.tools/topology/validate/#validate-plugin) allow you to write more powerful [validation tests](https://netlab.tools/topology/validate/) without creating complex Jinja2 templates
-   [IBGP sessions](https://netlab.tools/module/bgp/#bgp-ibgp-sessions) to routing daemons running on Linux VMs or containers can be established with external-facing IP addresses (not just remote loopbacks).
-   You can set [*netlab* defaults](https://netlab.tools/defaults/#defaults) from the [environment variables](https://netlab.tools/defaults/#defaults-env)
-   [Configuration template search paths and filenames](https://netlab.tools/dev/config/deploy/#dev-config-deploy-paths) are no longer hardcoded. Most can be configured in [system defaults](https://netlab.tools/defaults/#defaults) using **defaults.paths** dictionary.

Finally, I've thrown in a last-minute feature you might find somewhat useful: **netlab up** command can [reload saved device configurations](https://netlab.tools/netlab/up/#netlab-up-reload) instead of starting the initial device configuration process from scratch.

### Upgrading or Starting from Scratch

* For more details, [read the release notes](https://netlab.tools/release/1.8/#release-1-8-0).
* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
