---
date: 2021-09-08 07:22:00+00:00
dmvpn_tag: alternative
lastmod: 2021-09-26 14:48:00
tags:
- DMVPN
title: Open-Source DMVPN Alternatives
---
When I started collecting topics for the September 2021 ipSpace.net Design Clinic one of the subscribers sent me an interesting challenge: are there any open-source alternatives to Cisco's DMVPN?

I had no idea and posted the question on Twitter, resulting in numerous responses pointing to a half-dozen alternatives. Thanks a million to [@MarcelWiget](https://twitter.com/MarcelWiget/status/1432391938569814016), [@FlorianHeigl1](https://twitter.com/FlorianHeigl1/status/1432393573744402441), [@PacketGeekNet](https://twitter.com/packetgeeknet/status/1432395175263932420), [@DubbelDelta](https://twitter.com/dubbeldelta/status/1432398847393816581), [@Tomm3h](https://twitter.com/tomm3h/status/1432399630499713026), [@Joy](https://twitter.com/joy/status/1432400041289781248), [@RoganDawes](https://twitter.com/RoganDawes/status/1432401266592911361), [@Yassers_za](https://twitter.com/yassers_za/status/1432413744882147330), [@MeNotYouSharp](https://twitter.com/menotyousharp/status/1432416495544504325), [@Arko95](https://twitter.com/arko95/status/1432435935782834184), [@DavidThurm](https://twitter.com/davidthurm/status/1432436541167652864), Brian Faulkner, and several others who chimed in with additional information.

Here's what I learned:
<!--more-->
## As Close As You Can Get to DMVPN

* VyOS implemented DMVPN, and you can [run a DMVPN network without Cisco routers](https://github.com/nirinarisantatra/DMVPN).
* OpenNHRP is a compliant open-source implementation available for (at least) Alpine Linux, VyOS, OpenWrt, and Ubuntu.
* Alpine Linux *had [DMVPN support](https://wiki.alpinelinux.org/wiki/Dynamic_Multipoint_VPN_(DMVPN)) since ages*.
* [FRR has NHRP](https://docs.frrouting.org/en/latest/nhrpd.html#) and [can create shortcut tunnels](https://docs.frrouting.org/en/latest/nhrpd.html#clicmd-ip-nhrp-shortcut) over mGRE.

## Alternatives

* I was told [Zerotier](https://www.zerotier.com/) could do routing or bridging, so it could be a DMVPN replacement. Have to dig deeper into the docs.

## Almost There

* [Tailscale](https://tailscale.com/) is a WireGuard-based VPN with centralized (closed-source) control plane, so technically it doesn't count.
* [Headscale](https://github.com/juanfont/headscale) is an open-source implementation of Tailscale coordination server (control plane)
* [Nebula](https://github.com/slackhq/nebula/blob/master/README.md) -- seems to be a host-based implementation of an overlay subnet. However, you should be able to add a routing protocol on top of it and route between Linux interfaces. 
* [Tinc-VPN](https://www.tinc-vpn.org/) is another host-based overlay VPN solution with the ability to bridge Ethernet segments over VPN. What could possibly go wrong with that? Being a bit more creative, one could use it the same was as Nebula to route between LAN segments and overlay network.
* [Innernet](https://blog.tonari.no/introducing-innernet) is a configuration system on top of WireGuard. It looks like I'll have to figure out what WireGuard does as well ;)
* [Netmaker](https://netmaker.readthedocs.io/en/master/) is another WireGuard management system.
* [OpenOverlayRouter](https://openoverlayrouter.org/) is a LISP+VXLAN implementation. In theory you should be able to run IP routing on Linux nodes to implement something like DMVPN.

Have we missed something? Would you like to add more details? Please write a comment (and yes, it's perfectly fine to post links to product documentation ;).

## Revision History

2021-09-26
: Added links to Headscale and Netmaker (thanks to Brian Faulkner)