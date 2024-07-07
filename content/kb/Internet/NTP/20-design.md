---
kb_section: NTP
minimal_sidebar: true
title: Design Guidelines
url: /kb/Internet/NTP/20-design/
---
Typical NTP design guidelines recommend that every NTP server uses at least two upstream servers and peers with at least one more server of the same stratum. Of course, these recommendations have to be tailored to the actual network design. For example, if you have remote sites with a single router, it makes no sense for the router to peer with anyone but the upstream routers (or central NTP servers); if the upstream connectivity is gone, it has no reasonable peers anyway.

{{<figure src="../design-non-redundant.png" caption="NTP sessions on a non-redundant site">}}

On the other hand, if you have a redundant network design that has two routers on each remote site, it’s advisable that you configure them as NTP peers; even if one of them loses upstream connectivity, it can still synchronize to the other one:

{{<figure src="../design-redundant-site.png" caption="NTP sessions on a redundant remote site">}}

The NTP protocol uses little bandwidth and CPU resources on the routers. A Cisco router sends only a few NTP packets after the reload, trying to achieve fast synchronization with the upstream NTP servers and peers. After the initial synchronization attempt, NTP packets are sent every 64 seconds to unstable peers or newly configured servers. This interval is gradually increased until the packets are sent every 1024 seconds in the steady-state conditions. It’s therefore totally harmless to implement NTP topology that follows the actual physical topology of your network. The proposed NTP topology in a typical hierarchical network design is shown in the next diagram:

{{<figure src="../design-hierarchical.png" caption="NTP sessions in a typical hierarchical network">}}

If you want to have a robust distributed NTP architecture in your network, you should allow every NTP server to use its own local clock as one of the time sources ensuring that it will continue to serve meaningful time to its client even if it loses connectivity to all upstream servers and peers. The stratum of the local clock should be set to the worst possible stratum of all the upstream servers increased by one. Setting strata of local clocks to lower values might prevent time synchronization if the central NTP server fails.

{{<figure src="../design-stratum.png" caption="Strata of local clocks in a multi-level NTP network">}}

{{<note warn>}}If you want to set the stratum of a Cisco IOS router’s local clock to X, you should configure the router to be stratum X+1 server with the **ntp master** configuration command.{{</note>}}