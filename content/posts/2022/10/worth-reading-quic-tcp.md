---
title: "Worth Reading: QUIC Is Not a TCP Replacement"
date: 2022-10-02 08:54:00
tags: [ TCP, worth reading ]
---
Bruce Davie makes an excellent point in his [QUIC Is Not a TCP Replacement](https://systemsapproach.substack.com/p/quic-is-not-a-tcp-replacement) article -- QUIC not a next-generation TCP, it's a reliable RPC transport protocol.

What Bruce forgot to mention is that we had a production-grade RPC transport protocol for years -- [SCTP (Stream Control Transmission Protocol)](https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol) -- but it had two shortcomings:

* [It wasn't invented by the right people](/2009/08/what-went-wrong-sctp.html);
* It used a different IP protocol number and thus upset every ossified middlebox in the Internet. QUIC hides on top of UDP (because adding extra headers makes at least as much sense as [junk DNA](https://en.wikipedia.org/wiki/Non-coding_DNA#Junk_DNA)).
