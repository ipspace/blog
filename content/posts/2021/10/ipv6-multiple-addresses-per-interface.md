---
title: "Do We Need Multiple Global IPv6 Addresses Per Interface (RFC 7934)"
date: 2021-10-20 06:21:00
tags: [ IPv6, DHCP ]
---
I was happily munching popcorn while watching the latest season of _[Lack of DHCPv6 on Android](https://mailarchive.ietf.org/arch/msg/v6ops/LsWLNn7jBuNkjKlLzeZOTCrnPN8/)_ soap opera on [v6ops mailing list](https://mailarchive.ietf.org/arch/browse/v6ops/) when one of the lead actors trying to justify the current state of affairs with a technical argument [quoted an RFC to prove his rightful indignation with DHCPv6](https://mailarchive.ietf.org/arch/msg/v6ops/7AihJ8u7RotHzOnT-gHrkTQY0RM/) and the decision not to implement it in Android:

> [...not having multiple IPv6 addresses per interface...] is also harmful for a variety of reasons, and for general purpose devices, it's not recommended by the IETF. That's exactly what RFC 7934 is about - explaining why it's harmful.

{{<note info>}}If you're new to this discussion, you might want to start with *[Why Does DHCPv6 Matter](/2021/10/dhcpv6-matters/)* blog post{{</note>}}
<!--more-->
While this seems to me to be just another attempt to delay the decision for another decade[^2], let's try to figure out whether there's any technical merit behind _IPv6 hosts need multiple global addresses per interface_[^3] and _DHCPv6 can't provide that_.

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

That might be true in mobile phone tethering (where nobody uses DHCPv6 anyway -- [details here](/2021/10/dhcpv6-matters/)). Everywhere else it's pure and utter bullshit. There are [other reasons](/2011/12/ipv6-multihoming-without-nat-problem/) we need IPv6 NAT or [Network Prefix Translation (NPT)](/2011/12/we-just-might-need-nat66/) ([more NAT-related blog posts](/tag/nat/)), but number of IPv6 addresses per hosts, or address allocation mechanism (SLAAC vs DHCPv6), has nothing to do with them.

## Supposed Benefits

Moving on to *[Benefits of Providing Multiple Addresses](https://datatracker.ietf.org/doc/html/rfc7934#section-3)*[^4]:

[^4]: Keep in mind that the RFC is over half a decade old, and we've moved on in the meantime. On a tangential thought, it took less than a year from the first draft to the Best Practices RFC, so maybe the usual careful considerations and pondering of all angles so typical in [creation of a Best Practices RFC](/2015/02/rfc-7454-bgp-operations-and-security/) weren't applied to this one.

> Privacy addressing to prevent tracking by off-network hosts

Totally bogus. A random host ID changed every so often and never again used by the same device is most often good enough; [RFC 8981](https://datatracker.ietf.org/doc/html/rfc8981) solved the challenge in a better way.

> Multiple processors inside the same device.  For example, in many mobile devices, both the application processor and the baseband processor need to communicate with the network, particularly for technologies like I-WLAN [TS.24327] where the two processors share the Wi-Fi network connection.

I'm not familiar with the details of [cellular and WiFi interworking](https://en.wikipedia.org/wiki/Mobile_data_offloading#Cellular_and_Wi-Fi_network_interworking),  but it seems to be a special case of *an application needs a dedicated IPv6 address*. See below.

> Extending the network (e.g., "tethering").

Correct. However, as tethering takes place in mobile networks ([more details](/2021/10/dhcpv6-matters/)), it's ridiculous using this argument to justify *no DHCPv6 on multi-access[^L] segments ever*.

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

You could also ask for multiple IPv6 addresses in the initial DHCPv6 request. Here's what [RFC 8415 section 6.6](https://datatracker.ietf.org/doc/html/rfc8415#section-6.6) (*Multiple Addresses and Prefixes*) has to say about that:

> DHCP allows a client to receive multiple addresses.  During typical operation, a client sends one instance of an IA_NA option and the server assigns at most one address from each prefix assigned to the link to which the client is attached [...]
> 
>  A client can explicitly request multiple addresses by sending
   multiple IA_NA options (and/or IA_TA options; see Section 21.5).  A client can send multiple IA_NA (and/or IA_TA) options in its initial transmissions.  Alternatively, it can send an extra Request message with additional new IA_NA (and/or IA_TA) options (or include them in a Renew message).

One could argue that the authors of RFC 7934 were not aware of changes made to DHCPv6, but as the work on RFC 8415 started before the first draft of RFC 7934, I find that unlikely. One could also argue that RFC 7934 prompted the addition of Section 6.6 into RFC 8415[^TL], in which case RFC 7934 achieved its goals.

In any case, claiming that *"we cannot use DHCPv6 because it cannot provide more than one IPv6 address per interface as recommended by RFC 7934"* in 2021 makes one look uninformed and/or ridiculous[^BS].

[^TL]: draft-ietf-dhc-rfc3315bis-00 was published on March 23, 2015. draft-ietf-v6ops-host-addr-availability-00 was published on July 31st 2015. Section 6.6 was added to draft-ietf-dhc-rfc3315bis-08 published on May 8th 2017.

[^BS]: I tried really hard not to use more explicit language that might have included byproducts of large-sized ungulates.

Back to RFC 7934 *Benefits of Providing Multiple Addresses*:

> Identifier-Locator Addressing.

OK, maybe, but see above. Also, when you see a real-life application of ILA on Android, please let me know.

> Future applications

I've seen the same argument used by the proponents of "*every granny needs a /48*" address allocation. When you run out of arguments, claim that anything you don't like hinders the bright unspecified future.

## Recap

While there are legitimate uses for multiple IPv6 addresses per host, many of them don't apply to Android, or to the environments in which people want to see DHCPv6 working on Android, and RFC 8415 solved the problem anyway. 

Using RFC 7934 to justify not implementing DHCPv6 on Android is as bogus as it gets, and I'm positive people making those claims know that; they just use a *Best Practices RFC* as a stockpile of ammunition in useless battles.

**What can we do?** Not much until an IoT vendor selling expensive gear running on top of Android starts losing deals to its competitors[^6], or someone within EU administration figures out they need another example of Google abusing its platform monopoly, at which point the real behind-the-scenes screaming will start. 

In the meantime, please feel free to use this blog post in any IETF, NANOG, or RIPE discussion you wish to annoy the other side or to amuse the bystanders.

[^6]: ... hopefully because someone found a legitimate compliance reason to lock them out due to sloppy handling of IPv6 addresses.

