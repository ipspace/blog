---
title: "OpenFlow and SDN: Two Years after ONF Launch"
date: 2013-11-16 08:43:00
tags: [ OpenFlow, SDN ]
series: sdn_hype
sdn_hype_tag: back
comment:
  I was enthusiastic about OpenFlow when the vendor engineers started developing real-life solutions, but the reality has crushed all my high hopes. Approximately two and a half years after the ONF launch it was clear that things are not going well. This is what I wrote in November 2013. 
---
Major vendors (with the exception of NEC) haven’t made any progress. Juniper still hasn’t delivered on its promises. Cisco still hasn’t shipped an OpenFlow switch or an SDN controller (although they’ve announced both months ago). Brocade supposedly has OpenFlow on their high-end routers and Arista supports OpenFlow on its old high-end switch (but not in GA EOS release). 

Every major vendor is talking about SDN, but it’s mostly SDN-washing (aka CLI-in-API-disguise). Cisco is talking about OnePK, and has shipping early adopter SDK kit, but it will take a while before we see OnePK in GA code on a widespread platform. 

Startups aren’t doing any better. Big Switch is treading water and trying to find a useful use case for their controller. Nicira was acquired by VMware and is moving away from OpenFlow. Contrail was acquired by Juniper and recently shipped its product (which has nothing to do with OpenFlow and not much with SDN). LineRate Systems was acquired by F5 and disappeared.

We haven’t seen customer deployments either. Facebook is doing interesting things (but from what I’ve heard they’re not OpenFlow-based), Google has an OpenFlow/SDN deployment, but they could have done the exact same thing with classical routers and PCEP, Microsoft’s SDN is based on BGP (and works fine).

It seems like the reality hit OpenFlow and it was a very hard hit… and according to Gartner we haven’t reached the trough of disillusionment yet.
