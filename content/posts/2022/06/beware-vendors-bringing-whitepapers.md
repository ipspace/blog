---
date: 2022-06-15 06:20:00+00:00
series:
- ASIC
tags:
- switching
title: Beware of Vendors Bringing White Papers
---
A few weeks ago I wrote about [tradeoffs vendors have to make when designing data center switching ASICs](/2022/06/data-center-switching-asic-tradeoffs/), followed by another blog post [discussing how to select the ASICs for various roles in data center fabrics](/2022/06/select-data-center-switching-asic/).

You [REALLY SHOULD](https://datatracker.ietf.org/doc/html/rfc6919#section-1) read the two blog posts before moving on; here's the buffer-related TL&DR for those of you ignoring my advice ;)
<!--more-->
* You don't need large buffers in non-oversubscribed spine switches;
* You better have some more buffer space in edge switches, in particular when there's plenty of traffic going from high-speed ports toward low-speed ports.
* You might need deep buffers when there's a large mismatch between ingress and egress speeds or link latency.

I haven't received a single comment saying "_you're totally wrong and here's a good technical article proving that_" so I'm assuming I'm not horrendously off the mark.

Would you expect vendor product marketers to agree with the above? Of course not. Years ago, Arista was enamored of deep-buffer switches... until Cisco launched a Jericho-based data center switch. At that point buffers stopped mattering... unless you were reading Cisco white papers.

There were tons of rebuttal blog posts written at that time, so one would hope that the vendors got the message. That's too much to hope for, one of my readers [kindly pointed me to a Juniper white paper claiming just the opposite of the above TL&DR](/2022/05/network-hardware-disaggregation-2022/#1241):

{{<note info>}}The white paper discovered by my reader was removed from Juniper's web site less than 12 hours after this blog post has been published. I would like to thank [Ben Baker and his team](/2022/06/beware-vendors-bringing-whitepapers/#1302) for a swift and decisive reaction.{{</note>}}

---

An article from Juniper[^NG] I found on the web was saying quite opposite [_from what you were saying_]: Low On-Chip Memory ASIC for low buffer leafs, Large External Memory ASIC for high speed/high buffer leaf and spine.

---

[^NG]: Now gone, but I have a downloaded copy somewhere ;)

No surprise there. Juniper is selling numerous switches based on Broadcom merchant silicon (QFX 5000 series), and deep buffer ([100 milliseconds of buffers per port](https://www.juniper.net/us/en/products/switches/qfx-series/qfx10002-fixed-ethernet-switches-datasheet.html)) QFX 10000 switches using in-house silicon. What do you think they want you to buy?

The white paper my reader found compared switches using Broadcom Tomahawk ASIC with switches using Juniper Q5 ASIC, and wrongly concluded that you should use Tomahawk ASIC at the edge and Q5 ASIC at the core.

Tomahawk ASIC is a pretty bad choice for a data center fabric edge -- it's missing a lot of functionality available in Broadcom Trident chipset (for example, VXLAN Routing In and Out of Tunnels), and it has less buffer space than a Trident family ASIC with comparable throughput.

What about deep buffer switches at the spine layer? Do you really think you need tens of milliseconds of buffer space _per port_ on a spine switch? Is that what you want the fabric latency to be?

Will it hurt to have deep buffers on spine switches? Probably not, particularly if you don't care about latency, but you would be paying through the nose for functionality you might not need. But then, if you have infinite budget, go for it.

To wrap up: when a white paper comparing Tomahawk and Q5 ASICs is saying...

> Switching platforms based on low on-chip memory ASICs are best suited for cost-effective, high-speed, high-density server access deployments.

... they really mean:

> We want you to buy QFX10K for your spine switches, but we can't justify it any other way, so we'll claim shallow-buffer switches are only good for the network edge.

Last question: why wouldn't Juniper recommend a Trident-based edge switch? Because the white paper was written before they launched QFX5130 and nobody bothered to fix it?

### Long Story Short

* Never forget Rule#2 of good network design: beware of vendors bringing white papers[^GBG].
* When you decide to design a network based on vendor white papers, you'll get the network you deserve.

Finally a note for the vendors: I understand you have to present an alternate view of reality that's focused on what you want to sell, but could you at least fix it when you launch new products -- that document was written in 2015, removed from Juniper's web site in June 2022 and happily confusing unaware networking engineers in the meantime.

[^GBG]: Based on [beware of Greeks bearing gifts](https://en.wikipedia.org/wiki/Beware_of_Greeks_bearing_gifts), in particular when they look like a wooden horse.

### Revision History

2022-06-16
: The white paper was removed from Juniper's web site
