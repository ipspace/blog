---
date: 2020-01-27 09:10:00+01:00
tags:
- SD-WAN
title: Fast Failover in SD-WAN Networks
url: /2020/01/fast-failover-in-sd-wan-networks/
sd-wan_tag: myth
---
It's amazing how quickly you get "*must have feature Y or it should not be called X*" comments coming from vendor engineers the moment you mention something vaguely-defined like SD-WAN.

Here are just two of the claims I got as a response to "*BGP with IP-SLA is SD-WAN*" trolling I started on LinkedIn based on [this blog post](/2019/10/changing-cisco-ios-bgp-policies-based/):

> Key missing features \[of your solution\]:
>
> -   real time circuit failover (100ms is not real-time)
> -   traffic steering (again, 100ms is not real-time)

Let's get the facts straight: it seems Cisco IOS evaluates **route-map** statements using **track** objects in periodic BGP table scan process, so the failover time is on order of 30 seconds plus however long it takes IP SLA to detect the decreased link quality.
<!--more-->
Now for the crux of this blog post: does it matter?

It's obvious that 100 msec failover time looks way better than 30 second failover time in any PowerPoint slide deck (unless you're dealing with someone with the capability to distort the local reality field), so we should always buy products with better failover times, right? Of course... assuming that's the most critical parameter your business has to deal with.

If you're a hospital doing remote surgery, or a drone operator flying a combat mission, or you're participating in the final round of Fortnite World Cup qualifications, then 100 msec failover time matters a lot... but then I hope you use something better than IPsec-over-Internet for your WAN links (guess not if you're playing Fortnite ... but now you've been warned ;).

If you're running a non-real-time business like most of us do, then you probably don't care too much - after all, your remote users probably experience higher failover times when switching between cell phone towers (or maybe I'm just unlucky).

The next data point to consider is the frequency of failover events. If you have links with extremely inconsistent and quickly-deteriorating quality then it's crucial to have fast detection and quick failover. If you're dealing with "typical" links they provide good-enough quality (even for voice traffic) most of the time, so you might not care whether the [once-a-year failover](/2019/06/know-thy-environment-before-redesigning/) happens in 100 msec or in 30 seconds.

As always, you should NEVER base your decisions based on \$vendor selling points regardless of how compelling or vital they seem. Start with "*what problem am I trying to solve*", continue with "*what do I REALLY need to solve that problem*" (aka "*what would be a good-enough solution*") as opposed to "*let's merge all the features any vendor ever mentioned into our RFP just to be on the safe side*", and select a vendor that solves your challenge in the simplest and cleanest way (and don't forget to look behind the covers to figure out the [hidden complexity](/2018/02/we-do-magic-crypto-with-no-impact-and/)).

I covered a few of these considerations in the [Business Aspects of Networking Technologies](https://www.ipspace.net/Business_Aspects_of_Networking_Technologies) webinar and if you're new to SD-WAN, check out our free [SD-WAN Overview](https://www.ipspace.net/SD-WAN_Overview) webinar.
