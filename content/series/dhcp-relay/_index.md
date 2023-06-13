---
title: DHCP Relaying
sidebar_box: rb
layout: custom
minimal_sidebar: true
---
I never thought about DHCP relaying details until someone asked me how a client in a VRF reaches a server in another VRF in EVPN/VXLAN environment. As always, nothing is as easy as it looks, resulting in a series of blog posts:

{{<series-listing weight="yes">}}

If you prefer packet traces and Linux logs, you'll love the three-part series published by [Markku Leiniö](https://www.linkedin.com/in/markkuleinio/):

* [One Relay, One Server](https://majornetwork.net/2023/06/dhcp-relay-part-1-one-relay-one-server/)
* [One Relay, Two Servers](https://majornetwork.net/2023/06/dhcp-relay-part-2-one-relay-two-servers/)
* [Two Relays, Two Servers](https://majornetwork.net/2023/06/dhcp-relay-part-3-two-relays-two-servers/)
