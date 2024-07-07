---
date: 2013-04-04 07:33:00+02:00
tags:
- SDN
- OpenFlow
title: The Many Paths to SDN
url: /2013/04/the-many-paths-to-sdn/
---
I did a major overhaul of my [RIPE 65 SDN presentation](https://ripe65.ripe.net/archives/video/2/) prior to [MENOG 12](http://www.menog.org/meetings/previous/menog-12/) meeting, including a more comprehensive overview of SDN-related technologies sorted by the [networking device plane](/2013/08/management-control-and-data-planes-in/) they operate on.

{{<figure src="/2013/04/s1600-SDN_Paths.png" caption="Many paths to SDN">}}
<!--more-->
[NETCONF](/2012/06/netconf-expect-on-steroids/), [OF-Config](https://www.opennetworking.org/images/stories/downloads/of-config/of-config-1.1.pdf) (a YANG data model used to configure OpenFlow devices through NETCONF) and [XMPP](http://en.wikipedia.org/wiki/XMPP) (chat protocol [creatively used by Arista EOS](https://eos.aristanetworks.com/2011/08/management-over-xmpp/)) operate at the management plane -- they can change network device configuration or monitor its state.

[IRS](/2012/08/irs-just-what-sdn-goldilocks-is-looking/) and [PCEP](http://tools.ietf.org/html/rfc5440) (a protocol used to create MPLS-TE tunnels from a central controller) operate on the control plane (parallel to traditional routing protocols), as do numerous BGP-based tools, from well-known [Remote Triggered Black Holes](http://packetlife.net/blog/2009/jul/6/remotely-triggered-black-hole-rtbh-routing/) to [Flowspec](http://tools.ietf.org/html/rfc5575) (PBR through BGP used by creative network operators like [CloudFlare](http://blog.cloudflare.com/todays-outage-post-mortem-82515)) and [BGP-LS](http://tools.ietf.org/html/draft-gredler-idr-ls-distribution-02) (export of link state topology and MPLS-TE data through BGP).

[OpenFlow](/tag/openflow/), [MPLS-TP](/2010/11/what-is-mpls-tp-and-is-it-relevant/) and [ForCES](http://datatracker.ietf.org/wg/forces/charter/) work on the data plane -- they can modify the forwarding behavior of a controlled device or intercept/inject packets.

Have I missed a relevant protocol/technology? Please write a comment!
