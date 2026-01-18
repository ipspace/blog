---
title: "OMG, After a Decade, VXLAN Is Still Insecure"
date: 2026-02-04 07:22:00+0100
tags: [ worth reading ]
---
In 2017 (over eight years ago), I was making fun of the fact that "[VXLAN is insecure](https://blog.ipspace.net/2018/11/omg-vxlan-is-still-insecure/)" was news to some people. Obviously, the message needed to be repeated, as the same author gave a [very similar presentation](https://troopers.de/downloads/troopers19/TROOPERS19_AR_VXLAN_Security.pdf) two years later at a security conference.

Unfortunately, it seems that everything old is new again (see also RFC 1925 rules 4 and 11), as proved by a "Using GRE and VXLAN for Fun and Profit" (my summary) [presentation at DEFCON 33](https://infocondb.org/con/def-con/def-con-33/from-spoofing-to-tunneling-new-red-teams-networking-techniques-for-initial-access-and-evasion). Even if you knew that unencrypted tunnels are insecure (duh!) for decades, you might still want to read the [summary of the talk](https://blog.apnic.net/2026/01/16/from-spoofing-to-tunnelling-new-red-team-networking-techniques-for-initial-access-and-evasion/) (published on APNIC blog) and [view the slides](https://i.blackhat.com/BH-USA-25/Presentations/USA-25-Tung-From-Spoofing-To-Tunneling-New.pdf).
