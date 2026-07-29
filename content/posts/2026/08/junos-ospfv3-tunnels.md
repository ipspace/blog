---
title: "Dear Junos, Tunnels Are Not Virtual Links"
date: 2026-08-26 07:55:00+0200
tags: [ OSPF, netlab ]
netlab_tag: quirks
ospf_tag: rant
---
In late June, we added GRE tunnels to _netlab_, including a [Junos implementation](https://github.com/ipspace/netlab/pull/3573). It looked great (as in "everything worked") until I changed the [integration tests](https://github.com/ipspace/netlab/blob/dev/tests/integration/tunnel/01-gre.yml) to have GRE tunnels between a tested device and a pair of FRR containers. All other implementations worked as before, but Junos failed to establish an OSPFv3 adjacency over the GRE tunnel with FRR.

[Stefano Sasso](https://www.linkedin.com/in/ssasso/) quickly [identified the culprit](https://github.com/ipspace/netlab/issues/3657#issuecomment-5059712285): Junos OSPFv3 process thinks it should send the DBD packets over GRE tunnels with MTU set to zero (the behavior reserved for *virtual links*)[^WST].
<!--more-->
[^WST]: You don't have to believe me; the GitHub issue linked above includes a Wireshark screen capture.

Next, he did something hilarious: he asked an AI whether that's the correct behavior. Here's the ["expert" response](https://github.com/ipspace/netlab/issues/3657#issuecomment-5059759955):

> Per RFC2740 (OSPFv3), the "Interface MTU should be set to 0 in Database Description packets sent over virtual links." JUNOS is correct in sending MTU 0 on a tunnel interface, per the OSPFv3 spec, since the interface MTU field should be set to 0 in DBD packets sent over virtual links. Junos treats GRE/tunnel-type interfaces the same way it would a virtual link, and always transmits MTU 0 on them for OSPFv3 — regardless of what family inet6 mtu or show ospf3 interface extensive reports.

Let's forget the minor "quoting an obsolete RFC" glitch (the correct RFC is [RFC 5340](https://datatracker.ietf.org/doc/html/rfc5340)) and the improper capitalization of Junos[^MF], it's obvious the stochastic text generator has a bit of a problem distinguishing between *OSPF virtual links* (a control-plane construct used to connect disjoint parts of the backbone area) and *tunnel interfaces* (a regular interface from the OSPFv2/OSPFv3 perspective).

[^MF]: I wonder what ~~Juniper~~ HP marketing thinks about that ;)

But wait, it gets better: [Jeroen van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) used the "let my AI talk to your AI" approach to get [this masterpiece](https://github.com/ipspace/netlab/issues/3657#issuecomment-5066150520), which includes the following claims:

* In standard Junos OSPFv3 deployments on tunnel interfaces, Junos populates the DBD Interface MTU field using the interface's actual payload MTU or IPv6 MTU.
* If you explicitly adjust the MTU (e.g., setting `mtu` under `unit 0` or modifying `family inet6 mtu`), Junos updates the value placed in outgoing DBD packets accordingly.

The only problem with those claims: the reality, as represented by Wireshark captures (and FRR logs), disagrees with them[^NBSP]. The only thing that "helped" was disabling the OSPFv3 MTU check on the other device connected to the tunnel.

[^NBSP]: Also known as "never let the truth get in the way of a ~~good story~~ persuasive AI response"

I have no idea whether we encountered a quirk specific to Junos virtual router implementation or whether the same behavior occurs in physical boxes (after all, it's a control-plane behavior). If you know more, please leave a comment.
