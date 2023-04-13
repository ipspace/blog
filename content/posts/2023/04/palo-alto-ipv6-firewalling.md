---
title: "IPv6 Security in Layer-2 Firewalls"
date: 2023-04-25 07:06:00
tags: [ firewall, IPv6 ]
---
You can configure many firewalls to act as a router (layer-3 firewall) or as a ~~switch~~ bridge (layer-2 firewall). The oft-ignored detail: how does a layer-2 firewall handle ARP (or any layer-2 protocol)?

Unless you want to use static ARP tables it's pretty obvious that a layer-2 firewall MUST propagate ARP. It would be ideal if the firewall would also enforce layer-2 security (ARP/DHCP inspection and IPv6 RA guard), but it looks like at least PAN-OS version 11.0 disagrees with that sentiment.

Straight from [Layer 2 and Layer 3 Packets over a Virtual Wire](https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-networking-admin/configure-interfaces/virtual-wire-interfaces/layer-2-and-layer-3-packets-over-a-virtual-wire):
<!--more-->
> In order for bridge protocol data units (BPDUs) and other Layer 2 control packets (which are typically untagged) to pass through a virtual wire, the interfaces must be attached to a virtual wire object that allows untagged traffic, and that is the default. If the virtual wire object Tag Allowed field is empty, the virtual wire allows untagged traffic. (Security policy rules don’t apply to Layer 2 packets.)

I read this as "_please feel free to do ARP hijacking on a supposedly protected subnet_." I hope I'm wrong and would appreciate a pointer to a document explaining how PAN-OS enforces source address validation.

But wait, it gets worse. From the same web page:

> If you want to be able to apply security policy rules to a zone for IPv6 traffic arriving at a virtual wire interface on the firewall, enable IPv6 firewalling. Otherwise, IPv6 traffic is forwarded transparently across the wire.

Let me reiterate that (and I checked the [configuration instructions](https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-networking-admin/configure-interfaces/virtual-wire-interfaces/configure-virtual-wires) to be on the safe side): by default, Palo Alto firewalls pass IPv6 traffic between Virtual Wire (layer-2) interfaces.

{{<note>}}I hope I'm wrong and someone will send me a link explaining why Palo Alto firewalls filter IPv6 on virtual wires by default.{{</note>}}

You can probably guess how the rest of this blog post will look like ([hint](https://blog.ipspace.net/2011/11/ipv6-security-getting-bored-bru-airport.html)). Anyway, here we go:

* Nobody wants to configure IPv6.
* Windows and major Linux distributions have IPv6 enabled by default.
* Because nobody cares about IPv6, it's sometimes left enabled.
* Likewise, there's a non-zero chance that whoever configured the layer-2 firewall decided IPv6 didn't matter.
* Linux servers filter IPv4 traffic with **iptables** and IPv6 traffic with **ip6tables**. If your server administrators don't care about IPv6 they probably haven't configured **ip6tables** with a DENY ALL rule.

What could possibly go wrong? How about:

* Someone gets root access to the least-protected server on the subnet.
* They start IPv6 RA daemon and all other nodes (including servers across the layer-2 firewall) get IPv6 addresses.
* Unless someone configured IPv6 firewalls/ACLs on the other servers, they're now wide open to the intruder.

But wait, it gets better:

* Include DNS option in IPv6 RA
* That will make other servers use the compromised server as their DNS server.
* The fake DNS server can return AAAA records for every query, forcing all other servers to establish new sessions over IPv6 and thus send the traffic to the first-hop IPv6 router (the compromised server).
* A Palo Alto layer-2 firewall (unless explicitly configured for IPv6 firewalling) would happily propagate that traffic.

As always, it must be the DNS' fault 😜, and the optimum solution must be to use `/etc/hosts` files 🤣.

Want even more details? You'll find them in the [IPv6 Security](https://www.ipspace.net/IPv6_security) webinar and in the [Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work).