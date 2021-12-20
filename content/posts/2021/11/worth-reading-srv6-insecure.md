---
title: "Soap Opera: SRv6 Is Insecure"
date: 2021-11-06 07:11:00
tags: [ IPv6, security, worth reading ]
---
I heard about SRv6 when it was still on the drawing board, and my initial reaction was "_Another attempt to implement source routing. We know how that ends._" The then-counter-argument by one of the proponents went along the lines of "_but we'll use signed headers to prevent abuse_" and I thought "_yeah, that will work really well in silicon implementations_".

Years later, [Andrew Alston decided to document the state of the emperor's wardrobe](https://mailarchive.ietf.org/arch/msg/v6ops/GbWiie-bjQ_Bp1JKB1PlDh_fPdc/) (TL&DR: of course SRv6 is insecure and can be easily abused) and the counter-argument this time was "_but that applies to any tunnel technology_". Thank you, we knew that all along, and that's not what was promised.

You might want to browse the rest of that email thread; it's fun reading unless you built your next-generation network design on SRv6 running across third-party networks... which was another PowerPoint case study used by SRv6 proponents.
