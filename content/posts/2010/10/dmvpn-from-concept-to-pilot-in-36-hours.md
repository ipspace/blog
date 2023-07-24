---
date: 2010-10-07 10:13:00+02:00
dmvpn_tag: deploy
tags:
- DMVPN
title: 'DMVPN: from Concept to Pilot in 36 Hours'
url: /2010/10/dmvpn-from-concept-to-pilot-in-36-hours.html
---
Participants of my webinars might remember the concept of on-site workshops that I kept mentioning until the COVID-19 pandemic brought my in-person business to a halt. Almost a decade before that calamity, the networking team from a large multinational company had decided to test it in practice and invited me for a 3-day DMVPN workshop.

The agenda of these workshops is usually pretty simple:

-   Day 1: technology overview and review of the existing network design/challenges.
-   Day 2: work on proposed new network design.
-   Day 3: tying up loose ends and preparations for pilot/migration.

We agreed on a tentative agenda along these lines and I prepared the material for the technology overview using parts of my [*Choose the Optimal VPN Service*](https://www.ipspace.net/Choose_the_optimal_VPN_service) webinar (to compare DMVPN with other VPN solutions) and the [DMVPN](https://www.ipspace.net/DMVPN:_Advanced_and_Crazy_Scenarios) webinar. Oh boy, was I in for a surprise.
<!--more-->
The workshop started innocently enough with the introductions till we reached their network architect who "briefly" introduced the network. Their WAN network is very close to my dream design (BGP between major sites and IGP in the access layer), so we needed less than 30 minutes to walk through the relevant parts. It also turned out that they'd already attended my DMVPN webinar and knew a lot about IPSec and GRE. Obviously it was time for plan B.

We still went through the DMVPN materials, spending a lot of time with in-depth discussions that could never happen in time-limited open-enrollment webinar setting. In the afternoon we figured out where and how to use DMVPN in their existing network and they felt confident enough to start preparing the configurations for the pilot implementation.

This is where our remote lab capabilities came extremely handy: next morning I downloaded their existing router configurations onto a set of five routers (we just had to change interface names), got the relevant part of their network up and running in the lab and started modifying the configurations. After an intensive day full of gotchas and glitches we had Phase 2 DMVPN with spoke-to-spoke tunnels up and running. We also had well-documented step-by-step migration path, configuration templates and actual configurations of the routers participating in the pilot implementation.

After the dinner it was time to test our concepts: they took the configurations and started implementing changes in their production network. Half an hour later we had two DMVPN clouds (with hubs in two geographically distant locations) and new BGP neighbors up and running and the traffic was flowing over DMVPN tunnels (we left the old point-to-point tunnels active in case we'd have to do a roll back). We achieved what they expected to be a week's worth of efforts in two days, primarily thanks to the excellent preparation work they'd done.

Day 3: lots of in-depth technical discussions, ranging from QoS, BGP routing tweaks, partially-meshed Phase 2 DMVPN clouds, BGP policy templates... and they already started preparing router configurations for pilot deployment in the next region.

For me, this workshop was a fantastic deep-dive into DMVPN that exposed numerous aspects you never consider when talking about the technology. Thank you!!! (Obviously I can't mention any names, but you know who you are ;).
