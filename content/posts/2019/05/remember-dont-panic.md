---
cli_tag: fail
date: 2019-05-30 08:41:00+02:00
series_weight: 100
series:
- cli
tags:
- automation
title: 'Remember: Don’t Panic'
url: /2019/05/remember-dont-panic/
---
I hate listening to "this is what we were doing this year" podcasts as they usually turn into pointless blabbering, self-congratulations and meaningless plans (think New Year resolutions). [The Full Stack Journey Episode 28](https://packetpushers.net/podcast/full-stack-journey-028-turning-the-mic-on-scott-lowe/) with Scott Lowe was an amazing deviation from this too-common template.

If you don't have time to listen to the podcast (but you [OUGHT TO](https://tools.ietf.org/html/rfc6919#page-4) do it) here's what I loved most: "*When faced with the onslaught of new technologies, don't panic. Wait a few months to see which ones survive*".
<!--more-->
Maybe networking truly is different, but I wouldn't wait a few months but a year or two. Remember when Cisco ACI was launched? It might be safe to use it now. Remember early Juniper videos promising the nirvana of EVPN/VXLAN and demonstrating how simple the configuration was a year before the code actually shipped... and a few years before it was ready for production use?

Whatever networking technology the vendors are pushing, wait at least a few months before you start gathering data, then a bit more before you start playing with it in the lab, and way longer before you deploy it in production... while carefully evaluating whether the technology [solves a real business problem](/2013/04/this-is-what-makes-networking-so-complex/) that [cannot be solved by changing the way you work](/2013/01/long-distance-vmotion-stretched-ha/), fixing your design, eliminating the snowflakes or (god forbid) talking with the application team and figuring out common goals.

However, that doesn't mean that you shouldn't be considering interesting ideas that use age-old technologies in novel ways like (ta-da) network automation. There's no good reason you should still hand-craft your configurations instead of using templates, or use arcane naming conventions to keep track of versions and changes instead of pushing everything into source code control repository like Git.

Likewise, it's stupid to yammer about the lack of \$vendor-supplied tools when you could easily build your own, and even worse to claim you cannot get data out of the network when all you need is a framework that can execute the same **show** command on all devices in your network, parse the printout to extract useful data (thank you, \$vendors for not providing an API that would return structured data), and create a report.

Also, it might be worth exploring the world around you. For example, if you master enough HTML to create a web page you can immediately start creating PDF reports (there's an open-source tool that generates PDF from HTML), and if you manage to master the somewhat-arcane DOT syntax it's extremely easy to create graph descriptions that can be turned into images (or PDF) or into dynamic graphs displayed on web pages.

The only roadblock on this journey is your mindset. You have to decide whether you want to keep yammering, or whether you want to become tool-builder. The choice is yours, and there's no need to panic - like most things in life, it's not as hard as it looks when you're starting (and we have a [great course to help you get to your destination](https://www.ipspace.net/Building_Network_Automation_Solutions)).
