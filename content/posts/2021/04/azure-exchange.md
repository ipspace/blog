---
title: "Microsoft Azure: Remember Exchange Server?"
date: 2021-04-22 06:53:00
tags: [ cloud, Azure ]
---
Recently I joked there's [significant difference between AWS and Azure launching features](https://twitter.com/ioshints/status/1368601005424861191):

* AWS launches a production-ready feature that you can consume the next day.
* Azure launches a preview that might work in 6 months.

Those with long enough memories shouldn't be surprised. It's not the first time Microsoft is using the same tactics.
<!--more-->
{{<note>}}What follows is my recollection of the events; some other people claim Exchange fiasco was Microsoft's response to Lotus Notes. I was more impacted by Netscape's demise at that time, and we might all be suffering from Mandela effect anyway.{{</note>}}

{{<long-quote>}}
Long long time ago, on a planet far far away, there was a too-successful startup called Netscape. They made a web browser that actually worked (as opposed to early Internet Explorer), and had a [whole suite of server products](https://en.wikipedia.org/wiki/Netscape#Later_Netscape_products) alongside their web server offering email and directory services. Not surprisingly, everyone (particularly those sick-and-tired of Microsoft's Windows monopoly) got excited. It was time for the empire to strike back.

Microsoft started talking about a beautiful vision called Exchange years before it shipped (my memory is blurry -- if someone has a better timeline please write a comment). They created enough hype to stop the rush of unsatisfied customers migrating to Netscape. Obviously those customers got duped, as they remained stuck with their ancient email systems for at least another year if not longer, but who cares about such minor details.

Finally, Exchange shipped. It was buggy, it was slow, it was useless (for example, SMTP gateway was added a year later)... but Netscape was mostly dead by that time. Exchange got better, bugs were fixed ([apparently not all of them](https://msrc-blog.microsoft.com/2021/03/02/multiple-security-updates-released-for-exchange-server/)), but it pushed us back at least half a decade.
{{</long-quote>}}

AWS is far too big to make that tactic useful against them, but keep it in mind the next time you'll hear [industry analysts talking about Microsoft WAN](https://blog.cimicorp.com/?p=4532). It looks great in PowerPoint (pun intended), but might set you back a few years if you decide to become a true believer. I've heard enough horrors stories about Azure VPN gateway to be extra-cautious (turns out there's a reason people want to deploy their own appliances in Azure).

Want to know the technical details? I added [Virtual WAN section](https://my.ipspace.net/bin/list?id=AzureNet#WAN) to the [Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinar in early April.
