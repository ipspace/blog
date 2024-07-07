---
date: 2010-03-18 07:29:00.004000+01:00
tags:
- IS-IS
- CLNP
title: CLNS and CLNP
url: /2010/03/clns-and-clnp/
---
Yap Chin Hoong has been looking at the [OSI protocol stack](/2009/06/is-is-is-not-running-over-clnp/) I've published and asked an interesting question: "*where is CLNS in that protocol stack?*"

The OSI protocol stack has a major advantage over the TCP/IP stack: it defines both the protocols and the APIs between the layers. CLNS (Connection-less network Service) is the API (the function calls that allow transport layers to exchange datagrams across the network) while CLNP (Connection-less network Protocol) is the layer-3 protocol that implements CLNS. In [my diagram](/2009/06/is-is-is-not-running-over-clnp/), CLNS would be a thin line above CLNP between L3 and L4 boxes.

{{<note>}}IOS developers did not escape the confusion between CLNS and CLNP. The **clns routing** command does not make sense; you cannot route an API. The command should have been called **clnp routing**.{{</note>}}
