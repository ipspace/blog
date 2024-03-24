---
title: "Repost: Think About the 99% of the Users"
date: 2024-04-23 08:37:00+0100
tags: [ design ]
---
Daniel left a [very relevant comment](https://blog.ipspace.net/2024/03/fabric-designs-size-matters.html#2132) on my [Data Center Fabric Designs: Size Matters](https://blog.ipspace.net/2024/03/fabric-designs-size-matters.html) blog post, describing how everyone rushes to sell the newest gizmos and technologies to the unsuspecting (and sometimes too-awed) users[^ABC]:

[^ABC]: I let Grammarly do a bit of a cleanup.
---

Absolutely right. I'm working at an MSP, and we do a lot of project work for enterprises with between 500 and 2000 people. That means the IT department is not that big; it's usually just a cost center for them.
<!--more-->
Then, one of us comes in (often the presales guys first) and makes suggestions on what new shiny thing they could buy. Cisco ACI for your DC that doesn't change at all! VMware NSX for your 4 VMware servers, and you can save on networking! VXLAN EVPN for your four networking guys who do mostly client patching (the cables), have never heard of an overlay, and haven't touched BGP in their lives! YAY! Don't get me started on the automation stuff out there. Most companies are way over their head with much of that stuff. And it all comes crashing down if the wrong guy leaves for another better-paying job.

Be realistic and consult (you MSP guys) and buy (you enterprise guys) the right tool for your team that meets your needs. Maybe two or four switches with MLAG/vPC are not cool and shiny, but they get the job done, and you can troubleshoot them at 2 AM. Overlays in a campus network are really practical and can help solve many "issues" (primarily issues caused by someone who doesn't want or doesn't know how to do it better). But can you support it? As we started with campus fabrics (especially Cisco's SDA), most customers were shocked to learn about dot1x and what it means to roll that out. And that's just the start of all that. We always recommend dot1x for different reasons, but most companies can't handle that on their own. Those are all the 99%.

And what are we all talking about? The new stuff for the 1%. It takes years for that to trickle down to the 99%.

---

Speaking of BGP: did you know that most data center fabrics ([including early AWS fabrics](https://medium.com/the-elegant-network/what-ive-learned-about-scaling-ospf-in-datacenters-7100c33ce63c)) are [small enough to run OSPF as the IGP](https://blog.ipspace.net/2018/05/is-ospf-or-is-is-good-enough-for-my.html), and that you can [build VXLAN-based L2VPN without EVPN](https://blog.ipspace.net/2022/09/mlag-bridging-evpn.html)?