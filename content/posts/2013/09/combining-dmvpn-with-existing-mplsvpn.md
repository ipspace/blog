---
date: 2013-09-02 07:29:00+02:00
dmvpn_tag: deploy
ospf_tag: dmvpn
tags:
- design
- DMVPN
- OSPF
- BGP
- MPLS VPN
title: Combining DMVPN with Existing MPLS/VPN Network
url: /2013/09/combining-dmvpn-with-existing-mplsvpn/
---
One of the [Expert Express](http://www.ipspace.net/ExpertExpress) sessions focused on an MPLS/VPN-based WAN network using OSPF as the routing protocol. The customer wanted to add DMVPN-based backup links and planned to retain OSPF as the routing protocol. Not surprisingly, the initial design had all sorts of unexpectedly complex kludges (see the [case study](http://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN) for more details).

Having a really smart engineer on the other end of the WebEx call, I had to ask a single question: "Why don't you use BGP everywhere" and after a short pause got back the expected reply "wow... now it all makes sense."

{{<jump>}}
[Read more](http://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN)
{{</jump>}}
