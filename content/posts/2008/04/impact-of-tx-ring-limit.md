---
date: 2008-04-30 07:34:00.001000+02:00
tags:
- QoS
- WAN
title: The Impact of tx-ring-limit
url: /2008/04/impact-of-tx-ring-limit/
---
Setting the [size of the hardware output queue in Cisco IOS](/kb/tag/QoS/Queuing_Principles/) with the (then undocumented) **tx-ring-limit** (formerly known as **tx-limit**) has been a big deal when I was developing the first version of the QoS course that eventually became the initial release of the *Implementing Cisco Quality of Service* training.

However, while it\'s intuitively clear that the longer hardware queue affects the QoS, years passed before I finally took the time to [measure the actual impact](/kb/tag/QoS/TX-Ring-Limit/).
