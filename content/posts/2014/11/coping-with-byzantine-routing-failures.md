---
cdate: 2023-03-10
comment: |
  [SD-WAN](/tag/sd-wan.html) is another solution to this challenge, and most startups working in this space (like Viptela) have been acquired by major networking or virtualization vendors.
date: 2014-11-19 08:41:00+01:00
high-availability_tag: infra
tags:
- IP routing
- MPLS VPN
- WAN
- high availability
title: Coping with Byzantine Routing Failures
url: /2014/11/coping-with-byzantine-routing-failures.html
---
One of my readers sent me an interesting challenge:

> We have two MPLS providers sending us default routes and it seems like whenever we have problem with SP1 our failover is not happening properly and actually we have to go in manually and influence our traffic to forward via another path.

Welcome to the wondrous world of [byzantine routing failures](http://en.wikipedia.org/wiki/Byzantine_fault_tolerance) ;)
<!--more-->
Let's recap what the problem is:

-   The customer uses two service providers (ISPs, MPLS/VPN providers -- doesn't really matter);
-   Both SPs announce aggregated prefixes (example: default route);
-   The aggregated prefix is not revoked when the SP has a bad-hair-day.

It might be that the primary provider is clueless enough to generate the default route on the PE-router without considering the state of the rest of the network (because they never read [this blog post](http://blog.ipspace.net/2011/09/responsible-generation-of-bgp-default.html)), in which case the problem cannot be solved with BGP (the ["shared fate" property of BGP](http://blog.ipspace.net/2014/08/fate-sharing-in-ip-networks.html) is broken due to localized default route origination).

In any case, there are two commonly used solutions when one cannot trust the routing provided by the SP (no surprise there):

-   Running your own routing protocol between your sites across an **overlay network** (example: DMVPN, potentially without the encryption part if you're running DMVPN across an MPLS/VPN infrastructure, or [something way more complex](http://blog.ipspace.net/2011/03/mplsvpn-over-gre-over-ipsec-does-it.html)). [SD-WAN](/tag/sd-wan.html) solutions are also in this category.
-   **Locally generated default route** based on IP SLA measurements (for example, pinging Google DNS or one or more root nameservers).

You'll find plenty of information on the overlay approach in the [DMVPN webinars](http://www.ipspace.net/DMVPN_trilogy), and I covered some aspects of multi-provider connectivity in the [Data Center Design Case Studies](http://www.ipspace.net/Data_Center_Design_Case_Studies) book. I also blogged extensively about individual components of the second solution, but don't have a comprehensive case study addressing it yet.

If you're excessively brave, augment the DMVPN solution with PFRv3 (the combo known under the marketing name Intelligent WAN) . It's also worth considering startups working in this space: [Border6 if you need a BGP-only solution](http://blog.ipspace.net/2014/10/border6-non-stop-internet-commercial.html) or [Viptela if you need end-to-end private WAN](http://blog.ipspace.net/2014/11/viptela-sen-hybrid-wan-connectivity.html) load balanced across both SPs.

And finally -- don't forget to read [Radia Perlman's take on routing with byzantine robustness](https://gnunet.org/sites/default/files/smli_tr-2005-146.pdf)
