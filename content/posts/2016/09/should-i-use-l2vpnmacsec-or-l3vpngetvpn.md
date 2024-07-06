---
date: 2016-09-15 08:08:00+02:00
dmvpn_tag: other
tags:
- design
- DMVPN
- WAN
title: Should I Use L2VPN+MACSEC or L3VPN+GETVPN?
url: /2016/09/should-i-use-l2vpnmacsec-or-l3vpngetvpn.html
---
Here are the outlines of an interesting [ExpertExpress](http://www.ipspace.net/ExpertExpress) discussion:

-   A global organization wanted to connect data centers across the globe with a new transport backbone.
-   All the traffic has to be encrypted.

Should they buy L2VPN and use MACsec on it or L3VPN and use GETVPN on it (considering they already have large DMVPN deployments in each region)?
<!--more-->
As always, the correct answer is *it depends,* in this case on how much you value SP independence versus performance, cost and equipment manufacturer independence.

{{<note warn>}}Please note that they were not looking for a highly secure solution. That requirement would totally change the conversation and I'd recommend they get in touch with [Christoph Jaggi](http://uebermeister.com/about.html) who knows infinitely more about that topic than I do.{{</note>}}

The first recommendation I made was *try to be as independent from your Service Provider as you can be*. In other words, don't go for a classic L3VPN where the SP owns your core routing (yes, I know that sounds weird coming from the guy who wrote several MPLS books).

There are (at least) two ways to achieve that goal:

-   Buy L2VPN and run traditional IP routing on top of it.
-   Buy L3VPN and build an overlay (CE-to-CE tunnels) on top of it. Don't run routing protocol with the SP but rely on PE-CE subnets for transport connectivity (an architecture recently [remarketed as SD-WAN](/2015/06/software-defined-wanwell-orchestrated.html)).

The beauty of the second approach: you can use it with every VPN service (or even across the Internet) from every SP worldwide, which puts your SP in an awkward spot during the contract negotiation.

{{<note>}}Not surprisingly, the customer's SP contacts strongly suggested staying with traditional L3VPN.{{</note>}}

Second recommendation: decide whether you want to use a single VPN design for your access and core networks (in which case go with DMVPN for the core network) or whether you want to optimize other criteria, for example:

-   Price/performance. High-speed MACsec is dirt cheap compared to IPsec or IP-over-GRE-over-IPsec-over-IP (= DMVPN).
-   Equipment vendor independence. Any router or firewall on the market supports point-to-point IPsec tunnels, and it's reasonably easy to build a multi-vendor solution, giving you more negotiation room when faced with expensive high-speed IPsec hardware from your beloved vendor. DMVPN locks you into Cisco.

Why would I even consider DMVPN for the core network? Because the customer already has extensive DMVPN operational experience, whereas anything else would introduce a learning curve.

Why did I totally ignore GETVPN? GETVPN was designed for a single (end-to-end) routing domain, for example securing customer (CE-to-CE) traffic in classic L3VPN deployment with PE-CE routing protocols, which would make it hard to change SPs on the fly.
