---
title: "Fun Times: Another Broken Linux ALG"
date: 2020-11-28 09:12:00
tags: [ security ]
---
Dealing with protocols that embed network-layer addresses into application-layer messages (like FTP or SIP) is great fun, more so if the said protocol traverses a NAT device that has to find the IP addresses embedded in application messages while translating the addresses in IP headers. For whatever reason, the content rewriting functionality is called *application-level gateway* (ALG).

Even when we're faced with a monstrosity like FTP or SIP that should have been killed with napalm a microsecond after it was created, there's a proper way of doing things and a fast way of doing things. You could implement a protocol-level proxy that would intercept control-plane sessions... or you could implement a hack that tries to snoop TCP payload without tracking TCP session state.

Not surprisingly, the fast way of doing things usually results in a wonderful attack surface, more so if the attacker is [smart enough to construct HTTP requests that look like SIP messages](https://github.com/samyk/slipstream). Enjoy ;)
