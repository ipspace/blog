---
title: "EVPN on Cisco IOS/XE: Configuration Notes"
date: 2026-02-12 07:41:00+0100
tags: [ evpn ]
evpn_tag: details
---
After reading the [L2 Vxlan On Catalyst](https://michaelbecze.github.io/blog/2026/01/25/L2-Vxlan-on-Catalylst.html) blog post, I decided to add EVPN configuration templates to _netlab_-supported Cisco IOS/XE devices. It wasn't the easiest [EVPN implementation](https://netlab.tools/module/evpn/#platform-support) I encountered; here's what I learned (hoping you'll [find it helpful](https://xkcd.com/979/)).

Starting with the trivial hiccups:
<!--more-->
* Use software release 17.16.01a or later. It looks like you can configure EVPN-with-VXLAN on Cisco IOS/XE virtual machines in some prior releases, but it doesn't work (well?). Cisco IOS/XE running on physical hardware [seems to be more reliable](#2884).
* I was able to make EVPN with VXLAN work on Catalyst 8000v, Cisco IOL, and Cisco IOL layer-2 image. The CSR image is not new enough (IOS/XE 17.13 supports EVPN over MPLS but not over VXLAN)
* Catalyst 8000v and CSR can do VXLAN with static ingress replication. The exact same configuration is accepted by Cisco IOL, but does not work.

Next, the mandatory [router-versus-switch](https://blog.ipspace.net/2022/09/interfaces-ports/) brouhaha:

| IOS/XE routers (Cisco IOL) | IOS/XE switches (Cisco IOL L2) |
|----------------------------|--------------------------------|
| Has **BDI** interface | Has **vlan** interface |
| Use **bridge-domain** configuration | Use **vlan configuration** |
| Use **service instance** for access VLAN | Use **switchport access vlan** for access VLAN |
| Add **service instance** to **bridge-domain** | VLAN is built from **switchport** VLAN values |
{.fmtTable}

That brings us to the EVPN bits:

* You create an EVPN MAC VRF with the **l2vpn evpn instance** configuration block in which you specify the EVPN instance ID (EVI), RT/RD values, and the encapsulation. 
* After creating the MAC VRF instance, you can add it as a **member** of a **bridge-domain** or **vlan configuration**. That's also where you specify EVI-to-VNI (VXLAN Network Identifier) mapping (totally obvious, right?).
* Oh, the **member evpn-instance** command does not work[^ENA] until you configure **host-reachability protocol bgp** on the NVE (VXLAN) interface.

[^ENA]: It doesn't even appear in the on-demand help

That worked well for L2-only scenarios, as well as asymmetric IRB and centralized routing on IOL. IOL layer-2 image (IOLL2) failed those tests -- the VLAN interfaces are *down* unless an Ethernet interface belonging to that VLAN is *up*[^VLL]. You have to disable the **autostate** test on the VLAN interfaces to make many IRB scenarios work.

[^VLL]: One would hope that someone would realize it might make sense to treat the VXLAN tunnel as another VLAN interface (like all other platforms). Alas, we weren't so lucky.

But wait, it only gets better if you want to be a member of the Kool GIFEE crowd and run [EVPN-over-EBGP](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) (even the sane *[direct EBGP sessions](/2024/10/evpn-designs-ebgp/)* scenario):

* The EBGP EVPN routes with loopbacks as the next hop (the usual setup) *are not accepted* unless the EBGP session is configured as an **ebgp-multihop** session. I found no other nerd knob that would say "EBGP next hop could be anything."
* IOS/XE EVPN implementation desperately tries to change the EVPN BGP next hop on the EBGP sessions. The **neighbor next-hop-unchanged** (the usual fix) command didn't work for me; I had to create a route map that set the **ip next-hop** to **unchanged** and apply it to outbound EVPN updates.

On the positive side, once you figure things out, even the crazy [EBGP-over-EBGP](/2024/10/evpn-designs-ebgp-ebgp/) and [IBGP-over-EBGP](/2024/11/evpn-designs-ibgp-ebgp/) scenarios work flawlessly.

Finally, I haven't mustered the courage yet to try out the *transit VNI* and *symmetrical IRB*. I find the idea of configuring a full-blown VLAN for the transit VNI rather than having a single command within the BGP IP VRF configuration a bit disgusting. More to come...

### Revision History

2026-02-12
: Added a pointer to a comment claiming EVPN/VXLAN runs in release 16.12 on ASR1K.
