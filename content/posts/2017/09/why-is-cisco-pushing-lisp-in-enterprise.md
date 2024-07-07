---
date: 2017-09-11 08:22:00+02:00
tags:
- switching
- LISP
- LAN
title: Why Is Cisco Pushing LISP in Enterprise Campus?
url: /2017/09/why-is-cisco-pushing-lisp-in-enterprise/
---
I got several questions along the lines of "*why is Cisco pushing LISP instead of using EVPN in VXLAN-based Enterprise campus solutions?"*

Honestly, I'm wondering that myself (and maybe I'll get the answer in a few days @ [NFD16](http://techfieldday.com/event/nfd16/)). However, let's start at the very beginning...
<!--more-->
### What Do You Really Need?

It looks like Cisco (and a few other vendors, each one in its own way) still believes in the dire need for large layer-2 domains. I keep wondering why it seems everyone's so obsessed with large VLANs stretching all across campus. If you have a good use case, please let me know.

Do keep in mind that traffic separation is not a VLAN use case. It seems easier to solve with VLANs instead of VRFs because you don't appreciate how brittle or convoluted the behind-the-curtain stuff is. In other words, you're trading explicit complexity (VRFs + associated routing protocols) for hidden complexity (MLAG or TRILL or SPB or VXLAN with EVPN or LISP or...).

I also stopped believing in IP address mobility being the necessary driving force behind large VLANs. I know people using Mobile IP (and it's even easier with IPv6) on mobile phones, and most phones today can use mobile data + wireless at the same time anyway. On top of that, wireless access points tend to handle roaming pretty well, and in many cases use their own version of IP tunneling.

Long story short: ask yourself whether you really need large VLANs or whether you need a simpler IP network and smart apps (and as I said, do report your findings in the comments).

### Back to VXLAN

It looks like the networking industry is in another lemming rush. Everyone is rolling out VXLAN to solve large VLAN challenges, or even replacing MPLS with VXLAN for L3VPN deployments. Every single vendor is rolling out EVPN as the control plane for VXLAN. The current list includes at least Arista, Brocade (aka Extreme), Cisco, Cumulus, and Juniper.

Yet Cisco decided to use a completely different control plane (LISP) in campus networks. I can't possibly grasp why they'd do that apart from having a solution that has been searching for a problem to solve for years. If you know a really good technical reason why LISP is better in a campus network than EVPN (potentially with conversational learning in case Cisco yet again has hardware challenges) please share it with me.

I'm not the only baffled engineer out there. Here's what one of my readers wrote:

> Cisco DNA is not fulfilling my needs, this is more complex and looks like a marketing solution. Why would I use LISP to do the same thing given that we are already doing using EVPN \[in the data center\]?

He asked around whether he could use Nexus switches in campus to get the functionality he needs and (not surprisingly) got the answer along the lines "it might work, but we haven't tested it". Or as I told him:

> Don\'t fight the vendor. If your use case is not on their radar, don\'t try to push it through and make it work (though it makes perfect sense technically) - you\'ll hit all sorts of bugs because you\'ll be using untested combinations of features\... or you might discover that they don\'t have features you need in your particular environment.

Fortunately, there\'s more than one networking vendor out there, and some of them are small enough that they might work with you to get an interesting use case off the ground (I'm looking at you, Cumulus Networks). Just saying ;)
