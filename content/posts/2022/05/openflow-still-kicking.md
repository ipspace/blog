---
comment: 'More than a decade after the Open Networking Foundation started the OpenFlow/SDN
  hype (the blog post was written in 2022), OpenFlow remains a niche tool, and SDN
  means whatever you want it to mean.


  I would call that result a dismal failure; for whatever reason the (former) SDN
  evangelists tend to disagree with me and try to paint the SDN world in rosy colors.
  Judge for yourself ;)

  '
date: 2022-05-19 06:31:00+00:00
lastmod: 2022-05-20 10:20:00
sdn_hype_tag: back
series:
- sdn_hype
tags:
- OpenFlow
title: Is OpenFlow Still Kicking?
---
Continuing the _[how real is the decade-old SDN hype](/2022/05/network-hardware-disaggregation-2022.html)_ thread, let's try to figure out if anyone still uses OpenFlow. OpenFlow was [declared dead](/2016/12/response-on-death-of-openflow.html) by the troubadour of the SDN movement in 2016, so it looks like the question is moot. However, nothing ever dies in networking (including [hop-by-hop IPv6 extension headers](/2022/04/hop-by-hop-pmtud.html)), so here we go.

### Why Would One Use OpenFlow?

Ignoring for the moment the embarrassing _[we solved the global load balancing](/2011/10/openflow-and-state-explosion.html) with [per-flow forwarding](/2022/03/flow-based-forwarding.html)_ academic blunders[^SCOW], OpenFlow wasn't the worst tool for programming forwarding exceptions (ACL/PBR) into TCAM.
<!--more-->
I wouldn't be surprised to find it used to implement programmable patch panels, [sometimes known as *access switches*](/2015/12/running-open-daylight-in-production.html) or *virtual circuit switching* in service provider networks. Even in those cases, smart engineers would probably combine circuit-programming capabilities of OpenFlow with local control plane that would detect failures and trigger failovers.

[^SCOW]: See also: [spherical cow in vacuum](https://en.wikipedia.org/wiki/Spherical_cow)

### Is Anyone Still Supporting OpenFlow?

OpenFlow hype started in large data centers, so I first checked whether Arista[^ARISTA] still supports it. EOS 4.28.0F User Manual does mention OpenFlow, but the implementation hasn't changed in years -- EOS supports only OpenFlow 1.0 on ancient 7050/7050X switches. It looks like nobody large enough to interest Arista is asking for an OpenFlow implementation on a data center forwarding ASIC designed in the last decade.

Arista isn't the only vendor dealing with the remnants of the OpenFlow hype. It looks like [Alcatel Lucent also supports OpenFlow 1.3 on old hardware](/2022/05/openflow-still-kicking.html#1269), and I'm positive there are other vendors that have to do the same. On the other hand, Broadcom seem to have [stopped their OF-DPA efforts](https://twitter.com/networkservice/status/1527279230383337474); the latest commit in the [OF-DPA repository](https://github.com/Broadcom-Switch/of-dpa) was made 6 years ago.

[^ARISTA]: I'm assuming a second vendor in a large-enough market segment would be interested in implementing things customers want to buy.

Could we then declare OpenFlow a relic of the past? Maybe not. Another interesting source of information is the [Faucet SDN controller](https://docs.faucet.nz/en/latest/)[^FAUCET]. I looked at them in 2019 when preparing for a [chat with Nick Buraglio](/2019/04/using-faucet-to-build-sc18-network-with.html), and found them to be pretty conservative -- their [vendor-specific documentation](https://docs.faucet.nz/en/latest/vendors/index.html) always includes whatever they thought would work reasonably well[^PIPELINE].

[^FAUCET]: The only SDN controller I'm aware of that wasn't started as a marketing exercise.

[^PIPELINE]: Faucet is using a [multi-table pipeline](https://docs.faucet.nz/en/latest/architecture.html#faucet-openflow-switch-pipeline), which means that you can't use it with switches that don't support OpenFlow 1.3... and if your boxes don't support OpenFlow 1.3 in 2022, I really don't want to hear about them.

Their vendor list didn't change much over the years. NoviFlow has been there forever[^NOVIFLOW], I was pleasantly surprised to see [Aruba switches](https://docs.faucet.nz/en/latest/vendors/hpe/README_Aruba.html) on the list, and totally shocked to see [Cisco Catalyst 9000](https://docs.faucet.nz/en/latest/vendors/cisco/README_Cisco.html) -- OpenFlow has been implemented in IOS XE. Looks like there's a very large customer out there using OpenFlow on Catalyst switches.

[^NOVIFLOW]: It looks like NoviFlow pivoted away from hardware. OpenFlow switches are listed under _legacy network switching products_ on their website, but their OpenFlow agent seems to be running on whitebox switches using Barefoot/Intel Tofino chipset or Mellanox NPUs.

### Production Deployments

Readers of my blog sent me pointers to three publicly-known OpenFlow production deployments:

* Telstra is using OpenFlow and a homegrown SDN controller in their WAN network. [More details](https://www.slideshare.net/apnic/openkilda-stream-processing-meets-openflow), [source code](https://github.com/telstra/open-kilda).
* While Google seems to be [pushing P4 in Open Networking Foundation](/2022/05/network-hardware-disaggregation-2022.html#1237), they're still [talking about OpenFlow controllers running their B4 network](https://www.usenix.org/system/files/nsdi21-ferguson.pdf). Have to figure out what the latest article is all about; the [OpenFlow hype they generated almost exactly a decade ago](/2012/05/openflow-google-brilliant-but-not.html) was just a router built from pizza box switches and tons of ~~duct tape~~ external cables.
* Comcast [deployed](https://techblog.comsoc.org/2019/09/14/comcast-puts-onf-trellis-software-into-production/) OpenFlow-based [leaf-and-spine fabrics](https://opennetworking.org/reference-designs/trellis/) in 2019[^DEADHORSE]. The Trellis reference design claims to be based on OF-DPA[^TRELLIS], and considering Broadcom's lack of interest in OF-DPA (see above), I have a funny feeling that someone desperately tried to justify a wrong choice they made. According to a [later paper](https://dl.ifip.org/db/conf/ondm/ondm2021/1570726812.pdf), that deployment is used in 25 leaf-and-spine fabrics and services 160K subscribers. Comcast has over 34 million subscribers, so the whole thing looks like another Terastream project to me[^TS].
* ESnet was at one time running OpenFlow-based network built from Brocade MLX switches. I have no idea whether they're still doing it, but that would be as relevant as COBOL on IBM 370 mainframes.

[^DEADHORSE]: That would be three years after OpenFlow was declared dead. Were they trying to revive a dead horse instead of flogging it?

[^TRELLIS]: Or maybe ONF is just super-sloppy updating their materials to [reflect their own announcements](https://opennetworking.org/news-and-events/blog/stratum-now-powers-trellis-and-odtn-opening-the-door-to-embedding-network-functions-into-the-fabric/), which is also telling us something.

[^TS]: Terastream generated huge amount of publicity when it was [announced in 2012](https://www.telekom.com/en/media/media-information/archive/deutsche-telekom-tests-terastream-the-network-of-the-future-in-croatia-358444). The hype [continued in 2018](https://www.lightreading.com/automation/dts-terastream-a-bigger-splash/d/d-id/746072), but for whatever incomprehensible reason, its demise in 2021 wasn't made public. German journalists had to [pry the information from Deutsche Telekom](https://www.golem.de/news/terastream-telekom-stellt-pilotprojekt-fuer-revolution-von-glasfaser-ein-2103-155159.html).

### Have I missed something?

Is anyone else actively supporting OpenFlow? I'd love to hear from you -- your comments (preferably including links to documentation) would be most welcome. In case you want to send me a private message, you already have my email address if you have an [ipSpace.net subscription](https://www.ipspace.net/Subscription/), or if you're subscribed to my [SDN/automation mailing list](https://www.ipspace.net/Subscribe/Five_SDN_Tips), and there's the [Contact Us form](https://www.ipspace.net/Contact) for everyone else.

### Revision History

2022-05-20
: Added information based on user responses
: * OpenFlow support on ALE switches
: * Broadcom dropping OF-DPA
: * Comcast Trellis deployment
