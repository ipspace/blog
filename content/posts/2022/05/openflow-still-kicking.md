---
title: "Is OpenFlow Still Kicking?"
date: 2022-05-19 06:31:00
tags: [ OpenFlow ]
---
Continuing the _[how real is the decade-old SDN hype](/2022/05/network-hardware-disaggregation-2022.html)_ thread, let's try to figure out if anyone still uses OpenFlow. OpenFlow was [declared dead](/2016/12/response-on-death-of-openflow.html) by the troubadour of the SDN movement in 2016, so it looks like the question is moot. However, nothing ever dies in networking (including [hop-by-hop IPv6 extension headers](https://blog.ipspace.net/2022/04/hop-by-hop-pmtud.html)), so here we go.

### Why Would One Use OpenFlow?

Ignoring for the moment the embarrassing _[we solved the global load balancing](https://blog.ipspace.net/2011/10/openflow-and-state-explosion.html) with [per-flow forwarding](https://blog.ipspace.net/2022/03/flow-based-forwarding.html)_ academic blunders[^SCOW], OpenFlow wasn't the worst tool for programming forwarding exceptions (ACL/PBR) into TCAM.
<!--more-->
I wouldn't be surprised to find it used to implement programmable patch panels, [sometimes known as *access switches*](https://blog.ipspace.net/2015/12/running-open-daylight-in-production.html) or *virtual circuit switching* in service provider networks. Even in those cases, smart engineers would probably combine circuit-programming capabilities of OpenFlow with local control plane that would detect failures and trigger failovers.

[^SCOW]: See also: [spherical cow in vacuum](https://en.wikipedia.org/wiki/Spherical_cow)

### Is Anyone Still Supporting OpenFlow?

OpenFlow hype started in large data centers, so I first checked whether Arista[^ARISTA] still supports it. EOS 4.28.0F User Manual does mention OpenFlow, but the implementation hasn't changed in years -- EOS supports only OpenFlow 1.0 on ancient 7050/7050X switches. It looks like nobody large enough to interest Arista is asking for an OpenFlow implementation on a data center forwarding ASIC designed in the last decade.

Mission accomplished? Not so fast. Another interesting source of information is the [Faucet SDN controller](https://docs.faucet.nz/en/latest/)[^FAUCET]. I looked at them in 2019 when preparing for a [chat with Nick Buraglio](https://blog.ipspace.net/2019/04/using-faucet-to-build-sc18-network-with.html), and found them to be pretty conservative -- their [vendor-specific documentation](https://docs.faucet.nz/en/latest/vendors/index.html) always includes whatever they thought would work reasonably well[^PIPELINE].

Their vendor list didn't change much over the years. NoviFlow has been there forever[^NOVIFLOW], I was pleasantly surprised to see [Aruba switches](https://docs.faucet.nz/en/latest/vendors/hpe/README_Aruba.html) on the list, and totally shocked to see [Cisco Catalyst 9000](https://docs.faucet.nz/en/latest/vendors/cisco/README_Cisco.html) -- OpenFlow has been implemented in IOS XE. Looks like there's a very large customer out there using OpenFlow on Catalyst switches.

Have I missed something? Is anyone else actively supporting OpenFlow? Is anyone ([apart from Nick](https://blog.ipspace.net/2020/10/faucet-deep-dive.html)) using OpenFlow in a production network? I'd love to hear from you -- your comments (preferably including links to documentation) would be most welcome. In case you want to send me a private message, you already have my email address if you have an [ipSpace.net subscription](https://www.ipspace.net/Subscription/), or if you're subscribed to my [SDN/automation mailing list](https://www.ipspace.net/Subscribe/Five_SDN_Tips), and there's the [Contact Us form](https://www.ipspace.net/Contact) for everyone else.

[^ARISTA]: I'm assuming a second vendor in a large-enough market segment would be interested in implementing things customers want to buy.

[^FAUCET]: The only SDN controller I'm aware of that was not started as a marketing exercise.

[^PIPELINE]: Faucet is using a [multi-table pipeline](https://docs.faucet.nz/en/latest/architecture.html#faucet-openflow-switch-pipeline), which means that you can't use it with switches that don't support OpenFlow 1.3... and if your boxes don't support OpenFlow 1.3 in 2022, I really don't want to hear about them.

[^NOVIFLOW]: It looks like NoviFlow pivoted away from hardware. OpenFlow switches are listed under _legacy network switching products_ on their website, but their OpenFlow agent seems to be running on whitebox switches using Barefoot/Intel Tofino chipset or Mellanox NPUs.
