---
date: 2019-10-21 08:22:00+02:00
tags:
- SD-WAN
title: SD-WAN Vendor Landscape
url: /2019/10/sd-wan-vendor-landscape/
sd-wan_tag: rant
---
In the [Three Paths of Enterprise IT](https://my.ipspace.net/bin/list?id=NetBiz#3PATH) part of [Business Aspects of Networking](https://www.ipspace.net/Business_Aspects_of_Networking_Technologies) webinar I covered the traditional networking vendor landscape. Let's try to do the same for SD-WAN.

It's clear that we had two types of SD-WAN vendors:
<!--more-->
-   Startups claiming to be disruptive while trying to apply lessons their engineers learned in more traditional environments in a clean-slate product design. Most of these got acquired in the meantime.
-   Traditional vendors trying to sprinkle fairy dust on their products to be able to slap SD-WAN label on them (Cisco's DMVPN+PfR+OER+Glue Networks orchestration comes to mind).

{{<note warn>}}This blog post has been written in 2019. One can hope things improved in the meantime (or as they say, _hope dies last_).{{</note>}}

If you've been in networking long enough, you've probably seen what happens when traditional vendors try to "*do more with less*" and "*leverage the investment*". Trying to glue a bunch of software components that were never designed to work together into something that could be called a solution or new technology is never a pretty sight... but do keep in mind that [there are no miracles](/2015/06/software-defined-wanwell-orchestrated/) and in most cases you have to deal with either explicit complexity (aka "*seeing how the sausage is being made*") or with hidden complexity that [will eventually come back to bite you](/2015/11/can-you-afford-to-reformat-your-data/).

One would hope that the startups would come up with better solutions, but it seems that at least in the SD-WAN case a variant of [Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law) applies to them - no SD-WAN startup did a perfect job but focused on the aspects that were familiar to its founders. For example, Viptela was really good in solving the routing challenge (while using traditional packet forwarding) while VeloCloud had really interesting packet handling capabilities while trying to ignore the need for routing protocols.

{{<note>}}For whatever reason, a Systems Engineer working for VeloCloud didn\'t appreciate my mention of the company\'s history. To set the record straight: VeloCloud 3.3.0 supports customer-facing OSPF and BGP. I won\'t waste time digging into older releases to figure out when the routing protocol support was introduced, and you can find the details in their documentation which is now public. To avoid any further confrontation I won\'t go into the history of that particular topic ;){{</note>}}

Traditional vendors slapping SD-WAN labels onto their products fall into similar categories:

-   Router vendors being really good in finding paths across the networks while missing advanced WAN features;
-   WAN Optimization vendors applying their existing technologies to the WAN transport part of SD-WAN while having mediocre routing implementations;
-   Firewall vendors relabeling their VPN products while having sub-par routing or WAN transport capabilities.

Not surprisingly, most everybody the got [security part of the equation wrong](/2018/08/security-aspects-of-sd-wan-solutions/). That's what happens when you try to enter a complex technology area without understanding what you're doing and using obsolete versions of open-source libraries in your products because that's cheaper than investing into people who built good security products in the past (not that there would be too many of them).

Some of the [juicy security details](/2019/02/sd-wan-security-under-hood/) can be found in [this presentation](https://fahrplan.events.ccc.de/congress/2018/Fahrplan/system/event_attachments/attachments/000/003/661/original/SD-WAN_-_35C3_-_publish.pdf). Even better, a team of security researchers created [SD-WAN New Hope](https://github.com/sdnewhop/sdwannewhope) repository listing tons of white papers, presentations from independent security researchers, and their security findings. Fun reading...

{{<note>}}
I know a poor soul who was involved in SD-WAN pentesting and vendor evaluation. He has nightmares of vendors using key exchange and encryption technologies that were obsoleted for a very good reason by recent IPsec RFCs, but unfortunately cannot share the horror stories due to layers of NDAs he had to sign to get the vendors to spill their (lack of) beans.
{{</note>}}

Does this landscape look gloomy? Sure it does, but then what did you expect after another gold rush? Can we hope to get something better in the future? I doubt - the most-promising startups have been acquired, and their product architectures are mature enough that they are getting ossified... and being a part of 400-pound gorilla makes it really hard to change things that the gorilla paid big money for. Looks like we'll have to live with the consequences of [another round of disruptive marketing](/2019/10/the-cost-of-disruptiveness-and/) for years.

{{<note>}}
People are telling me that Viptela is getting better and gradually implementing functionality available in competing SD-WAN products, so there's still some hope... ;)
{{</note>}}
