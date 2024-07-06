---
title: "MPLS/LDP Creation Myths"
date: 2022-03-22 08:05:00
tags: [ MPLS ]
---
Hannes Gredler wrote an [interesting comment](/2022/03/hub-spoke-ldp-segment-routing.html#1077) to my _[Segment Routing vs LDP in Hub-and-Spoke Networks](/2022/03/hub-spoke-ldp-segment-routing.html)_ blog post:

> In 2014 when I did the first prototype implementation of MPLS-SR node labels, I was stunned that just with an incremental add of 500 lines of code to the vanilla IPv4/IPv6 IS-IS codebase I got full any-to-any connectivity, no sync issues, no targeted sessions for R-LFA .... essentially labeled transport comes for free. 

Based on that, one has to wonder "*why did we take the LDP detour and all the complexity it brings?*". Here's what Hannes found out:
<!--more-->
> Later I did ask George Swallow and Yakov Rekhter (The original MPLS design team) "Why did you not do this right from the start ?" and the answer was not pretty: "IGPs have been done in San Jose and the MPLS design team was mostly located in the Boxborough office. At the time there was lots of stability issues with IGPs and management has asked us not to touch any IGP code"

The reality is a bit more complex than that. Tag switching (later MPLS) was an extremely niche technology until MPLS/VPN made it popular, and was used to integrate ATM switches with IP routers. Here's what Henk Smit [had to say on the topic](/2022/03/hub-spoke-ldp-segment-routing.html#1083):

> The issue is much simpler. UUnet and iMCI were designing their new backbones with routers at the edge, and all Fore ATM switches in the middle. That was a $100M market that cisco was losing out on. At the same time, Ipsilon came with their proprietary technology with some flow-based, connection-oriented, doing IP-packet switching over ATM circuits. Lots of people at ISPs (and even at the IETF) loved the idea of having circuits. Old telephone people never change.
>
> So Yakov came with MPLS (first called tag-switching). It was basically the idea of using connections (LSPs) to compete with Fore and Ipsilon. And nobody thought of doing "connectionless labels". That is how we ended up with LDP and TE-RSVP. Because the people who made the purchasing decisions, and the VCs that invested in new technology, all wanted connection-oriented technology. 

Considering MPLS was targeting ATM switches (P-routers) with IP routers (PE-routers) connected to them there were a few "minor" details:

* ATM label space was limited
* ATM switches required per-interface label space (that's how ATM hardware works)
* The downstream-on-demand label allocation was thus the only way to make it work reasonably well.
* Independent label control was out of question -- an ATM switch could not process IP packets at any reasonable speed.

Now you know why TDP/LDP have a gazillion of label allocation modes.

Also, SR-MPLS works well with a single link-state IGP. Route redistribution between multiple routing protocols would kill that idea. Implementing SR-MPLS in EIGRP or BGP might be _doable_ but there's a reason we're not doing it -- things are simpler if you have full visibility into network topology. Staying away from the routing protocol complexity and allocating labels to the survivors that managed to fight their way into the forwarding table was probably the easiest way to get the job done.

But wait, there's more. I love joking about the $0.02 CPUs networking vendors put into data center switches. ATM switches were much worse. When Cisco bought StrataCom (a maker of rack-size ATM switches) and wanted to deploy Tag Switching on that hardware they couldn't make it work without attaching external brains (a 7200-series router) to the ATM switch[^EX9200]. Considering all that, one could relate to the "_don't touch IGP code_" sentiment, and so we were stuck with an ugly workaround and a favela of kludges built on top of that for the next three decades.

[^EX9200]: If that reminds you of the tricks [Juniper used trying to keep EX8200 switches relevant](/2010/11/multi-chassis-link-aggregation-mlag.html). RFC 1925 Rule 11 strikes again.