---
title: "OMG, Not Again: New Mobile Internet Protocol Vulnerabilities"
date: 2020-07-29 07:20:00
tags: [ security, worth reading ]
---
Every now and then a security researcher "discovers" a tunneling protocol designed to be used over a protected transport core and "declares it vulnerable" assuming the attacker can connect to that transport network... even though the protocol [was purposefully designed that way](/2015/04/omg-vxlan-encapsulation-has-no-security/), and everyone with a bit of clue knew the whole story years ago (and/or it's even [documented in the RFC](https://tools.ietf.org/html/rfc7348#section-7)).

It was MPLS decades ago, then [VXLAN a few years ago](/2018/11/omg-vxlan-is-still-insecure/), and now someone "found" a ["high-impact vulnerability" in GPRS Tunnel Protocol](https://thehackernews.com/2020/06/mobile-internet-hacking.html). Recommended countermeasures: whitelist-based IP filtering. Yeah, it's amazing what a wonderful new tool they found.

Unfortunately (for the rest of us), common sense never generated headlines on Hacker News (or anywhere else).