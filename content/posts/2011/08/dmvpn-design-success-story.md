---
date: 2011-08-18 06:48:00.001000+02:00
dmvpn_tag: training
tags:
- DMVPN
title: DMVPN Deployment Success Story
url: /2011/08/dmvpn-design-success-story.html
---
Warning: totally shameless plug ahead. You might want to stop reading right now.

Every now and then one of the engineers listening to my webinars shares a nice success story with me. One of them wrote:

> I\'m doing a DMVPN deployment and Cisco design docs just don't cover dual ISPs for the spokes hence I thought I give your webinars/configs a try.

\... and a bit later (after going through the configs that you get with the [DMVPN webinar](https://www.ipspace.net/DMVPN:_From_Basics_to_Scalable_Networks)):
<!--more-->
> I have been testing the 2 VRF 2 ISP solution today, very cool, never thought of using vrfs to get round the 2 ISP issue. I was looking at using a loopback for the tunnel source and doing IP SLAs to change gateway upon ISP failure but the VRF method is a lot cleaner.

But there was another problem to be solved:

> Furthermore my scenario for a customer is such that they need local internet breakout so today been experimenting with modifying your scripts by simply adding a default route on the global table to serial 1/0 and using \"ip nat enable\".

As it happens, the local Internet breakout with VRFs (including inter-VRF NAT) is thoroughly covered in the [*Enterprise MPLS VPN Deployment*](https://www.ipspace.net/EntMPLS) webinar (yet again, you get tested router configs with the materials). Two not-so-very-trivial design problems solved for [less than \$80](https://www.ipspace.net/Recordings) ;)
