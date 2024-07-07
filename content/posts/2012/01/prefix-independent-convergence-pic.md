---
date: 2012-01-27 07:18:00+01:00
ospf_tag: mp
series_title: Fixing the FIB Bottleneck
tags:
- IS-IS
- OSPF
- service providers
- BGP
title: 'Prefix-Independent Convergence (PIC): Fixing the FIB Bottleneck'
url: /2012/01/prefix-independent-convergence-pic/
---
Did you rush to try OSPF Loop-Free Alternate on a Cisco 7200 after reading my [LFA blog post](/2012/01/loop-free-alternate-ospf-meets-eigrp/)... and disappointedly discovered that it only works on Cisco 7600? The reason is simple: while LFA does add feasible-successor-like behavior to OSPF, its primary mission is to improve RIB-to-FIB convergence time.
<!--more-->
If you want to know more details, I would strongly suggest you browse through the [IP Fast Reroute Applicability](http://www.data.proidea.org.pl/euronog/1edycja/materialy/prezentacje/Pierre_Francois_IP_Fast_Reroute_Applicability.pdf) presentation Pierre Francois had @ EuroNOG 2011. To summarize what he told us:

- It's relatively easy to fine-tune OSPF or IS-IS and get convergence times in tens of milliseconds. SPF runs reasonably fast on modern processors, more so with incremental SPF optimizations.
- A software-based switching platform can use the SPF results immediately (thus, there's no real need for LFA on a Cisco 7200).
- The true bottleneck is the process of updating distributed forwarding tables (FIBs) from the IP routing table (RIB) on platforms that use hardware switching. That operation can take a relatively long time if the router has to update many prefixes.

The generic optimization of the RIB-to-FIB update process is known as *Prefix-Independent Convergence (PIC)*. If the routing protocols can pre-compute alternate paths, suitably designed FIB can use that information to cache alternate next hops. Updating such a FIB no longer involves numerous updates to individual prefixes; you must change only the next-hop reachability information.

PIC was first implemented for BGP (you can find more details, including interesting discussions of FIB architectures, in [another presentation Pierre Francois had @ EuroNOG](http://www.data.proidea.org.pl/euronog/1edycja/materialy/prezentacje/Pierre_Francois_BGP_Add-Paths.pdf)), which usually carries hundreds of thousands of prefixes that point to a few tens of different next hops. It seems some Service Providers carry way too many routes in OSPF or IS-IS, so it also made sense to implement LFA for those routing protocols.

In its simplest form, BGP PIC goes a bit beyond exiting EBGP/IBGP multipathing and copies *backup path information* into RIB and FIB. Distributing alternate paths throughout the network requires numerous additional tweaks, from modified [BGP path propagation rules](/2021/12/bgp-multipath-addpath/) to [modified BGP route reflector behavior](/2021/10/bgp-optimal-route-reflection/).
