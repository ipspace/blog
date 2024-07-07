---
date: 2018-01-30 09:31:00+01:00
dr_tag: vendor
high-availability_tag: dr
series:
- dr
tags:
- design
- switching
- data center
- high availability
title: 'Revisited: The Need for Stretched VLANs'
url: /2018/01/revisited-need-for-stretched-vlans/
---
Regardless of how much I write about (the [ridiculousness of using](/2015/02/before-talking-about-vmotion-across/)) stretched VLANs, I keep getting questions along the same lines. This time it's:

> What type of applications require L2 Extension and L3 extension?

I don't think I've seen anyone use *L3 extension* (after all, isn't that what Internet is all about), so let's focus on the first one.

Stretched VLANs (or L2 extensions) are used to solve a number of unrelated problems, because once a vendor sold you a hammer everything starts looking like a nail, and once you get used to replacing everything with nails, you want to use them in all possible environments, including public and hybrid clouds.
<!--more-->
Some of the challenges that I've seen solved with stretched VLANs include:

**Subnet mobility**. You must move a subnet from one site to another during disaster recovery process because the subnet (or IP addresses within the subnet) is [hard-coded in application, configuration files, or firewall/load balancer rules](/2013/04/this-is-what-makes-networking-so-complex/).

This one is easiest to solve: start using automation and make network infrastructure recovery part of your overall recovery process.

Alternatively, configure the same subnet on VLAN interfaces or firewall contexts that are shutdown during the regular operation, and enabled when needed.

For whatever reason, most everyone solves this one by stretching a VLAN between data centers (because VMware consultants told them to do so) and then [experiencing a dual-data-center meltdown](/2013/01/long-distance-vmotion-stretched-ha/) before ever having the need to do a disaster recovery.

**IP address mobility**. Similar to the one above, but caused by [cold or hot VM move](/2013/02/hot-and-cold-vm-mobility/), resulting in an IP subnet stretched across multiple sites.

You can implement this requirement without stretching a VLAN by using [host-route-based IP forwarding](/2015/04/rearchitecting-l3-only-networks/) as implemented in [Local Area Mobility](/2011/02/local-area-mobility-lam-true-story/) (requires at least Cisco IOS version 10.0), Cisco DFA, Cisco ACI, Cumulus Linux [*redistribute ARP*](/2015/08/layer-3-only-data-center-networks-with/), or any decent EVPN implementation.

However, as you usually cannot announce host routes to WAN or public Internet, this design effectively creates multi-site summarization boundary. Anyone with production-grade multi-area OSPF experience probably knows how bad this could be; everyone else should figure this one out as a nice homework assignment.

**IP multicast**. The application needs IP multicast because whatever (the only valid reasons I found: stock exchange feeds and video streaming) and it's easier to stretch a VLAN than to figure out how to spell PIM (btw, I agree with this conclusion).

Some vendors "solve" this problem by [requiring layer-2 connectivity between cluster members](/2017/11/lets-pretend-we-run-distributed-storage/) (see also: *let's offload our support costs* below).

**Simplistic routing on** **multihomed** **hosts**. I strongly suspect that most of *we need layer-2 for iSCSI* sentiment comes from inability to properly configure IP routing on multihomed iSCSI clients. VMware fixed this in recent vSphere versions, not sure what other vendors are doing.

This one is way harder than one would expect. I started writing a lengthy article on the topic and still haven't finished it because new worms keep turning up every time you turn around.

**Let's offload our support costs to customer's networking team**. A typical trick used by software vendors is to write requirements that include *must have layer-2 connectivity between hosts in a cluster* for no reason, and reject support requests from environments that violate this ridiculous CYA approach.

Famous vendors in this category:

-   VMware requiring layer-2 connectivity between kernel interfaces to run a TCP-based vMotion session between them (they got to their senses in the meantime);
-   Oracle database clusters.

Honorable mentions:

-   Nutanix distributed storage.
-   Stretched Cisco Hyperflex clusters

{{<note warn>}}The response I got from the [Hyperflex presenter](http://techfieldday.com/appearance/cisco-hyperflex-presents-at-tech-field-day-extra-at-cisco-live-europe/) @ [Tech Field Day Extra CLEUR 2018](http://techfieldday.com/event/cleur18/): \"*yes, we\'re using pure IP transport without IP multicast, and no, we haven\'t tested and validated our solution for use over routed networks*.\" Now you know.{{</note>}}

Anything else? Write a comment!

**Let's offload error detection to customer's networking team**. It's easier to [rely on Ethernet checksums than to do application-level checksums](/2015/11/ethernet-checksums-are-not-good-enough/).

Bad news: with MAC-over-IP solutions like VXLAN-with-EVPN that almost every data center switching vendor is pushing you lose end-to-end Ethernet checksum even if the whole thing still looks like a thick yellow cable.

**Non-IP protocols**. Hey, it's 2018. Let's move on.

**We want thick yellow cable**. Solutions implementing stupidities that are skirting the edges of valid Ethernet behavior and work well only on a [thick yellow cable](/2015/02/lets-get-rid-of-thick-yellow-cable/). I'm looking at you [Network Load Balancing](/2012/02/microsoft-network-load-balancing-behind/).

**Wrap-up**: It makes me sad that after all these years we still have to deal with ignorance and decade-old stupidities that refuse to die.

Fortunately, the big cloud providers don't want to budge on this one because they're focused on making money from running services instead of supporting old crap based on which VP yells louder, so most of the things I mentioned above might die in the next few decades.

For an even more cynical view, join the [Building Next-Generation Data Centers](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course and listen to what [Michele Chubirka has to say about infrastructure, security and DevOps](http://nextgendc.ipspace.net/Public:5-High-Availability_Concerns#Guest_Speaker).
