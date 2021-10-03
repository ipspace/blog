---
title: "Do We Need Multiple Global IPv6 Addresses Per Interface (RFC 7934)"
date: 2021-10-20 06:21:00
tags: [ IPv6, DHCP ]
---
I was happily munching popcorn while watching the latest season of _[Lack of DHCPv6 on Android](https://mailarchive.ietf.org/arch/msg/v6ops/LsWLNn7jBuNkjKlLzeZOTCrnPN8/)_ soap opera on [v6ops mailing list](https://mailarchive.ietf.org/arch/browse/v6ops/) when one of the players desperately searching for a technical argument to justify the current state of affairs [quoted an RFC to prove his rightful indignation with DHCPv6](https://mailarchive.ietf.org/arch/msg/v6ops/7AihJ8u7RotHzOnT-gHrkTQY0RM/):

> [...not having multiple IPv6 addresses per interface...] is also harmful for a variety of reasons, and for general purpose devices, it's not recommended by the IETF. That's exactly what RFC 7934 is about - explaining why it's harmful.

The implication of that statement are obvious: DHCPv6 IA_NA cannot provide that, thus it makes no sense to implement it on Android. [Fix DHCPv6 first and then we can talk](https://mailarchive.ietf.org/arch/msg/v6ops/GeWHsiEm008tMtsWsI96dPND288/).

{{<note info>}}If you're new to this discussion, you might want to start with *[Why Does DHCPv6 Matter](/2021/10/dhcpv6-matters.html)* blog post{{</note>}}
<!--more-->
Ignoring for the moment that the engineer referring to [RFC 7934](https://datatracker.ietf.org/doc/html/rfc7934) happens to be the lead author of that RFC, and that his statement seems to be just another attempt to delay the decision for another decade[^2], let's try to figure out whether there's any technical merit behind the _IPv6 hosts need multiple global addresses per interface_[^3].

[^2]: ... while giving enterprises reluctant to deploy IPv6 perfect excuse not to do it, but who cares about enterprises these days anyway, it's not like they would be the entities exploitable through ad tracking and profiling.

[^3]: Not surprisingly, I'm not the only one [thinking along those lines](https://mailarchive.ietf.org/arch/msg/v6ops/XDpXyn_Nt0m8nv7CErumDcwV0S4/).

## Dissecting the Problem

Let's see how RFC 7934 introduces the problem:

> IPv6 addresses are not a scarce resource.  In IPv6, a single link provides over four billion times more address space than the whole IPv4 Internet [RFC7421].

Correct.

> Thus, unlike IPv4, IPv6 networks are not forced by address scarcity concerns to provide only one address per host.

Correct.

> Furthermore, providing multiple addresses has many benefits, including application functionality and simplicity, privacy, and flexibility to accommodate future applications.

We'll see about that.

> Another significant benefit is the ability to provide Internet access without the use of Network Address Translation (NAT). Providing only one IPv6 address per host negates these benefits.

That might be true in mobile phone tethering (where nobody uses DHCPv6 anyway -- [details here](/2021/10/dhcpv6-matters.html#fnref:1)). Everywhere else it's pure and utter bullshit. There are [other reasons](https://blog.ipspace.net/2011/12/ipv6-multihoming-without-nat-problem.html) we need IPv6 NAT or [Network Prefix Translation (NPT)](https://blog.ipspace.net/2011/12/we-just-might-need-nat66.html) ([more NAT-related blog posts](https://blog.ipspace.net/tag/nat.html)), but number of IPv6 addresses per hosts, or address allocation mechanism (SLAAC vs DHCPv6), has nothing to do with them.

## Supposed Benefits

Moving on to *[Benefits of Providing Multiple Addresses](https://datatracker.ietf.org/doc/html/rfc7934#section-3)*[^4]:

[^4]: Keep in mind that the RFC is over half a decade old, and we've moved on in the meantime. On a tangential thought, it took less than a year from the first draft to the Best Practices RFC, so maybe the usual careful considerations and pondering of all angles so typical in [creation of a Best Practices RFC](https://blog.ipspace.net/2015/02/rfc-7454-bgp-operations-and-security.html) weren't applied to this one.

> Privacy addressing to prevent tracking by off-network hosts

Totally bogus. A random host ID changed every so often and never again used by the same device is most often good enough; [RFC 8981](https://datatracker.ietf.org/doc/html/rfc8981) solved the challenge in a better way.

> Multiple processors inside the same device.  For example, in many mobile devices, both the application processor and the baseband processor need to communicate with the network, particularly for technologies like I-WLAN [TS.24327] where the two processors share the Wi-Fi network connection.

I'm not familiar with the details of [cellular and WiFi interworking](https://en.wikipedia.org/wiki/Mobile_data_offloading#Cellular_and_Wi-Fi_network_interworking),  but it seems to be a special case of *an application needs a dedicated IPv6 address*. See below.

> Extending the network (e.g., "tethering").

Correct. However, as tethering takes place in mobile networks ([more details](/2021/10/dhcpv6-matters.html#fnref:1)), it's ridiculous using this argument to justify *no DHCPv6 on multi-access[^L] segments ever*.

[^L]: WiFi or Ethernet (not much else is left in 2021)

> Running virtual machines on hosts.

Correct. Yet again, using this one for *no DHCPv6 on Android* is pure and simple nonsense.

Looking at a bigger picture, we have the same problem in IPv4 networks, and it's been solved for ages:

1. Virtual machines are connected to the outside LAN segment[^5]
2. Each virtual machine uses DHCP/DHCPv6 to get the outside IPv4/IPv6 address it needs.
3. [Profit](https://en.wikipedia.org/wiki/Gnomes_(South_Park)).

[^5]: It doesn't matter whether the implementation uses *bridging* or *packet forwarding based on IP addresses*, what matters is that the virtual machines appear to be co-resident to the hypervisor host.

> Translation-based transition technologies such as 464XLAT (a combination of stateful and stateless translation) (RFC6877) that translate between IPv4 and IPv6.  Some of these technologies require the availability of a dedicated IPv6 address in order to determine whether inbound packets are translated or native ([RFC6877, Section 6.3](https://datatracker.ietf.org/doc/html/rfc6877#section-6.3)).

Correct. Now we're in the *application-specific IPv6 address* territory. What's wrong with sending another DHCPv6 request for each additional application-specific IPv6 address (similar to the *virtual machines* scenario above)? The idea is nicely described in [RFC 8415 section 21.5](https://datatracker.ietf.org/doc/html/rfc8415#section-21.5) (*Identity Association for Temporary Addresses Option*):

> The client obtains new temporary addresses by sending an IA_TA option with a new IAID to a server.  Requesting new temporary addresses from the server is the equivalent of generating new temporary addresses as described in [RFC4941].

One could argue that the authors of RFC 7934 were not aware of this mechanism, but as the work on RFC 8415 started before the first draft of RFC 7934, I find that unlikely. In any case, IA_TA makes *we cannot use DHCPv6 because RFC 7934* argument totally bogus.

Back to RFC 7934 *‌Benefits of Providing Multiple Addresses*:

> Identifier-Locator Addressing.

OK, maybe, but see above. Also, when you see a real-life application of ILA on Android, please let me know.

> Future applications

I've seen the same argument used by the proponents of "*every granny needs a /48*" address allocation. When you run out of arguments, claim that anything you don't like hinders the bright unspecified future.

## Recap

While there are legitimate uses for multiple IPv6 addresses per host, many of them don't apply to Android, or to the environments in which people want to see DHCPv6 working on Android, and DHCPv6 IA_TA solved the problem anyway. 

Using RFC 7934 to justify not implementing DHCPv6 on Android is as bogus as it gets, and I'm positive people making those claims know that; they just use a *Best Practices RFC* as a stockpile of ammunition in useless battles.

**What can we do?** Not much until an IoT vendor selling expensive gear running on top of Android starts losing deals to its competitors[^6], at which point the real behind-the-scenes screaming will start. 

In the meantime, please feel free to use this blog post in any IETF, NANOG, or RIPE discussion you wish to annoy the other side or to amuse the bystanders.

[^6]: ... hopefully because someone found a legitimate compliance reason to lock them out due to sloppy handling of IPv6 addresses.

