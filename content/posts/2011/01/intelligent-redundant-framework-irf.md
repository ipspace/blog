---
date: 2011-01-24 06:56:00.007000+01:00
mlag_tag: implement
series:
- mlag
tags:
- link aggregation
- switching
title: Intelligent Redundant Framework (IRF) – Stacking as Usual
url: /2011/01/intelligent-redundant-framework-irf/
---
When I was listening to the Intelligent Redundant Framework (IRF) presentation from HP during the Tech Field Day 2010 and read the [HP/H3C IRF 2.0 whitepaper](http://www.h3c.com/portal/download.do?id=1027834) afterwards, IRF looked like a technology sent straight from Data Center heavens: you could build a single unified fabric with optimal L2 and L3 forwarding that spans the whole data center (I was somewhat skeptical about their multi-DC vision) and behaves like a single managed entity.

No wonder I started drawing the following highly optimistic diagram when creating materials for the [Data Center 3.0](https://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) webinar, which includes information on Multi-Chassis Link Aggregation (MLAG) technologies from numerous vendors.
<!--more-->
{{<figure src="/2011/01/s320-irf.png" caption="Oversimplified HP IRF design">}}

However, the worm of doubt was continuously nagging somewhere deep in my subconsciousness, so I decided to check the configuration guides of various HP switches (kudos to HP for the free and unrestricted access to their very good documentation). I selected a core switch (S12508) and an access-layer switch (S5820X-28S) from the HP IRF technology page[^NOLINK], downloaded their configuration guides and studied the IRF chapters. What a disappointment:

[^NOLINK]: Had to remove the links to HP web sites when cleaning up this article in May 2022 -- HP can't be bothered to have valid TLS certificates on their web sites. If you really want to find those links, search through the commit history on [ipSpace.net blog repository](https://github.com/ipspace/blog).

-   **Only devices of the same series can form an IRF**. How is that different from any other stackable switch vendor?
-   **Only two core switches can form an IRF**. How is that different from [Cisco's VSS](/2010/10/multi-chassis-link-aggregation-stacking/) or [Juniper's XRE200](/2010/11/multi-chassis-link-aggregation-mlag/)?
-   **One device in the IRF is the master, others are slaves**. Same as Cisco's VSS.
-   **Numerous stackable switches can form an IRF**. Everyone else is calling that a stack.
-   **IRF partition is detected through proprietarily modified LACP or BFD.** Same as Cisco's VSS.
-   **After IRF partition, the loser devices block their ports.** The white paper is curiously mum about the consequences of IRF partition. No wonder, IRF does the same thing as any other vendor -- the losing part of the cluster blocks its ports following a partition.

There might be something novel in the IRF technology that truly sets it apart from other vendors' solutions, but I haven't found it. For the moment, IRF looks like stacking-as-usual to me; if I got it wrong, please chime in with your comments.

### More information

Numerous MLAG technologies, including Cisco's VSS and vPC, Juniper's XRE200 and HP's IRF are described in the [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30) webinar.
