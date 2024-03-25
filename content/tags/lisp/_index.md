---
title: LISP
page_title: Locator/ID Separation Protocol (LISP)
minimal_sidebar: true
layout: custom
---
[LISP](https://en.wikipedia.org/wiki/Locator/Identifier_Separation_Protocol) is a networking technology that has been searching for a relevant problem for a decade and a half (the LISP IETF working group started in the spring of 2009). Initially, I was cautiously optimistic. However, as LISP pivoted from an IPv6-over-IPv4 solution to a multihoming solution, then VM mobility and IP endpoint mobility solution, until it finally landed in Cisco Campus BU as the foundational technology of Software-Defined Access, I lost all hope.

LISP started as a DNS-like cache-based packet forwarding technology. Eventually, reality intervened, and the LISP believers rediscovered the flaws of cache-based forwarding. It looks like LISP pivoted to become a topology-driven PUB-SUB protocol. Assuming that's correct, there's little conceptual difference between LISP and EVPN. It's just a question of defining a suitable set of policy mechanisms and developing an optimal implementation.

Discussing the benefits and drawbacks of LISP or EVPN thus makes as much sense as debating the [number of angels dancing on the head of a pin](https://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F), but that has never stopped people from doing one or the other.

Just in case you want to know more, you will find some details in the LISP-related blog posts I wrote since 2010:

{{<series-listing year="sure">}}
