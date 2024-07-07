---
title: "Hiding Malicious Packets Behind LLC SNAP Header"
date: 2023-01-26 07:55:00
tags: [ LAN, security ]
---
A random tweet[^DT] pointed me to [Vulnerability Note VU#855201](https://kb.cert.org/vuls/id/855201) that documents four vulnerabilities exploiting a weird combination of LLC and VLAN headers can bypass layer-2 security on most network devices.

{{<note warn>}}Before anyone starts jumping up and down -- even though the VLAN header is mentioned, this is NOT VLAN hopping.{{</note>}}

The security researcher who found the vulnerability also [provided an excellent in-depth description](https://blog.champtar.fr/VLAN0_LLC_SNAP/) focused on the way operating systems like Linux and Windows handle LLC-encapsulated IP packets. Here's the CliffNotes version focused more on the hardware switches. Even though I tried to keep it simple, you might want to read the [History of Ethernet Encapsulation](/2022/10/ethernet-encapsulations/) before moving on.
<!--more-->
[^DT]: ... making fun of Deutsche Telekom responding to the vulnerability with "_We have no Switches produced by any vendors for us_". It's really hard to [top Scott Adams](https://dilbert.com/strip/2010-04-24), but DT is doing their best.

This is how an Ethernet frame using a VLAN tag (802.1q) or frame priority (802.1p -- VLAN field is set to zero) should look like:

{{<ascii>}}
┌─────────────┬───────┬────────┬──────────┬────────────────────┐
│MAC addresses│VLAN ET│VLAN HDR│Payload ET│Payload             │
└─────────────┴───────┴────────┴──────────┴────────────────────┘
{{</ascii>}}

* The frame is using Ethernet II encapsulation
* VLAN EtherType (0x8100) is the first EtherType in the frame
* VLAN header follows the VLAN EtherType
* Payload follows the VLAN header, starting with payload EtherType (0x0800 for IPv4, 0x86DD for IPv6, ...)

LLC2 encapsulation is used on all other LAN media (example: WiFi). The same packet sent on WiFi looks like this:

{{<ascii>}}
┌─────────────┬────────┬───────┬────────┬──────────┬───────────┐
│MAC addresses│LLC SNAP│VLAN ET│VLAN HDR│Payload ET│Payload    │
└─────────────┴────────┴───────┴────────┴──────────┴───────────┘
{{</ascii>}}

* The frame is using LLC Type 1 encapsulation
* LLC header specifies SNAP encapsulation -- the rest of the frame will use EtherTypes
* VLAN EtherType (0x8100) is the first EtherType in the frame
* VLAN header follows the VLAN EtherType
* Payload follows the VLAN header, starting with payload EtherType (0x0800 for IPv4, 0x86DD for IPv6)

What do you think would happen if someone sends WiFi-formatted packet on Ethernet?

* Most operating systems would happily receive it, process the slightly bizarre sequence of headers, and send the IP datagram to the IP stack.
* Most forwarding hardware would be totally confused and fail to parse the inner payload as it does not expect such a layering of protocol headers.

{{<note warn>}}Things can get a bit more complex than that. You could combine headers in multiple incorrect ways, or use frame length in LLC-formatted Ethernet frame that does not match the actual packet length; some operating systems graciously ignore that "omission". There's a reason for four related vulnerabilities listed in that vulnerability note ;){{</note>}}

What's the impact of that parsing failure? You can't get anything forwarded into another subnet if the forwarding device doesn't parse the incoming frame as containing a layer-3 packet, but you can get an obfuscated packet past a layer-2 ACL that does not have a "deny all" at the end.

Unfortunately, the defaults that switch vendors have to implement to reduce their support costs[^CA] is to forward all packets within a layer-2 segment and drop only those malicious packets that they recognize (for example, [IPv6 RA messages coming from an untrusted source](/2011/11/ipv6-security-getting-bored-bru-airport/)). The unusual (and probably invalid, but who's counting) stacking of protocol headers thus allows an intruder to bypass any layer-2 security measure like layer-3 ACLs on layer-2 ports, ARP/ND inspection, DHCP guard or RA guard.

[Arista's security advisory](https://www.arista.com/en/support/advisories-notices/security-advisory/16276-security-advisory-0080) clearly identifies these challenges (if you know where to look) and recommends using a layer-2 ACL that drops any frames where the hardware parser stopped at 802.1q or 802.1ad EtherType. They also recommend a much better solution to block another vulnerability -- stricter ACL that permits only IPv4, IPv6, and ARP.

**Long story short**: The vulnerabilities are an interesting exploit of too many encapsulation options, but they cannot be used to implement VLAN hopping, and the sky is still not falling. They do present an interesting lesson in [having too many standards](https://xkcd.com/927/), but I doubt that many people working for a networking vendor or participating in a standards body would be interested in considering it.

[^CA]: For example, a customer opening a case saying "_my 50-year-old craplication using LAT stopped working when I installed your switch, I'm going back to your competitor_" because it's too hard to read the manual that says "_if you want to forward packets that are not IPv4 or IPv6, you have to configure these layer-2 ACLs_" and configure said ACL.
