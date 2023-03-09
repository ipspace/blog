---
date: 2015-12-10 10:41:00+01:00
ha-cluster_tag: firewall
high-availability_tag: ignore
series:
- ha-cluster
tags:
- design
- data center
- vMotion
- high availability
title: The Grumpy Old Network Architects and Facebook
url: /2015/12/the-grumpy-old-network-architects-and.html
---
Nuno wrote an interesting comment to my [Stretched Firewalls across L3 DCI](http://blog.ipspace.net/2015/11/stretched-firewalls-across-layer-3-dci.html) blog post:

> You\'re an old school, disciplined networking leader that architects networks based on rock-solid, time-tested designs. But it seems that the prevailing fashion in network design and availability go against your traditional design principles: inter-site firewall clustering, inter-site vMotion, DCI, etc.

Not so fast, my young padawan.

Let's define *prevailing fashion* first. You might define it as *Kool-Aid id peddled by snake oil salesmen* or *cool network designs by people who know what they're doing*. If we stick with the first definition, you're absolutely right.

Now let's look at the second camp: how people who know what they're doing build their network (Amazon VPC, Microsoft Azure or Bing, Google, Facebook, a number of other large-scale networks). You'll find L3 down to ToR switch (or even virtual switch), and absolutely no inter-site vMotion or clustering -- because they don't want to bet their service, ads or likes on the whims of technology that was designed to [emulate thick yellow cable](http://blog.ipspace.net/2015/02/lets-get-rid-of-thick-yellow-cable.html).

{{<note info>}}Want to know how to design an application to work over a stable network? Watch my [Designing Active-Active and Disaster Recovery Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.{{</note>}}

> This isn\'t the first time that readers have asked you about these technologies, and it won\'t be the last. Vendors will continue to market them despite their shortcomings, and customers will continue to eat them up.

As long as there will be someone willing to believe in fairy tales and Santa Claus, there will be someone dressed in red coat and fake beard yelling "Ho, Ho, Ho!"

Enterprise IT managers sometimes act like small kids. They don't want to hear that they have people- and process problems, and love to believe that the next magical bit of technology will solve whatever it is that bothers them. Vendors obviously love to explore these cravings and sell them ever-more-complex solutions.

> I\'d like to think that vendors will also continue to work out the kinks and over time the technology will become rock solid and time-tested.

I am positive you can make any technology almost-rock-solid. You can also make pigs fly (see RFC 1925 sect. 2.3). However, have you included the fuel costs in your TCO?

Also, the more complex a technology is, the likelier it is to crash down like a house of cards, and you'll be left with an incomprehensible mix of bits and pieces that will be impossible to put back together (see also: [You can't reformat your data center](http://blog.ipspace.net/2015/11/can-you-afford-to-reformat-your-data.html)).

Nino concluded his comment with a question:

> Are you too stuck on past, traditional designs and not being open to new ways of building IT? I get that IT is very cyclical, and these new trends may die in the future\...or thrive, and the customers may either fail\...or succeed.

I am very open to new ways of building IT. I preach the need for [meaningful SDN](http://www.ipspace.net/SDN,_OpenFlow_and_NFV_Workshop) (not the [centralized control plane crap](http://blog.ipspace.net/2015/06/centralized-control-is-not-centralized.html)), network automation, and proper application architecture. I just refuse to believe in fairy tales, and [solving non-technical problems with technology](http://blog.ipspace.net/2014/09/youve-been-doing-same-thing-for-last-20.html).

#### Finally...

Looking for more red pills? Explore my [SDN webinars](https://www.ipspace.net/SDN), [Designing Active/Active Data Centers](http://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar, and [vMotion-related blog posts](http://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html).
