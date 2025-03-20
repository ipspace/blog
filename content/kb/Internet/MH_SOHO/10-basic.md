---
kb_section: MH_SOHO
minimal_sidebar: true
title: Basic Small Site Multi-Homing
alt_section: posts
---
Connecting a small site to multiple service providers can be extremely easy – you get two upstream links and two provider-assigned (PA) IPv4 addresses (static or dynamically assigned). Since each ISP will give you only a single IPv4 address, you have to use private IPv4 addresses on the LAN side of the router (Figure 1).

{{<figure src="/kb/Internet/MH_SOHO/MultihomedSOHO_1.jpg" caption="IP addressing in small multi-homed site" width="500">}}

Most ISPs are unwilling to run a dynamic routing protocol with small sites, so you must configure static default routing on your router. Since you would almost always prefer one provider over the other, you would create a primary and a backup default route.

{{<figure src="/kb/Internet/MH_SOHO/MultihomedSOHO_2.jpg" caption="Static default routing" width="500">}}

{{<note>}}With careful configuration, it’s also possible to achieve rudimentary load sharing with two equally good default routes.
{{</note>}}

The router on the remote site would also have to perform two independent NAT translations, one for packets sent to ISP A (where local addresses get translated to the IP address assigned by ISP A) and another for packets sent to ISP B (Figure 3).

{{<figure src="/kb/Internet/MH_SOHO/MultihomedSOHO_3.jpg" caption="NAT translation in small multi-homed site" width="500">}}

One of the significant issues in multi-homed site design is the proper handling of the return traffic. It’s not uncommon to experience performance problems if the outbound and return traffic flow over different links (also known as asymmetrical routing), while IP multicast and stateful packet inspection (part of the Cisco IOS firewall feature set) almost always break under these conditions. Fortunately, asymmetrical routing is never a problem in a dual NAT design (see the above diagram), as the source address of the outbound packet indicates the link that has been used to send it:

{{<figure src="/kb/Internet/MH_SOHO/MultihomedSOHO_4.jpg" caption="Symmetrical routing with dual NAT" width="500">}}
