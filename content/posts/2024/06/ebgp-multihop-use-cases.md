---
title: "Looking for a Simple Multihop EBGP Use Case"
date: 2024-06-26 08:23:00+0200
tags: [ BGP ]
---
I plan to add several challenge labs using multihop EBGP sessions to the [BGP labs project](https://bgplabs.net/), including:

1. Running BGP between VMs and central BGP route servers
2. Using multihop EBGP session to send full Internet routing table to a customer without overloading the PE-router
3. Running EBGP EVPN session between loopbacks advertised with EBGP IPv4 session (🤢)

However, I would love to start with a simple use case to help engineers unfamiliar with BGP realize when they might have to use multihop EBGP sessions. Unfortunately, I can't find one, and the scenarios where I used multihop EBGP in the past (EBGP load balancing and using a low-end router in the EBGP path, where I was effectively using the reverse application of #2 as a customer) are mostly irrelevant.

Would you have an easy-to-understand use case that is best solved with a multihop EBGP session? Please share it in the comments. Thanks a million!