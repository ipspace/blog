---
title: "State of IT Security in 2021"
date: 2021-09-27 07:21:00
tags: [ security ]
---
[Patrik Schindler](https://www.pocnet.net/) sent me his views on code quality and resulting security nightmares after reading the [Cisco SD-WAN SQL Injection saga](/2021/09/cisco-sdwan-security.html). Enjoy!

---

I think we have a global problem with code quality. Both from a security perspective, and from a less problematic but still annoying bugs-everywhere perspective. I'm not sure if the issue is largely ignored, or we've given up on it (see also: [Cloud Complexity Lies](https://ea.rna.nl/2021/01/10/the-many-lies-about-reducing-complexity-part-2-cloud/) or [Cisco ACI Complexity](/2021/03/rant-cisco-aci-complexity.html)).
<!--more-->
Instead on focusing to not create even more bugs, companies like VMware publish a new vCenter server with some old bugs fixed, some new introduced and a shiny new bling-bling web interface style. Apparently it's cheaper to pay some icon designers than programmers.

I think, mankind at large is running towards a great catastrophe. Like stretched VLANs, it's not about if the catastrophe will happen, but when. And maybe how bad the fallout will be.

"With great power comes great responsibility." — Companies providing software which helps avoid civilization collapse because power stations work, water flows, food is produced, and money is shoveled around the globe have been incredibly lucky so far[^1]. I feel it's high time to stop depending on luck and start to divert money and time into solid software development processes, including testing, testing, testing. Everywhere. 

That will take money, which is often currently spent to make shareholders happy, or on the next bigger Porsche car for the CEO, or silly amounts of bonus payments to managers for saving money — on the wrong things. Money from many to a few. Money which isn't there to be spent on security expenses, training in best coding practices, etc.

[^1]: Ignoring [Boeing 737 MAX](https://en.wikipedia.org/wiki/Boeing_737_MAX_groundings) or [Therac-25](https://en.wikipedia.org/wiki/Therac-25).