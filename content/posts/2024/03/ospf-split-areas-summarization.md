---
title: "OSPF Summarization and Split Areas"
date: 2024-03-12 07:39:00+0100
tags: [ OSPF ]
ospf_tag: areas
---
In the [Do We Still Need OSPF Areas and Summarization?](https://blog.ipspace.net/2016/09/do-we-still-need-ospf-areas-and.html) I wrote this somewhat cryptic remark:

> The routers advertising a summarized prefix should be connected by a path going exclusively through the part of the network with more specific prefixes. GRE tunnel also satisfies that criteria; the proof is left as an exercise for the reader.

One of my readers asked for a lengthier explanation, so here we go. Imagine a network with two areas doing inter-area summarization on /24 boundary:
<!--more-->
{{<ascii>}}
┌────────────────────────────────┐          
│             Area 1             │          
│  ┌────────┐        ┌────────┐  │          
│  │   R1   ├────────┤   R2   │  │          
│  │10.0.0.1│        │10.0.0.2│  │          
│  └────┬───┘        └────┬───┘  │          
│       │                 │      │          
└─ ┌────┴───┐ ────── ┌────┴───┐ ─┘          
   │  ABR1  │        │  ABR2  │             
┌─ └────┬───┘ ────── └────┬───┘ ─┐         ┼
│       │                 │      │          
│       │   ┌────────┐    │      │          
│       └───┤  RTR   ├────┘      │          
│           └────────┘           │          
│             Area 0             │          
└────────────────────────────────┘          
{{</ascii>}}

This is what you should see if you got it configured correctly:

* ABR1 and ABR2 advertise 10.0.0.0/24 to RTR (inter-area summarization)
* ABR1 and ABR2 have a path to 10.0.0.1/32 and 10.0.0.2/32, and the path goes through Area 1.

No surprise there.

Now, imagine the R1-R2 link going down. ABR1 and ABR2 still have at least one prefix within the summarization range, so they keep advertising 10.0.0.0/24. If RTR chooses ABR1 to get to R2, the packet is dropped; ABR1 has no idea how to get to 10.0.0.2/32, and the summary prefix advertised into the backbone area is backed up with a route to the *null* interface to prevent forwarding loops.

Long story short: the network started blackholing traffic toward R1 and R2 because we lost the *path going exclusively through the part of the network with more specific prefixes.* Hope that makes the first part of the remark unambiguous. It's also not an OSPF-specific issue. Route summarization (regardless of the routing protocol you use) always results in information loss and potential suboptimal paths or black holes.

Now for the GRE part. Our woes have two root causes:

* ABR1 and ABR2 summarize prefixes from Area 1 into the backbone area.
* Area 1 is discontiguous (split into two fragments).

We must fix one of those root causes to make the network work. We could turn off summarization – ABR1 would advertise the R1 prefix into the backbone area, ABR2 would do the same for R2, and RTR would know which way to go. It's worth noting that OSPF works just fine with fragmented areas *as long as you're not using route summarization.*[^EFTR] 

[^EFTR]: The proof (as expected) is left as an exercise for the reader. Hint: google for "OSPF inter-area distance vector" ;)

We could also patch together the fragments of Area 1, and if we can't fix the R1-R2 link, we could build a GRE link between the ABRs *with tunnel endpoints in the backbone area* and put the tunnel into OSPF Area 1. [Duct tape applied](https://twitter.com/ioshints/status/10449562829328384), problem solved.

For completeness' sake, virtual links won't help you. They can be used to extend the backbone area but not as duct tape to patch together non-backbone areas.
