---
title: "Worth Watching: Rethinking BGP in the Data Center"
date: 2021-05-23 06:16:00
tags: [ data center, design, BGP ]
---
Ever since [draft-lapukhov](https://datatracker.ietf.org/doc/html/draft-lapukhov-bgp-routing-large-dc-00) was first published almost a decade ago, we all knew BGP was the only routing protocol suitable for data center networking... or at least Thought Leaders and vendor marketers seem to be of that persuasion.
<!--more-->
Russ White[^1] argued[^2] that's not the case, dived deep into what the true requirements are, and showed how link-state protocols do a better job if only we fix the flooding behavior[^3].

In the meantime, while many hyperscalers moved beyond BGP-as-the-only-tool mantra, all major data center switching vendors keep promoting [EBGP-over-EBGP or IBGP-over-EBGP EVPN designs](https://blog.ipspace.net/2019/11/the-evpn-dilemma.html), proving yet again how the whole networking industry behaves like fashion designers on a lemming run chasing the latest fad.

{{<jump>}}[Watch the video](https://www.youtube.com/watch?v=pwxuhh7UIrU){{</jump>}}

[^1]: Contrary to the above-mentioned gentlemen, Russ has real-life design and operations experience.

[^2]: In 2018 when he was still at LinkedIn and developing OpenFabric, so he might have been a bit biased.

[^3]: Warning: Google will try its very best to track you if you decide to watch Russ' presentation.
