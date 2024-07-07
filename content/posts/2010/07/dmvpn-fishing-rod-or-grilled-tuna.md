---
date: 2010-07-05 14:51:00.006000+02:00
dmvpn_tag: other
tags:
- DMVPN
- workshop
- IPsec
title: 'DMVPN: Fishing Rod or Grilled Tuna?'
url: /2010/07/dmvpn-fishing-rod-or-grilled-tuna/
---
Last days I was eating, drinking, breathing and dreaming DMVPN as I was preparing lab scenarios for my DMVPN webinar (the participants will get complete router configurations for 12 different scenarios implemented in an 8-router fully redundant DMVPN network).

Some of the advanced scenarios were easy; for example, I've found a passing reference to passive RIPv2 with IP SLA in the _DMVPN/GETVPN Design & Case Study_ presentation (lost in the mists of time). I knew exactly what the author had in mind and was able to create a working scenario in minutes. Unfortunately, 2-tier hub site with IPSec offload was a completely different beast.
<!--more-->
It all started with the innocently-looking _Large Scale DMVPN Deployment design guide_ (now long gone). The categorization (*design guide*) is a clear misnomer: the document is a type-me-in recipe. If your environment closely matches the described setup, that just might be all you need. However, the recipe probably relies heavily on crypto engine implementation particular to the Cisco 7600 platform and I was unable to make it work on a 7200 platform (I will leave the reasons for my preference of the 7200 platform up to your imagination). My lack of IPSec wizardry skill didn't help either.

Anyhow, after 6 hours of head-banging (helped immensely by large dose of misconfiguration) I was able to reverse-engineer the design, make it work and describe its step-by-step requirements (it took me seven slides and I tried to keep it short and simple)... which brings me to the title of this post. What would you prefer: getting a grilled tuna (= a configuration recipe where you have no clue how it was made and why it works so well) or a fishing rod and a tuna-catching lesson? When considering the answer, keep in mind that you just might have to maintain, troubleshoot and modify this particular tuna school in the future.
