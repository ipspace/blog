---
title: "Interesting: BGP Zombie Outbreak on Juniper Routers"
date: 2023-04-30 06:54:00
tags: [ BGP ]
---
BGP zombies are routes in the BGP table that refuse to disappear even though they should have been long gone. [Recent measurements](https://storage.googleapis.com/site-media-prod/meetings/NANOG87/4692/20230215_Manassakis_Bgp_Zombies_-_v1.pdf) estimate between 0.5% and 1.5% of all routes in the global BGP table are zombies, which sounds crazy -- after all, BGP is supposed to be pretty reliable.

Daryll Swer identified one potential source -- Juniper routers do not revoke suppressed aggregated prefixes -- and documented it in *[Navigating a BGP zombie outbreak on Juniper routers](https://blog.apnic.net/2023/04/13/navigating-a-bgp-zombie-outbreak-on-juniper-routers/)*.
