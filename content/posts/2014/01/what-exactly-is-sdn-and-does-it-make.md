---
cdate: 2022-07-09
comment: 'The very strict definition of SDN as understood by Open Networking Foundation
  promotes an architecture with strict separation between a controller and totally
  dumb devices that cannot do more than forward packets based on forwarding rules
  downloaded from the controller. Does that definition make sense?


  This is what I wrote in January 2014. The centralized control plane idea was mostly
  debunked in the meantime, and even ONF abandoned OpenFlow in favor of P4.

  '
date: 2014-01-16 07:17:00+01:00
sdn_101_tag: intro
series:
- sdn_101
series_weight: 190
tags:
- SDN
title: What Exactly Is SDN (And Does It Make Sense)?
url: /2014/01/what-exactly-is-sdn-and-does-it-make.html
---
When Open Networking Foundation claimed ownership of Software-Defined Networking, they [defined it as separation of control and data plane](https://www.opennetworking.org/sdn-definition):

> \[SDN is\] The physical separation of the network control plane from the forwarding plane, and where a control plane controls several devices.

Does this definition make sense or is it too limiting? Is there more to SDN? Would a broader scope make more sense?
<!--more-->
### A Bit of a History

It's worth looking at the [founding members of ONF](https://www.opennetworking.org/news-and-events/press-releases/261-onf-formed-to-speed-network-innovation) and their interests: most of them are large cloud providers looking for cheapest possible hardware, preferably using a standard API so it can be sourced from multiple suppliers, driving the prices even lower. Most of them are big enough to write their own control plane software (and Google already did).

A separation of control plane (running their own software) and data plane (implemented in a low-cost white-label switches) was exactly what they wanted to see, and the Stanford team working on OpenFlow provided the architectural framework they could use. No wonder ONF pushes this particular definition of SDN.

### Meanwhile Deep Below the Cloudy Heights

I have yet to meet a customer (academics might be an exception) that would consider writing their own control-plane software; most of my customers [aren't anywhere close to writing an SDN application](https://blog.ipspace.net/2013/09/do-you-really-want-to-program-your.html) on top of a controller framework (Open Daylight, Cisco XNC or HP VAN SDN controller).

{{<note>}}Buying a shrink-wrapped application bundled with commercial support might be a different story ... but then nobody really cares whether such a solution uses OpenFlow or [RFC 2549](http://tools.ietf.org/html/rfc2549); the protocols and encapsulation mechanisms used within a controller-based network solution are often proprietary and thus hard to troubleshoot anyway.{{</note>}}

On the other hand, I keep hearing about common themes:

-   The need for [faster, more standardized, and automated provisioning](https://blog.ipspace.net/2013/03/what-did-you-do-to-get-rid-of-manual.html);
-   The need for programmable network elements and vendor-neutral programming mechanisms (I'm looking at you, [netmod working group](http://datatracker.ietf.org/wg/netmod/));
-   Centralized policies and decision making based on end-to-end visibility;
-   Easier integration of network elements with orchestration and provisioning systems.

Will physical separation of control and forward plane solve any of these? It might, but [there are numerous tools out there](https://blog.ipspace.net/2013/04/the-many-paths-to-sdn.html) that can do the same without overhauling everything we've been doing in the last 30 years.

We don't need the physical separation of control plane to solve our problems (although the ability to control individual forwarding entries does help) ... and it will probably take a decade before we glimpse the promised savings of whitelabel switches and open-source software (even [Greg Ferro stopped believing that](https://www.networkcomputing.com/networking/sdn-doesnt-mean-cheaper-networking)).

### Now What?

Does it make sense to accept the definition of SDN that makes sense to ONF founding members but not to your environment? Shall we strive for a different definition of SDN or just move on, declare it as meaningless as the clouds, and focus on solving our problems? Would it be better to talk about NetOps? Share your thoughts in the comments.
