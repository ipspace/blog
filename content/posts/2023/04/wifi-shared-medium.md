---
title: "Turning WiFi into a Thick Yellow Cable"
date: 2023-04-07 07:09:00
tags: [ security, switching, video ]
---
The "beauty" (from an attacker perspective) of the original shared-media Ethernet was the ability to see all traffic sent to other hosts. While it's trivial to steal someone else's IPv4 address, the ability to see their traffic allowed you to hijack their TCP sessions without the victim being any wiser (apart from the obvious session timeout). Really smart attackers could go a step further, insert themselves into the forwarding path, and inject extra payload into unencrypted sessions.

A [recently-discovered WiFi vulnerability](https://www.usenix.org/conference/usenixsecurity23/presentation/schepers) brought us back to that wonderful world.
<!--more-->
### How Does It Work?

In a nutshell (for more details read the article and security notices from your favorite WiFi vendor):

* Modern WiFi protocols allow a WiFi client to say "_I'm going to take a nap, please buffer all inbound packets_"[^FB].
* As it turns out, anyone connected to the WiFi network can send the "_taking a nap_" frame on behalf of anyone else.
* Even worse, many access points can be persuaded to send the queued frames using an intruder-enforced encryption key (or even unencrypted). Welcome back to the Thick Yellow Cable.

[^FB]: That's how you can get (almost) instant Facebook notifications without burning your battery in an hour.

### Hijacking Traffic for Fun and Profit

Now that we know how to hijack someone else's frames, let's insert ourselves into the forwarding path:

* Send a unicast GARP[^UGARP] for the victim's IP address to the MAC address of the first-hop router. That will persuade the router to send victim's traffic to us. Please note we need unicast GARP to work otherwise the victim will try to defend its IP address (or we could overload the victim first).
* Send a unicast GARP for the router's IP address to the victim. That will persuade the victim to send off-subnet traffic to us.
* Even better, start sending IPv6 Router Advertisements (maybe obfuscated using the [latest Ethernet encapsulation scam](/2023/01/hiding-packets-behind-llc-headers.html)) and [persuade the victim it's connected to a well-functioning IPv6 network](/2011/11/ipv6-security-getting-bored-bru-airport.html).

[^UGARP]: Yes, unicast Gratuitous ARP is a thing, and it's perfectly legal according to ARP RFC. Even worse, it's used by some multi-link NICs. More about that abomination in another blog post (unless I get too disgusted to write about it).

The above attack works within any subnet (VLAN) that is not protected with strict [Source Address Validation Improvement (SAVI)](https://www.rfc-editor.org/rfc/rfc7039) mechanisms on the first-hop switch. The WiFi Thick Yellow Cable vulnerability adds the capability to capture TCP frames of existing TCP flows and thus hijack the unencrypted TCP sessions (trivial to do once you know the sequence numbers).

Another possibility is the DNS hijacking: intercept DNS responses to victim's DNS queries, replace the A/AAAA information with your own IPv4/IPv6 address, and act as a TCP/UDP proxy for the victim. If only people would figure out how to use DNSsec ;)

### More Details

* I mentioned the ARP/ND hijacks and TCP session hijacks in the [Address and Session Hijacking](https://my.ipspace.net/bin/get/Net101/NS2.1%20-%20Address%20and%20Session%20Hijacking.mp4?doccode=Net101) video (part of [Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC) section of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar).
* We talked about IPv6 RA hijacks, SAVI, and RA Guard in the [IPv6 Security](https://www.ipspace.net/IPv6_security) webinar.
* For even more details, read the [RFC 6959: Source Address Validation Improvement (SAVI) Threat Scope](https://www.rfc-editor.org/rfc/rfc6959).

{{<jump>}}[Watch the video](https://my.ipspace.net/bin/get/Net101/NS2.1%20-%20Address%20and%20Session%20Hijacking.mp4?doccode=Net101){{</jump>}}

{{<note free>}}The Address and Session Hijacking video and parts of the IPv6 Security webinar are available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).{{</note>}}