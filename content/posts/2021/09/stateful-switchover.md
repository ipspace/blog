---
date: 2021-09-14 06:51:00+00:00
distributed-systems_tag: device
ha-switching_tag: mechanism
high-availability_tag: external
series:
- ha-switching
- distributed-systems
series_title: Stateful Switchover (SSO)
tags:
- switching
- high availability
- networking fundamentals
title: Stateful Switchover (SSO) 101
---
*Stateful Switchover (SSO)* is another seemingly awesome technology that can help you implement high availability when facing a ~~broken~~ non-redundant network design. Here's how it's supposed to work:

* A network device runs two copies of the control plane (primary and backup);
* Primary control plane continuously synchronizes its state with the backup control plane;
* When the primary control plane crashes, the backup control plane already has all the required state and is ready to take over in moments.

Delighted? You might be disappointed once you start digging into the details.
<!--more-->
## Before Moving On

The rest of this blog post might look like I'm picking on Cisco IOS XE. IOS XE might seem irrelevant abandonware with an ancient architecture when looking at its documentation[^1] but one has to start somewhere.

Even more important, the fundamental challenges of implementing Stateful Switchover stay the same regardless of what (network) operating system you use:

* You need a distributed state database, and you cannot be sure the state database isn't corrupted when the primary control plane crashes;
* Secondary control plane has to figure out the primary control plane crashed, which is an interesting problem if you have just two nodes.
* Stateful Switchover has to be implemented for every single control-plane protocol and data- or control-plane feature that has at least minimal state.
* It's hard to take over stateful control plane protocols (almost all routing protocols) without help of adjacent nodes (*Graceful Restart* capability).

OK, now for the details.

## What State? (Part 1)

Let's start with a simple question: what *state* is synchronized between the control planes? [Cisco IOS XE 17 High Availability Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ha/configuration/xe-17/ha-xe-17-book/ha-config-stateful-switchover.html) lists four redundancy modes:

* **High System Availability** (HSA) -- the backup control plane is down and is rebooted after the failure of the primary control plane.
* **Route Processor Redundancy** (RPR) -- startup configuration is loaded into backup control plane which waits in standby slumber until the primary control plane fails.
* **Route Processor Redundancy Plus** (RPR+) -- primary control plane pushes configuration changes to the backup control plane which is still dormant, so when the primary control plane fails you won't have to deal with out-of-date configuration.
* **Stateful Switchover** (SSO) -- the one true magic (my wording) we're looking for.

## What State? (Part 2)

Now that we know we're interested in SSO, it's time to start wondering *what exactly is synchronized between the primary and backup control planes?* You'll quickly figure out that there's no easy answer to that question. I couldn't find a comprehensive overview of what Cisco IOS XE features support SSO.

Here's what I managed to get from the above-mentioned documentation:

* IPv4 and IPv6 forwarding tables;
* ARP and ND caches (needed for FIB adjacencies)
* Virtual access interfaces

What is not synchronized (according to the documentation):

* Routing protocol state or sessions. You need *Non Stop Routing* for that.
* HSRP, but there's another document called [SSO HRSP](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16-5/fhp-xe-16-5-book/fhp-hsrp-sso.html) so it looks like HSRP works with SSO and someone forgot to fix the outdated docs.
* Enhanced Object Tracking (EOT)
* IP Multicast state and forwarding tables
* AAA state
* Tons of Frame Relay and ATM features I couldn't be bothered with.

Control plane features that are not even mentioned (so who knows what's going on): LACP, LLDP, STP.

Data plane features not mentioned in the SSO documentation: NAT, stateful firewall, IPsec SA.

MPLS seems to be supported -- there's *‌[MPLS High Availability Configuration Guide, IOS XE 17](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/mp_ha/configuration/xe-17/mp-ha-xe-17-book.html)* claiming SSO works with LDP, MPLS-TE and MPLS/VPN.

## Wrapping Up

I already covered many caveats in *[Non-Stop Forwarding 101](non-stop-forwarding.html)* blog post and *[Before Moving On](#before-moving-on)* section, so let's just revisit the the two elephants that bother me most:

* Can we be sure that the backup control plane reliably figures out the primary control plane is down? What happens if that misfires? What happened to *[never take two chronometers to the sea](https://blog.ipspace.net/2017/01/never-take-two-chronometers-to-sea.html)* or the idea of a *witness node*?
* Assume the primary control plane crashes due to some SNAFU in the system state. That state has been synchronized to the backup control plane. What happens when the backup control plane starts using the messed-up state?

With that in mind:

* Use *Stateful Switchover* and *Non-Stop Forwarding* only when absolutely necessary. It's not a silver bullet but a kludge-of-last-resort.
* If you decide to use SSO, do a thorough check to verify *what state* is synchronized and whether all control- and data plane features you use support SSO. It's not a tragedy if some of them don't, but you do need to have a clear understanding of what you can expect when the primary control plane fails.
* SSO does not preserve the state of most control-plane protocols. You need *Graceful Restart* functionality to gloss over that detail, and GR brings another can of delicious worms with it.
* SSO is not instantaneous. It will take seconds (or longer). What happens to the transit traffic during that time? One would assume that *Non-Stop Forwarding* takes care of that, but if there's one thing you should have learned so far it's *don't assume anything*.

To summarize:

* Be skeptical;
* Ask pointed questions to separate marketing myths from reality;
* Test, test, test.

Finally, considering all of the above, it might be worthwhile replacing vendor magic with proper network design.

[^1]: It's worth noting that most of the tables in the [IOS XE 17 High Availability Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ha/configuration/xe-17/ha-xe-17-book/ha-config-stateful-switchover.html) talk about ancient IOS software releases like 12.0S. Maybe it's time to hire a decent technical writer to spiff things up? Also, if you're aware of a more decent document, please add a link in a comment.

## Behind the Scenes

This post was made much better based on extensive feedback provided by [Nicola Modena](https://www.ipspace.net/Expert:Nicola_Modena). Thanks a million!
