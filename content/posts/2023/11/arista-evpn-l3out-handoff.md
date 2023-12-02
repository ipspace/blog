---
title: "VXLAN/EVPN Layer-3 Handoff (L3Out) on Arista EOS"
date: 2023-11-20 07:11:00
tags: [ EVPN, VXLAN, WAN ]
---
A while ago, I published a blog post describing how to [establish a LAN/WAN L3 boundary in VXLAN/EVPN networks using Cisco NX-OS](/2023/09/evpn-wan-handoff-l3out.html). At that time, I promised similar information for Arista EOS. Here it is, coming straight from [Massimo Magnani](https://www.linkedin.com/in/massimo-magnani-8b3a59/). The useful part of what follows is his; all errors were introduced during my editing process.

---

In the cases I have dealt with so far, implementing the LAN-WAN boundary has the main benefit of limiting the churn blast radius to the local domain, trying to impact the remote ones as little as possible. To achieve that, we decided to go for a hierarchical solution where you create two domains, local (default) and remote, and maintain them as separate as possible. 
<!--more-->
We do that with DC gateway devices that provide a logical separation between local and remote domains by regulating how NLRIs are exchanged between them. 

We have to optimize NLRI advertisements and play with BGP next hops so that each local domain only needs to know its local gateway BGP next hop and nothing else. To do this, you need a data plane decapsulation/encapsulation (VXLAN-to-VXLAN but also VXLAN-to-MPLS) on the gateways themselves. We are doing this on our Jericho2 (and J2C, J2C+, Qumran2A) boxes, namely all the R3 and R3A devices (7280/7500/7800).

As you mentioned, all these things can become cumbersome to implement and maintain. That’s why we tried to simplify the best we could by introducing both L2/L3 hierarchical DC GW features.

In EOS, we implemented the solution depicted in RFC9104 (L2 GW) and the one from draft-ietf-bess-evpn-ipvpn-interworking (L3 GW), trying to make all the configurations and the maintenance of the solution as simple as possible.

You can configure the two domains (remote and local) at the EVPN AF level under BGP, and a couple of other commands, and most of the work is done. Then, you can have dedicated remote and local domain RDs and RTs (today, for L2, L3 will come in a later release). We can do MLAG (on DCI gateway) and anycast-ip for gateway redundancy today. We will also support the EVPN all-active GW redundancy mode in a few releases.

We have chosen to implement RFC9014 for the L2GW and IP VPN  interworking instead of the competing draft (draft-sharma-bess-multi-site-evpn) because of these advantages:

1. Interoperability: we can interoperate with a larger number of vendors
2. Multiple data plane encapsulations: the second draft only supports the VXLAN data plane;
3. No change to existing EVPN routes (the other draft adds a new ESI extended community for type-1 routes);
4. MAC mobility: with our approach (RFC9104), local MAC moves don’t trigger type-2 updates towards remote gateways;

Last but not least, we are actively looking at implementing the “Unknown MAC route” (UMR) in the future. That will significantly improve scaling and overall stability as only the gateways may keep on maintaining all the MAC Type-2 advertisements and only originate a type-2 UMR NLRI to the local leaf devices so that, in case of remote MAC churns, they will be able to “shield” the local domain from the remote faults.

---

### Revision History

2023-12-02
: Fixed the EVPN RFC number (9104 → 9014)
