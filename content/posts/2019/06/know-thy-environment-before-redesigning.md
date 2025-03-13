---
date: 2019-06-03 07:21:00+02:00
tags:
- design
- WAN
title: Know Thy Environment Before Redesigning It
url: /2019/06/know-thy-environment-before-redesigning/
---
A while ago, I had an interesting [consulting engagement](https://www.ipspace.net/ExpertExpress): a multinational organization wanted to migrate off global Carrier Ethernet VPN (with routers at the edges) to MPLS/VPN.

While that sounds like the right thing to do (after all, L3 must be better than L2, right?), in that particular case, they wanted to combine the provider VPN with an Internet-based IPsec VPN. Doing that in parallel with MPLS/VPN tends to become an interesting exercise in "*[how convoluted can I make my design before I give up and migrate to BGP](https://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN)*."
<!--more-->
As we analyzed their options and potential designs, I became convinced that it makes no sense to [give the keys to the kingdom (core routing protocols) to a third party](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)... but still wondered whether they were dealing with a horrible service provider (in which case switching the provider would make sense).

They mentioned frequent outages, so I tried to put that claim in perspective. We eventually figured out they would have a link failure (detected as routing protocol adjacency loss) every week... in a network with approximately 100 sites. I know that my conclusions would probably make [Rachel Traylor](https://www.ipspace.net/Author:Rachel_Traylor) extremely upset, but using a rule of thumb, I converted that into "a link fails on average once in 100 weeks... or once in two years". It was not exactly a stellar performance, but it was not catastrophic either.

It was interesting to discover that links don't fail very often, but they could still be dealing with gray failures. So, I asked them to deploy BFD and track BFD errors over several weeks. The result was tons of BFD errors, so maybe the Service Provider was the root cause of their problems.

Another quick check: BFD timers. They set aggressive timers, and it seemed that BFD packets got stuck behind large bursts of user traffic in output queues on Service Provider switches. After increasing the BFD timer to 300 msec, BFD errors disappeared almost completely, proving that (A) the links were pretty reliable but (B) also experiencing periods of significant congestion.

Ultimately, the customer made no significant changes apart from minor cleanups of their core routing configuration. However, they understood the network behavior much better than before and had data to back up their decisions.

### More Information

I did a webinar [describing various VPN services from architecture- and technology perspectives](https://www.ipspace.net/Choose_the_Optimal_VPN_Service).
