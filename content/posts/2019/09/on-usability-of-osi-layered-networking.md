---
date: 2019-09-24 08:49:00+02:00
networking-fundamentals_tag: must
tags:
- networking fundamentals
- CLNP
title: On the Usability of OSI Layered Networking Model
url: /2019/09/on-usability-of-osi-layered-networking/
weight: 100
---
Two weeks ago I [replied to a battle-scar reaction to 7-layer OSI model](/2019/09/response-osi-model-is-lie/), this time I'll address a [much more nuanced view](https://rule11.tech/stop-using-osi/) from Russ White. Please read his article first (as always, it's well worth reading) and when you come back we'll focus on this claim:

> The OSI Model does not accurately describe networks.

Like with any tool in your toolbox, you can view the 7-layer OSI model in a number of ways. In the case of OSI model, it can be used:
<!--more-->
-   As a **framework** describing what functionality needs to be present in an end-to-end networking solution;
-   As a **recipe** on how to build a networking stack;
-   As a particular **implementation** of that recipe including LLC on Ethernet, CLNP on network layer, TP4 on transport layer...
-   As the **one true religion**
-   As a **religious tool** used to squash the infidels (= the ARPANET folks).

I always viewed OSI model as a **framework**. As I explained in [The Importance of Networking Layers](https://my.ipspace.net/bin/list?id=Net101#LAYERS) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar, you have to implement at least these functions in an end-to-end networking stack:

{{<figure src="/2019/09/s1600-Challenges-to-Solve.jpg">}}

Trying to implement all that functionality in a *large bowl of spaghetti-with-meatballs* approach results in a nightmare. It's much better to have an architecture where every layer in the architecture provides services to the layer above it while consuming services from the layer below it.

Having such an architecture allows you to group the functionality that needs to be implemented in manageable chunks. It also allows you to think about the optimal position of a particular function. For example, do you implement reliable transport on every hop, or do you use an end-to-end reliable transport protocol, or do you do a hybrid of both. As you probably know by now, there is no right answer. In this particular case, the best answer depends on the error rate of the underlying transmission medium.

From this perspective, I would view the OSI model (or an alternative, but I haven't seen one yet) as an indispensable high-level tool for anyone who tries to understand how networking works.

{{<note info>}}
Please read the [comments by Innokentiy](/2019/09/response-osi-model-is-lie/#c6658127076918961874) for a more nuanced view.
{{</note>}}

Unfortunately most critiques of the OSI model come from people who were either exposed to it when it was used as a religious tool, or from people who were exposed to the particular implementation I described above (or its connection-oriented alternative using CONS/X.25 instead of CNLP and TP0 instead of TP4).

Even that implementation wasn't as bad as the critics would have you believe. It gave us IS-IS (probably the most versatile IGP out there) as well as concepts like "*per-host addressing*" instead of "*per-interface addressing*" that [would nicely solve a number of stupidities](/2010/12/clnp-and-multihoming-myths/) we have to deal with today. Not surprisingly, we're reinventing that particular wheel with [layer-3-only forwarding](/2015/05/reinventing-clns-with-l3-only-forwarding/) and [IPv6 prefixes assigned to container hosts](/2017/09/coming-full-circle-on-ipv6-address/).

However, there is one serious omission in the OSI model (and I guess Russ and myself are in perfect agreement on this one) - the lack of recursive network layer, resulting in [angels-dancing-on-a-pin](https://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F) discussions of whether [MPLS is tunneling or not](/2011/10/mpls-is-not-tunneling/).

Internet Protocol (IP) was always designed to run across another subnetwork protocol (remember: the whole ARPANET was such a subnetwork), and that distinctive characteristic got lost in translation when someone collected various proven ideas and presented them as one-and-only solution (now I'm getting sarcastic, but you should be used to it by now). Some people [never stopped explaining that](http://csr.bu.edu/rina/KoreaNamingFund100218.pdf) but as always nobody was listening, because everyone knew the right answer... and left us the mess we still have to deal with decades later.

Can we change the fundamental architecture of the Internet? Probably not. Can we make it perform better? Sure... and we can start by understanding the characteristics and limitations of current networking technologies - something I'm trying to explain in [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.