---
title: "History of IP TTL in EBGP Sessions"
date: 2023-03-02 07:16:00
tags: [ BGP ]
---
[Chris Parker](https://www.networkfuntimes.com/about/) wrote a [wonderful blog post](https://www.networkfuntimes.com/your-multihop-bgp-session-probably-isnt-multi-hop/) going deep into the weeds on how EBGP sessions use IP TTL and why we need multihop EBGP sessions between adjacent devices. However, he couldn't find a source explaining why early BGP implementations decided to use IP TTL set to one on EBGP sessions:

> If there's a source on the internet that explains when it was decided that EBGP should use a TTL of 1, I can't find it. I can't even find it in any RFC. I looked in the RFC for BGP v4, and went all the way back to BGP v1. None of these documents contain the text "TTL or "time to live" or "time-to-live." It's not even in the RFC for EGP, back in 1984.
<!--more-->
I wasn't close to Cisco Engineering in the early 1990s, and the discussions I had with TAC engineers when teaching my BGP course at Cisco Europe never went in that direction, so the best I can offer is an educated guess based on how we used BGP in those days.

As I explained in the [Why Do We Need IBGP Full Mesh](/2022/10/ibgp-full-mesh/) blog post, BGP creators assumed we'd use BGP like this:

-   EBGP would propagate IP prefixes between autonomous systems (AS).
-   Edge routers would redistribute EBGP routes into IGP. IGP would propagate *those same prefixes* within each AS.
-   Edge routers would use IBGP solely to propagate other policy attributes (AS-path and friends) *across* an autonomous system.

Early BGP implementations contained mechanisms like BGP synchronization that enforced these assumptions -- an IBGP route would not be valid (and thus not propagated to EBGP neighbors) unless it had an exact IGP match in the IP routing table.

BGP synchronization ensured that all routers within an autonomous system had the same set of IP prefixes. There was no such mechanism between autonomous systems and network practitioners[^NP], having no clue how BGP works[^STNC], sometimes tried to insert additional routers between EBGP speakers, resulting in a phenomenal black hole[^PLER].

The easiest way to stop unintentional stupidities[^SIS] was to set IP TTL in EBGP packets to one -- having a layer-3 device in the path between EBGP speakers would ensure the BGP routers couldn't establish the EBGP session. Even if an overly-creative network practitioner tried to fool BGP routers and used the same IP subnet[^JS] on both ends of the intermediate device, EBGP session wouldn't start. If you insisted on using such a design, you had to turn a nerd knob, which was an immediate red flag for anyone familiar with BGP[^TAC] telling them something funky was going on.

**Long story short**: I suspect the original use case for EBGP TTL=1 was enforcing sane designs, not BGP session security.

[^NP]: It might not be fair to call them engineers. Also, I was one of them.

[^STNC]: Some things never change

[^PLER]: The proof is left as an exercise for the reader

[^SIS]: It's impossible to stop intentional stupidities because the fools are so ingenious.

[^JS]: Or mismatched subnet masks for increased job security

[^TAC]: For example, an unfortunate TAC engineer working on a "_BGP is broken in Cisco IOS_" ticket.
