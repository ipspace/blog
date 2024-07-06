---
date: 2018-11-13 07:31:00+01:00
tags:
- VXLAN
title: Sunset of VXLAN. Really?
url: /2018/11/sunset-of-vxlan-really.html
---
A lightning talk at the recent RIPE77 conference focused on [shortcomings of VXLAN and rise of Geneve](https://ripe77.ripe.net/presentations/54-the-sunset-of-vxlan-181016-final.pdf).

So what are those perceived shortcomings?

**No protocol identifier** -- a single VXLAN VNI cannot carry more than one payload type. Let me point out that MPLS has the same shortcoming, as does IPsec.
<!--more-->
**Original VXLAN was envisioned for carrying Ethernet payload only**. Correct. There are other whatever-over-IP encapsulation techniques for other use cases, many of them with widespread deployment.

**No inband OAM mechanism**. Do we really need a new one? What's wrong with sending CFM frames between VTEP MAC addresses... varying TTL values if want to track underlay path?

**No extensibility**. VXLAN has plenty of reserved fields in its header, but no extensibility... but do we really want another IPv6 headers fiasco? Add enough complexity and extensibility to a tunneling protocol and you'll have another Fernando Gont running circles around you in no time.

Don't get the reference? Search for IETF drafts and RFCs Fernando wrote and watch his presentations (I attended several of them at Troopers and Slovenian IPv6 Summit).

I don't understand the obsession with universally extensible tools. There's a reason every craftsman has a toolbox of tools that are just right for the job instead of a giant Swiss Army Knife.

However, don't worry -- IETF NVO3 working group has an answer: [Geneve](https://tools.ietf.org/pdf/draft-ietf-nvo3-geneve-08.pdf). It's hardware-friendly (so the lightning talk) and has extensible header that can be up to 260 bytes long. I've heard that before... and it didn't end well -- we got to a point where [software developers gave up on using smart NIC features](/2018/09/smart-or-dumb-nics-on-software-gone-wild.html) because of all the underlying complexity.

I can't help but being reminded of RFC1925 Rule 5... and even if I'm wrong (and I would love to be), do remember that every time someone designs a universal extensible protocol, you'll be paying for the increased complexity and associated security SNAFUs of every device using it.
