---
title: "ICMP Redirects Considered Harmful"
date: 2022-02-22 07:28:00
lastmod: 2022-02-03 07:33:00
tags: [ IP routing, data center, design ]
---
One of my readers sent me an intriguing challenge based on the following design:

* He has a data center with two core switches (C1 and C2) and two Cisco Nexus edge switches (E1 and E2).
* He's using static default routing from core to edge switches with HSRP on the edge switches.
* E1 is the active HSRP gateway connected to the primary WAN link.

The following picture shows the simplified network diagram:
<!--more-->
{{<figure src="/2022/02/icmp-redirect-physical.png" caption="Physical connectivity">}}

All four devices are in the same VLAN, resulting in the following logical connectivity:

{{<figure src="/2022/02/icmp-redirect-layer-3.png" caption="Layer-3 connectivity">}}

He wanted to test the backup WAN link, shut down the primary link without changing the active HSRP gateway, and discovered that the core switches are no longer reachable from the outside world. Changing the HSRP gateway solved the problem. Adding another transit link between E1 and E2, and running a routing protocol on that link instead of on the current VLAN also fixed it.

I had no clue what might have gone wrong, even though the root cause was so obvious in hindsight: **ICMP redirects**.

C1 and C2 had no idea about the changed routing landscape. When they continued sending the outgoing packets toward E1, E1 sent them ICMP redirects, desperately trying to tell them to send the traffic to E2 instead. There were just a few tiny little problems:

* Linecard hardware cannot send ICMP redirects. All packets that generate a redirect (packets sent out through the same interface) must be forwarded to the main CPU.
* Control Plane Protection -- protecting the main CPU -- dropped most of those packets.
* IP routers (aka layer-3 switches) ignore ICMP redirects anyway.

Disabling ICMP redirects on the Nexus switches with **no ip redirects** magically solved the problem.

Considering the impact of this SNAFU, one has to wonder about the Nexus OS default settings:

* ICMP redirects are rarely useful
* Ignoring ICMP redirects on hosts is often considered a "security best practice" -- they are almost as good as [IPv6 Router Advertisements](/2011/11/ipv6-security-getting-bored-bru-airport/) if you want to snatch someone's traffic.
* Sending ICMP redirects is a performance killer.

And still, a modern network operating system has an obsolete 40-year-old technology enabled by default (still true on Nexus OS 9.3.8). Mindboggling.

On a tangential note, the current design suffers from traffic trombones: S1 and S2 send outgoing traffic to E1, which forwards it to E2 when the primary WAN link is down. That particular glitch would be easy to fix with anycast gateway or active-active VRRP. The proof is left as an exercise for the reader.

### It's All IETF Fault

[Christopher Hart quickly pointed](https://twitter.com/_ChrisJHart/status/1496097748206112771) out that an IPv4 router must send ICMP Redirects as mandated by Section 5.2.7.2 of RFC 1812 (Requirements for IP Version 4 Routers). 

> Routers MUST be able to generate the Redirect for Host message (Code 1)

While ICMP Source Quench messages have been deprecated[^DP] by [RFC 6633](https://datatracker.ietf.org/doc/html/rfc6633) (an update to RFC 1812), nothing similar was ever done for ICMP Redirects.

{{<note info>}}I find the wording of that section confusing. Does it mean that the router *must he **ABLE** to generate redirects* (but doesn't have to generate them) or that the router *must **GENERATE** redirects*?{{</note>}}

In the weird world of corporate marketing, other vendors' marketing teams would have a field day (so Christopher) if NX-OS  were not an RFC-compliant IPv4 router due to disabled ICMP redirects, even if disabling this behavior by default was a universally good thing.

---

Cisco IOS initially disabled ICMP redirects on interfaces that had HSRP enabled -- Jeroen van Bemmel [sent me a link](https://twitter.com/jbemmel/status/1496241937057202190) to the relevant page in *Cisco IOS in a Nutshell* book which was unfortunately last updated over 15 years ago. 

It seems that they decided to [change that behavior in IOS release 12.1](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp/command/iap-cr-book/iap-i1.html#wp1977268460), and [added yet another nerd knob in a later IOS release](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16-5/fhp-xe-16-5-book/fhp-hsrp-icmp.html) to make it even more complex.

---

IPv6 requirements are slightly less outdated ([RFC 4861 section 8.2](https://www.rfc-editor.org/rfc/rfc4861.html#section-8.2), HT [Darrell Root](https://twitter.com/DarrellRoot/status/1496124013198082060)):

>  A router SHOULD send a redirect message, subject to rate limiting, whenever it forwards a packet that is not explicitly addressed to itself (i.e., a packet that is not source routed through the router) in which: [..a list of requirement that causes ICMP redirect to be sent...]

Want to know more? You'll find way too many details in Christopher's _[ICMP Redirects - How Data Plane Traffic Can Become Control Plane Traffic](https://chrisjhart.com/How-Data-Plane-Traffic-Can-Become-Control-Plane-Traffic/)_ blog post.

### But Wait, It Gets Worse

I focused on the sending router, but what happens when a router receives an ICMP redirect? RFC 1812 (same section) contains an interesting loophole (emphasis mine):

> A router using a routing protocol (other than static routes) MUST NOT consider paths learned from ICMP Redirects **when forwarding a packet**.

But what happens to the locally-generated control-plane traffic? Could a router with hardware forwarding (aka a *switch*) listen to ICMP redirects and install them in the operating system forwarding table which is used for control-plane traffic but not in the forwarding hardware? Dmytro Shypovalov claims he's [seen that in real life](https://twitter.com/routingcraft/status/1496069240926969858):

> It gets even uglier if the router accepts ICMP redirects (it shouldn't by default, but I've seen some do). Redirect kernel cache entry is not installed in RIB or FIB, so local and transit traffic to the same destination take different paths.

One has to wonder: how crazy can it get?

### Revision History

2022-02-23
: Added feedback by Christopher Hart, Darrell Root, Dmytro Shypovalov, and Jeroen van Bemmel.

[^DP]: Because nothing ever dies in IETF world