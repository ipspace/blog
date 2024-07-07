---
title: "Why Do We Need Source IP Addresses in IP Headers?"
date: 2023-09-26 06:40:00
tags: [ networking fundamentals ]
---
After discussing [names, addresses and routes](/2023/09/names-addresses-routes/), and the [various addresses we might need in a networking stack](/2023/09/addresses-in-network-stack/), we're ready to tackle an interesting comment [made by a Twitter user](https://twitter.com/odecentralize/status/1659947153999970305) as a reply to my *[Why Is Source Address Validation Still a Problem?](/2023/05/worth-reading-source-address-validation-still-a-problem/)* blog post:

> Maybe the question we should be asking is why there is a source address in the packet header at all.

Most consumers of network services expect a two-way communication -- you send some stuff to another node providing an interesting service, and you usually expect to get some stuff back. So far so good. Now for the fun part: how does the server know where to send the stuff back to? There are two possible answers[^RSC]:
<!--more-->
[^RSC]: As explained to me during the Cisco Router Software Course I attended in early 1990s ;)

* The conversation between the user and the server resembles a telephone call -- we don't have to worry how we'll send the stuff back to the user because we're on a phone call. We call this *connection-oriented* service.
* The conversation between the user and the server resembles an exchange of letters[^LT] -- we call this *connectionless* service. Obviously you need to know what address to write on the envelope if you want the letter to be delivered.

[^LT]: In case you never wrote a letter: in the ancient times we  would write stuff on bits of paper, put them in an envelope, and ask some courier service to transport that envelope to the recipient. For whatever weird reasons, every time I did that the courier service wanted to know where to deliver the envelope to.

Networking stacks are complex{{<sup>}}[citation needed]{{</sup>}}, and while the applications often expect connection-oriented service, the underlying transport might be connectionless[^X25]. For example, TCP provides a reliable stream service to its consumers while using connectionless IP transport. The TCP implementation thus needs to know how to send  IP packets back to the remote node.

[^X25]: Could we have connection-oriented service all the way down to the physical layer? Sure we can. We tried, and it didn't work too well. That's why you've got this text over the Internet instead of reading it on a [Minitel terminal using X.25](/2022/04/x25-still-alive/).

Obviously one could cheat, exchange IP addresses during the TCP session establishment, and use unique TCP connection identifier as an index into a table that would contain (among other things) remote IP address. In such a world, we wouldn't need source IP addresses in IP headers as TCP would know where to send the replies to.

There's just a tiny little gotcha: sometimes we want to have a quick response, and don't want to be bothered with setting up a reliable transport service[^CLAP]. A typical example might be a DNS query.

[^CLAP]: In other words. we want application-layer connectionless service.

We still need to identify application endpoints even if we don't want to set up a persistent session, so we have to use a thin wrapper on top of network layer to route the packets to target applications on the destination node (we use UDP for that in the TCP/IP stack). However, we still need to know where to send the reply to. You could store that information in the wrapper I just mentioned, or decide to be consistent and say "*meh, I'm giving up, all IP packets will have a source IP address so we know where to send the replies to* 🤷‍♂️"[^LV], and that's what the IP architects (and most other protocol designers) decided to do.

[^LV]: We could also go down the academic path and argue about layering violations, but even outside of ivory towers storing network addresses in higher-layer headers never ended well. Just remember the gruesome stuff NAT boxes have to do to fix FTP or SIP sessions.

Finally, an off-topic remark on connection identifiers: whoever designed TCP took a shortcut and decided to use the 4-tuple (source/destination IP addresses and port numbers) as connection identifiers. That's why we can't change the node IP address while having open TCP sessions[^MPTCP], totally destroying the ability to do easy roaming or live VM migration, and making [TCP the most expensive part of your data center](/2019/10/saved-tcp-is-most-expensive-part-of/).

[^MPTCP]: You can do it with Multipath TCP, which (surprise, surprise) uses *connection tokens*.
