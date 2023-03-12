---
date: 2015-06-08 08:34:00+02:00
high-availability_tag: ignore
series:
- ha-switching
tags:
- data center
- fabric
- design
- high availability
title: So You Need ISSU on Your ToR switch? Really?
url: /2015/06/so-you-need-issu-on-your-tor-switch.html
---
During the Cumulus Linux presentation Dinesh Dutt had at [Data Center Fabrics webinar](http://www.ipspace.net/Data_Center_Fabrics), someone asked an unexpected question: "*Do you have In-Service Software Upgrade (ISSU) on Cumulus Linux*" and we both went like "*What? Why?*"

Dinesh is an honest engineer and answered: "*No, we don't do it*" with absolutely no hesitation, but we both kept wondering, "*Why exactly would you want to do that?*"
<!--more-->
Back-channel conversation with the attendee brought up interesting facts:

-   He was asking about ISSU on ToR switches (not on MLAG core, where it might potentially make sense... or not);
-   Supposedly he's getting requests from service providers who build their cloud infrastructure with single-homed servers and then hammer on the network equipment vendors to implement ISSU on the ToR switches.

There's something radically wrong with this picture.

From my biased perspective, you have exactly two options:

-   You're big enough to afford losing dozens of servers after a ToR switch failure (regardless of whether you're building a scale-out web farm, Hadoop cluster, or public cloud infrastructure);
-   You're not big enough ([acceptable unit of loss](http://kontrolissues.net/2015/03/27/sometimes-size-matters-im-sorry-but-youre-just-not-big-enough/) is less than a ToR switch and all attached servers), in which case you dual-home your servers to two ToR switches, and stop caring about a ToR switch failure.

There is no middle ground or fifty shades of ToR redundancy -- you either have redundancy, or you don't. Forcing equipment manufacturers to do backflips with a mortar tied to their back because you botched your design is (at least) counterproductive.

Also, when was the "Keep it Simple, Stupid" replaced with "Let's [throw more spaghetti](https://blog.ipspace.net/2013/06/network-virtualization-and-spaghetti.html) at the wall"?

If you're still not persuaded, consider all possible failure scenarios:

-   Switch or server hardware failure (unlikely);
-   Transceiver failure or cable fault (not-so-unlikely);
-   Server or switch software crash;
-   Server or switch software upgrade.

Assuming hardware failures are unlikely (you might disagree with that, in which case you should change your supplier), will the switch software upgrade really be the most disruptive operation that will happen in your network, or will you experience switch software crashes more often than you're doing software upgrades (in which case ISSU doesn't buy you much). Also, how often are you planning to do the software upgrades anyway? Are you solving a major problem or complicating everyone's life to address a small minority of potential outages?

Also, do keep in mind that ISSU (and associated [Graceful Restart ](https://blog.ipspace.net/2021/09/graceful-restart.html)and [Non-Stop Forwarding](https://blog.ipspace.net/2021/09/non-stop-forwarding.html)) [vastly increases the device complexity](https://blog.ipspace.net/2014/04/should-we-use-redundant-supervisors.html), resulting in higher costs, more subtle bugs, and more opportunities for weird hangs and crashes.

### Want to know more?

Interested in data center switches and fabrics? Check out the [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar.
