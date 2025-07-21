---
title: "Ultra Ethernet: Reinventing X.25"
date: 2025-07-23 08:06:00+0200
tags: [ data center ]
---
One should never trust the technical details published by the *industry press*, but assuming the [Tomahawk Ultra puff piece](https://www.nextplatform.com/2025/07/17/broadcom-tries-to-kill-infiniband-and-nvswitch-with-one-ethernet-stone/) isn't too far off the mark, the new Broadcom ASIC (supposedly loosely based on emerging Ultra Ethernet specs):

1. Uses *Optimized Ethernet Header*, replacing IP/UDP header with a 10-byte something (let's call it *session identifier*)
2. Makes Ethernet lossless with hop-by-hop retransmission/error recovery
3. Uses credit-based flow control (the receiver continuously updates the sender about the amount of available space)

If you're ancient enough, you might recognize #3 as part of Fibre Channel, #2 and #3 as part of IEEE 802.1 LLC2 (used by IBM to implement SNA over Token Ring and Ethernet), and all three as the fundamental ideas of X.25 that Broadcom obviously reinvented at 800 Gbps speeds, proving (yet again) RFC 1925 Rule 11.