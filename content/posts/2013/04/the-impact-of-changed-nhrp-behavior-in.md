---
date: 2013-04-03 07:02:00+02:00
dmvpn_tag: quirk
tags:
- firewall
- DMVPN
- IPsec
title: The Impact of Changed NHRP Behavior in DMVPN Networks
url: /2013/04/the-impact-of-changed-nhrp-behavior-in.html
---
Two years ago I wrote the another [Fermatish](http://en.wikipedia.org/wiki/Fermat's_Last_Theorem) post: I described how [NHRP behavior changed in DMVPN networks using NAT](/2011/04/dmvpn-spoke-nhrp-behavior-changed-in.html) and claimed that it might be a huge problem, without ever explaining what the problem is.

Fabrice [quickly identified the problem](/2011/04/dmvpn-spoke-nhrp-behavior-changed-in.html?showComment=1304374254012#c7665983883544403504), but it seems the description was not explicit enough as I'm still getting queries about that post, so here's a step-by-step description of what's going on.
<!--more-->
A single DMVPN network has two hubs and two spokes. Spokes are behind NAT boxes (e.g. cable/DSL modems) that prevent IPsec session between the spokes to be established.

{{<figure src="/2013/04/s450-DMVPN_NHRP_Problem.jpg">}}

When Spoke-A tries to establish communication with Spoke-B, the following events take place:

1.  Spoke A sends NHRP request for Spoke B to one of the hub routers (H1).
2.  At the same time spoke A creates fake NHRP entry for B pointing to H1 (this is the crux of the changes introduced in 15.0M).
3.  H1 forwards the NHRP request to Spoke B.
4.  Spoke B tries to establish IPsec tunnel to Spoke A to send the NHRP reply back to Spoke A.
5.  If the B-to-A IPsec tunnel establishment fails, the NHRP reply never arrives to Spoke A, and Spoke A uses fake NHRP entry pointing to H1 till it expires (3 minutes).

And now for the gotcha: Spoke A continues sending traffic toward H1 until the fake NHRP entry expires, regardless of whether H1 fails in the meantime or not. Only after the fake NHRP entry expires will Spoke A send another NHRP request to the hub router(s) alive at that time (H2). End result: traffic between Spoke A and Spoke B will be interrupted for up to three minutes even though you have redundant hubs in the DMVPN network.

### More information

Still using DMVPN? Check out my [DMVPN webinars](http://www.ipspace.net/Roadmap/VPN_webinars).
