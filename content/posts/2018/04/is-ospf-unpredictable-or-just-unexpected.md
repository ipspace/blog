---
date: 2018-04-26 07:52:00+02:00
intent-based-networking_tag: related
ospf_tag: rant
tags:
- OSPF
- SDN
- intent-based networking
title: Is OSPF Unpredictable or Just Unexpected?
url: /2018/04/is-ospf-unpredictable-or-just-unexpected.html
---
I was listening to a very interesting [Future of Networking with Fred Baker](http://packetpushers.net/podcast/podcasts/show-354-future-networking-fred-baker/) a long while ago and enjoyed Fred's perspectives and historical insight until Greg Ferro couldn't possibly resist the usual bashing of traditional routing protocols and praising of intent-based (or [flow-based](/2015/11/packet-and-flow-based-forwarding.html) or SDN or...) whatever.

Here's what I understood he said around 35:17
<!--more-->
> The problem with the dynamic or distributed algorithms is that they quite often do unexpected things.

You might think it was a Freudian slip-of-tongue, but it seems to be a persistent mantra. Recently it [became](http://etherealmind.com/networking-complex-hard/) "*a fallacy that a network will ever be reliable or predictable*."

Well, I totally believe that routing algorithms like OSPF would surprise Greg [or myself](/2017/01/ospf-forwarding-address-yet-another.html) (as I often admit during my [network automation workshops](http://www.ipspace.net/Hands-On_Network_Automation)), but that only means that with all the nerd knobs we added they became too complex for mere mortals to intuitively grasp their behavior.

{{<note>}}On a side note, I would love to see how [*expected*](https://www.youtube.com/watch?v=ARJ8cAGm6JE) the results of complex intent-based systems will be.{{</note>}}

Anyway, let's move from subjective *unexpected* to objective *unpredictable* or *non-deterministic*.

Interestingly, with the clear split between information distribution (LSA flooding) and route computation (SPF algorithm), link-state routing protocols are one of the most predictable distributed algorithms out there, and can in the worst-case scenario result in temporary forwarding loops due to eventual consistency of topology database.

{{<note warn>}}Seemingly simpler hop-by-hop protocols like distance- or path vector routing protocols are much worse and can result in [permanent forwarding loops](/2013/10/can-bgp-route-reflectors-really.html) or [persistent oscillations](https://rule11.tech/bgp-persistent-oscillation/).{{</note>}}

Assuming you have infinite patience, it's quite easy to predict what an OSPF network will look like:

-   Take topology database;
-   Follow all the intricate rules in various OSPF-related RFCs;
-   Get the final forwarding table.

{{<note>}}Speaking about the intricate rules: many of them seem like Rube Goldberg fixes introduced to correct unexpected OSPF behavior, probably proving my "*lack of intuitive grasp*" hypothesis.{{</note>}}

Nobody in his right mind would do something like that, but once the steps to a solution are well-defined, it's trivial (from the perspective of a mathematical proof, not the actual implementation) to carry them out... and there are tools like Cariden's MATE that do exactly that.

However, because it's easier to not spend money on something that would prevent an event with uncertain probability (network going down due to misconfigured OSPF, or losing customer data due to an intrusion), vendors like Cariden have relatively few customers, resulting in expensive tools.

Of course, there's another way of dealing with the "unexpectedness" of OSPF: [stop being a MacGyver](/2013/08/temper-your-macgyver-streak.html), forget the [nerd knobs](/2015/08/musing-on-nerd-knobs.html), keep your network design [as simple as possible](/2011/05/complexity-belongs-to-network-edge.html), and use the absolute minimum subset of features you need to get the job done.

Unfortunately, it seems like only a small minority of engineers or architects want to follow this particular advice. It's so much easier to [believe](/2016/01/the-sad-state-of-enterprise-networking.html) in [yet another technology wonder](/2017/09/intent-based-hype.html).
