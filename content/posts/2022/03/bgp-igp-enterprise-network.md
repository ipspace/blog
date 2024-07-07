---
title: "Combining BGP and IGP in an Enterprise Network"
date: 2022-03-28 08:42:00
lastmod: 2024-05-31 13:51:00+02:00
tags: [ BGP, IP routing, design ]
---
Syed Khalid Ali left the following question on an old blog post [describing the use of IBGP and EBGP in an enterprise network](/2011/08/ibgp-or-ebgp-in-enterprise-network/):

> From an enterprise customer perspective, should I run iBGP, iBGP+IGP (OSPF/ISIS/EIGRP), or IGP with mutual redistribution on the edge routers? I was hoping you could share some thoughtful insight on when to select one over the other.

We covered many relevant details in the [January 2022 Design Clinic](https://my.ipspace.net/bin/list?id=Design#2022_01); here's the CliffNotes version. Remember that the road to hell (and broken designs) is paved with great recipes and best practices and that I'm presenting a black-and-white picture because I don't feel like transcribing our discussion into an oversized blog post. People wrote books on this topic; search for "Russ White books" to find a few.

Finally, there's no good substitute for understanding how things work (which brings me to [another webinar](https://www.ipspace.net/How_Networks_Really_Work) ;).
<!--more-->
Let's start with the basics:

* Contrary to what many data center networking vendors tell you, you might not need BGP in your data center. Contrary to what many SD-WAN vendors tell you, you might need it anyway. As always, it depends (more below).
* Two-way redistribution is terrible. It can be done, and if you're willing to live with the resulting complexity and want to have fun troubleshooting sessions when things go wrong, you could get it to work. For everyone else, I have just one word of advice: DON'T.

### Do You Need BGP or Not?

Here are a few good reasons why you might want to use BGP in your network[^NV]:

[^NV]: "Because my vendor told me to do so" is not one of them.

* If you want to **advertise your address space to the public Internet**. BGP is the only sane way to go if you need redundant Internet connectivity.
* If you plan to **run services that need BGP**, for example, EVPN. In that case, please use the [simplest possible design](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) (IBGP with IGP -- [more details](/series/dcbgp/)). [You're not Microsoft](/2017/11/bgp-as-better-igp-when-and-where/), and [don't have the scaling challenges](https://www.ipspace.net/Data_Center_BGP/BGP_Fabric_Routing_Protocol) that prompted them to use EBGP as an IGP.
* If you have **too many prefixes and hit IGP scaling limits**. In this case, you might have to implement an edge IGP (to collect prefixes) and a different core IGP (to support IBGP). Does this sound too complex? It is; OSPF areas and route summarization might be a better fit unless you're dealing with a giant organically grown mess. Also, today's CPUs are a bit faster than the [last time I faced this particular design challenge](/2024/05/worth-reading-ospf-protocol-analysis/).
* If you insist on **having thousands of routers connected to the same subnet** (typically Carrier Ethernet or DMVPN). IGPs are delicate souls and were not designed to survive such abusive behavior.
* If you want to **implement routing policies** that are more complex than "use LTE for backup," which can be solved with link cost. BGP is usually warranted in large multinational core networks with expensive core links. Use IBGP within regions (where you don't care about routing policy) and EBGP between the regions -- AS path is a nice mechanism to keep track of the regions the traffic would have to traverse.
* If you're **using MPLS/VPN services** and want to retain your sanity, run EBGP with the service provider. I covered that scenario in the _[Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)_ webinar.
* If you're running a **routing protocol with servers or VM instances** in your data center, use EBGP to [build a trust barrier](/2013/08/virtual-appliance-routing-network/) between network and hosts.[^MF] However, there's usually no need to propagate these more specific routes beyond the data center edge -- advertise a summary prefix (or a few of them) into the WAN network and move on.

Have I missed something? Please write a comment!

[^MF]: IBM mainframes supported only OSPF a long while ago, resulting in designs where a single link failure would inadvertently turn the mainframe into the most expensive (and slowest) core router you've ever seen.

### A Word on Redistribution

There are at least two ways to avoid the need for two-way redistribution (keeping in mind I'm painting a coarse black-and-white picture).

**Run IGP in parallel with BGP**. Carry all relevant prefixes in both protocols or fine-tune what information you're carrying in BGP. For example, if you need BGP to support EVPN, you might not need the BGP IPv4 address family.

**Make BGP your core routing protocol**. Ensure you're running BGP on every hop between any two BGP speakers[^BFC], and advertise the default route or a set of aggregate prefixes into IGP. If that's hard to implement, extend BGP to the point where it's feasible to advertise a default route into IGP.

{{<note info>}}For this approach to make sense, you should have at least some EBGP in your network. The proof is left as an exercise for the reader.{{</note>}}

For example, you might run EBGP with your MPLS/VPN provider and another EBGP session with your ISP. Run IBGP on every hop between the Internet Edge routers and CE routers [^VLAN]. Advertise RFC 1918 summary prefixes into IGP from the CE routers and the default route from the Internet Edge routers.

[^VLAN]: Or stretch a VLAN between them. I don't believe I just wrote that ;)

[^BFC]: Of course, you could also build a BGP-free MPLS core, but we agreed to keep things simple, right? 

### Default Routing

Instead of running BGP everywhere or having two-way redistribution, you could advertise the default route from all BGP speakers into IGP; the BGP router closest to the user(s) will pick up the traffic and sort it out.

However, every router *in any possible IP transit path* between two BGP routers must have enough information to determine which BGP router should be the next hop without generating a forwarding loop. To meet this requirement, you could create non-IP paths between BGP routers (VLANs, MPLS LSPs, VXLAN tunnels) or insert enough information into whatever routing protocol the transit routers use.

### Revision History

2024-05-31
: Expanded the _default routing_ section based on a [user comment](#2279).

2022-03-29
: Added _routing on servers_ use case based on feedback from Sander Steffann.

2022-03-31
: Added _redundant Internet connectivity_ use case
