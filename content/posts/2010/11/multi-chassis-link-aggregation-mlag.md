---
date: 2010-11-01 07:02:00.005000+01:00
mlag_tag: implement
more_blurb: true
series:
- mlag
tags:
- link aggregation
- data center
title: External Brains Driving an MLAG Cluster
url: /2010/11/multi-chassis-link-aggregation-mlag.html
---
{{<note warn>}}The architecture described in this blog post is long gone, but it's worth remembering what vendors tried in the past and why it failed -- someone will inevitably try to sell an obsolete idea as the next best thing since sliced bread (see also RFC 1925 Rule 11){{</note>}}

Juniper has introduced an interesting twist to the *Stacking on Steroids* architecture: the brains of the box (control plane) are outsourced. When you want to build a *virtual chassis* (Juniper's marketing term for stack of core switches) out of EX8200 switches, you offload all the control-plane functionality (Spanning Tree Protocol, Link Aggregation Control Protocol, first-hop redundancy protocol, routing protocols) to an external box (XRE200).
<!--more-->
The resulting architecture is very similar to [Cisco's VSS](/2010/10/multi-chassis-link-aggregation-stacking.html), the major difference being that the internal routing engine in an EX8200 participating in a virtual chassis performs only the most rudimentary functions (chassis/linecard monitoring and maintenance).

{{<figure src="/2010/11/s400-MLAG_EX8200.png" caption="Juniper MLAG cluster with an external control plane">}}

Theoretically you could scale the *virtual chassis* architecture to numerous EX8200 switches behaving like a single data center fabric. From that perspective, the *virtual chassis* approach is way better than Cisco's VSS (which still looks like a hack to me). In reality, only two EX8200-series switches can be joined initially, making the *virtual chassis* a more expensive hack than the VSS (not only are you lobotomizing one supervisor module, you have to buy two more and lobotomize three out of four).

### The Nasty Details

Not surprisingly, Juniper's white paper[^GONE] is full of not-so-subtle hints comparing *virtual chassis* with VSS. For example: if the inter-switch link (Juniper's term: *intra-chassis link*) goes down, you don't lose half of your switching capacity (like you do with VSS). What they forget to mention is that the most common reason you'd lose a well-designed inter-switch link implemented as a port channel of multiple 10Gb connections terminated on different linecards is the failure of the supervisor module (in which case half of your switching capacity is dead anyway).

[^GONE]: No longer available on Juniper's web site, probably for a number of good reasons ;)

Furthermore, losing the inter-switch link between two Catalysts in a VSS system is equivalent to losing all the connections between the left- and right-hand sides in the above diagram, in which case the *virtual chassis* is at least as brain-dead as VSS (the whitepaper is curiously mum about that scenario). Another omission: when you lose the *intra-chassis link* between two EX8200 switches, hosts connected only to the left-hand switch (most probably) can no longer talk to hosts connected only to the right-hand switch.

Last but not least, when trying to compare apples to apples (which you can never expect a marketing whitepaper to do), we should also consider the extra power supplies, fans and other infrastructure needed in the XRE200 boxes.

Speaking of marketing misdirections, the [EX8200 Virtual Chassis Technology](http://www.juniper.net/us/en/local/pdf/fact-sheets-backgrounder/3000068-en.pdf) "fact sheet" has some "excellent" FUD:

> \[virtual chassis behavior at inter-switch link loss\] is a significant advancement over other vendors' solutions, where the loss of the intra-chassis link leads to complete loss in connectivity between any nodes (access switches or core routers) interconnected via the aggregation layer.

If you're unsure why that's a bogus claim, maybe it's time to watch the [*Data Center 3.0 for the Networking Engineers*](https://www.ipspace.net/DataCenterIntro) webinar ;)

### Summary

Due to the current limitations, the *virtual chassis* offers no clear advantages over Cisco's VSS or vPC solutions. However, the architecture (clean separation between control and data planes with numerous redundant paths between them) looks promising and once they manage to implement a reliable system beyond the two chassis, it might be an interesting solution.

### Revision History

2022-05-08
: Cleanup