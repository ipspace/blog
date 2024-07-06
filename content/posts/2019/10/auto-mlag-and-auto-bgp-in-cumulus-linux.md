---
date: 2019-10-23 09:12:00+02:00
tags:
- bridging
- BGP
- Cumulus Linux
series: [ mlag, dcbgp ]
mlag_tag: implement
dcbgp_tag: cl
title: Auto-MLAG and Auto-BGP in Cumulus Linux
url: /2019/10/auto-mlag-and-auto-bgp-in-cumulus-linux.html
---
When I first met Cumulus Networks engineers ([during NFD9](/2015/02/networking-field-day-9-brief-recap.html)) their focus on simplifying switch configurations [totally delighted me](/2015/02/bgp-configuration-made-simple-with.html) ([video](/2015/10/video-simplify-network-configurations.html)).

{{<note>}}
I was [ranting about the more traditional approach to data center fabric configuration](/2015/05/stupidities-of-switch-programming.html) resulting in dozens if not hundreds of device configuration commands in 2013... and other vendors still haven\'t done much in this respect in the meantime.
{{</note>}}

After solving the BGP configuration challenge (could you imagine configuring BGP in a leaf-and-spine fabric with just a few commands in 2015), they did the same thing with EVPN configuration, where they decided to implement the simplest possible design ([EBGP-only fabric running EBGP EVPN sessions on leaf-to-spine links](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics)), resulting in another round of configuration simplicity.
<!--more-->
{{<note>}}
Of course you can always apply RFC 1925 Rule 6 and solve the same challenge by adding another layer of abstraction, this time using network automation with complex templates... but it turns out that the [state management needed to do that gets complex](/2017/08/challenges-of-data-center-fabric.html), and your life becomes much easier if you don't have to keep that state.
{{</note>}}

Fortunately Cumulus Networks didn't decide to rest on the laurels -- in the [Data Center Fabrics](https://www.ipspace.net/Data_Center_Fabrics) update session we ran in September 2019,[Pete Lumbis](https://www.ipspace.net/Author:Pete_Lumbis) talked about the new features they're adding to Cumulus Linux 4.0 ([videos and slide deck](https://my.ipspace.net/bin/list?id=DCFabric#CUMULUS)) - even more sane defaults, using auto-generated BGP AS numbers on leaf switches, and simplifying MLAG configuration (including peer link and server port channels) to a single command.

Here are a few more details Pete sent me:

---

AutoBGP is not magic, we are effectively building a macro that will hash the platform MAC address and generate an ASN from the 4-byte private space. We are targeting two-tier Clos networks (Superspines are hard to solve for and those folks have opinions). To avoid further complexity we are planning on doing something along the lines of "net add bgp leaf" and "net add bgp spine". If you say "spine" you get AS 4294967294. If you say "leaf" we hash against a search space of 4200000000 to 4294967293. I actually ran this against every **cl-support** (our "show tech") we've ever collected and had zero ASN collisions. 

For some of the MLAG features:

-   **MLAG Unnumbered** - This is the same as BGP unnumbered. The two MLAG peers need an L3 communication channel that is directly connected. Instead of assigning an IP address we just use the v6 LLA and discover our peer by listening for RAs on the defined bond interface.
-   **Auto Bonds** - We haven't decided if we will support this for non-MLAG scenarios, but with MLAG the idea is that when you receive an LACP packet you exchange all of that information with your MLAG peer as a "candidate bond member". If the peer also sees these LACP messages we'll just build a bond in kernel (i.e., "ip link add bond..."). This ends up eliminating \~6 lines of configuration for every server attached. 
-   **Auto MLAG identifiers** - Perhaps you still want to manually define bond ports and not just open up the world to sending you LACP messages. We can still make a life a bit easier by removing the need to define an MLAG bond identifier (Cisco uses "vpc 100" under the port channel for example) and just derive it from the received LACP messages. Auto Bonds would incorporate this.
-   **Logical MLAG Identifiers** - Okay, you don't want any of our fancy under the hood magic, you want to do everything the hard way. You have a strong desire to artisanally configure every bond on the system (or you're unwilling to pay for a license to enable LACP on your unnamed hypervisor), we are adding the ability to provide strings as MLAG identifiers, for example "mlag-id mailServer01".
