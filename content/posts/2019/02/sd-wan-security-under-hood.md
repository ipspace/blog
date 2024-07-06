---
date: 2019-02-07 08:08:00+01:00
tags:
- security
- SD-WAN
- SDN
- WAN
title: SD-WAN Security Under the Hood
url: /2019/02/sd-wan-security-under-hood.html
sd-wan_tag: security
---
A while ago we published a guest blog post by [Christoph Jaggi](https://www.ipspace.net/Author:Christoph_Jaggi) explaining the [high-level security challenges of most SD-WAN solutions](/2018/08/security-aspects-of-sd-wan-solutions.html)... but what about the low-level details?

[Sergey Gordeychik](http://www.scada.sl/) dived deep into implementation details of SD-WAN security in his 35C3 talk ([slides](https://fahrplan.events.ccc.de/congress/2018/Fahrplan/system/event_attachments/attachments/000/003/661/original/SD-WAN_-_35C3_-_publish.pdf), [video](https://www.youtube.com/watch?v=tfn2Q0sDqOY)).

TL&DW: some of the SD-WAN boxes are as secure as \$19.99 Chinese webcam you bought on eBay.
<!--more-->
Even more fun: you'll find some of the worst offenders as *leaders* in the Gartner's 2018 [Magic Quadrant for WAN Edge Infrastructure](https://www.silver-peak.com/sd-wan-edge-gartner-magic-quadrant-2018). Looks like cloudy visions and PowerPoint count more than quality of implementation.

However, we shouldn't be surprised. What could you expect to happen when vendors that were good in a totally different technology area decide to "*explore the market adjacencies*" and buy digital camera manufacturer or slap together a bunch of outdated open-source software and call the hodgepodge software-defined.
