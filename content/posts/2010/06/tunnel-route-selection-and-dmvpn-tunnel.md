---
date: 2010-06-23 06:57:00+02:00
dmvpn_tag: quirk
tags:
- DMVPN
- VPN
title: Tunnel Route Selection and DMVPN Tunnel Protection Don’t Work Together
url: /2010/06/tunnel-route-selection-and-dmvpn-tunnel.html
---
Cisco has introduced *Tunnel Route Selection*, another "somewhat" underdocumented feature in IOS release 12.4(11)T (reading the sparse documentation, it appears to be a half-baked kludge implemented for a specific customer). I was wondering for a long time why I would ever want to use this feature, until Floris Martens asked me a question about a redundant DMVPN network using two ISPs, and all of a sudden it all made a perfect sense.
<!--more-->
Building redundant DMVPN networks with multiple ISPs is a pretty common scenario, so I've included it in the [*DMVPN -- From Basics To Scalable Networks*](http://www.ipspace.net/DMVPN:_From_Basics_to_Scalable_Networks). However, when I tried to build a test lab, I could not get **tunnel route-via** to work in a protected DMVPN network. After a few hours, I had to conclude there's no way to make **tunnel route-via** work with **tunnel protection** (you could probably make it work in combination with crypto maps in Phase I DMVPN configuration, but I definitely didn't want to go down that route).

To add insult to injury, somehow Cisco's programmers managed to lose the "tunnel route-via feature is on" part of the **show interface** printout when merging various IOS trains to produce 15.0(1)M. The feature works in 15.0(1)M, but there's no way to check with a **show** printout whether it's enabled or not.
