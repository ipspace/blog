---
title: "Networking, Engineering and Safety"
date: 2020-09-07 07:07:00
tags: [ BGP, design ]
dcbgp_tag: rant
series:
- dcbgp
---
You might remember my [occasional rants about lack of engineering](/2018/12/bifurcation-of-knowledge.html) in networking. A long while ago [David Barroso](https://www.ipspace.net/Author:David_Barroso) nicely [summarized the situation in a tweet](https://twitter.com/dbarrosop/status/1204306828500312064) responding to my _[BGP and Car Safety](/2019/12/bgp-and-car-safety.html)_ blog post:

> If we were in a proper engineering we’d be discussing how to regulate and add safeties to an important tech that is unsafe and hard to operate. Instead, we blog about how to do crazy shit to it or how it’s a hot mess. Let’s be honest, if BGP was a car it’d be one pulled by horses.
<!--more-->
He got the "pulled by horses" part wrong. BGP would be a car without engine cover, making sure all moving parts are easily accessible by inquiring fingers.

Coming back to product safety, here's [another tweet](https://twitter.com/dbarrosop/status/1204307534296821762) from David:

> And yes, there are lot of **optional** knobs and even groups trying to set some “standards” to safely operate BGP but all of that should be baked in into BGP and impossible to remove the same way I can’t remove the seatbelts in my car.

Unfortunately, most vendors are more interested in creating [additional nerd knobs](/2015/08/musing-on-nerd-knobs.html) than in making a product safer to operate. Safety doesn't generate new sales until the public starts screaming or suing manufacturers for malpractice.
