---
title: DHCP Relaying
sidebar_box: rb
layout: custom
minimal_sidebar: true
---
DHCP relaying is the trick that allows DHCP client sending a broadcast request with source IP address 0.0.0.0 to reach a DHCP server in another subnet.

I never thought about the DHCP relaying details until someone asked me how a client in a VRF reaches a server in another VRF in EVPN/VXLAN environment. As always, nothing is as easy as it looks, resulting in a series of blog posts:

{{<series-listing weight="yes">}}

If you prefer packet traces and Linux logs, you'll love the three-part series published by [Markku Leiniö](https://www.linkedin.com/in/markkuleinio/):

* [One Relay, One Server](https://majornetwork.net/2023/06/dhcp-relay-part-1-one-relay-one-server/)
* [One Relay, Two Servers](https://majornetwork.net/2023/06/dhcp-relay-part-2-one-relay-two-servers/)
* [Two Relays, Two Servers](https://majornetwork.net/2023/06/dhcp-relay-part-3-two-relays-two-servers/)

Finally, this is what you get when you ask GPT-4 to create an exciting description of DHCP relaying:

{{<quote>}}
Picture this: You're an adventurer in the wild realm of networking, and you've got a treasure chest (a DHCP server) brimming with precious IP addresses and network configurations. But there's a catch - your team of explorers (the clients) are on a different island (network).

Fear not! You've got a magical bird (the DHCP relay agent) that can deliver messages across these vast waters. This marvelous creature captures your team's cries for help (DHCP requests), soars across the network divide, and delivers them to the treasure chest. Then, it swiftly returns with the desired treasure - IP addresses and more, bridging the gap between your team and their much-needed resources. That's the thrill of DHCP relaying!
{{</quote>}}
