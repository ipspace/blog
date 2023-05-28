---
title: "Path Failure Detection on Multi-Homed Servers"
date: 2023-05-30 06:32:00
tags: [ data center, switching ]
---
**TL&DR:** Installing an Ethernet NIC with two uplinks in a server is easy[^2NIC]. Connecting those uplinks to two edge switches is common sense[^VMW]. Detecting physical link failure is trivial in Gigabit Ethernet world. Deciding between two independent uplinks or a link aggregation group is interesting. Detecting path failure and disabling the useless uplink that causes traffic blackholing is a living hell (more details in this [Design Clinic question](https://designclinic.ipspace.net/topic/dual-homing-hosts/)).

[^2NIC]: Bonus points if you realized a NIC could fail and installed two NICs.

[^VMW]: I did get a "why would anyone want to do that" question from someone working at VMware, but I considered that par for the course. If you claim to be a networking engineer but can't answer that question, OTOH, you have a bigger problem than what this blog post discusses.

Want to know more? Let's dive into the gory details.
<!--more-->
### Detecting Link Failures

Imagine you have a server with two uplinks connected to two edge switches. You want to use one or both uplinks[^SLB] but don't want to send the traffic into a black hole, so you have to know whether the data path between your server and its peers is operational.

[^SLB]: Skipping the load balancing can-of-worms for the moment.

The most trivial scenario is a link failure. Ethernet Network Interface Card (NIC) detects the failure, reports it to the operating system kernel, the link is disabled, and all the outgoing traffic takes the other link.

Next is a transceiver (or NIC or switch ASIC port) failure. The link is up, but the traffic sent over it is lost. Years ago, we used protocols like [UDLD](https://blog.ipspace.net/2012/09/do-we-need-lacp-and-udld.html) to detect unidirectional links. Gigabit Ethernet (and faster technologies) [include Link Fault Signalling ](https://blog.ipspace.net/2020/11/detecting-network-failure.html)that can detect failures between the transceivers. You need a control-plane protocol to detect failures beyond a cable and directly-attached components.

### Detecting Failures with a Control-Plane Protocol

We usually connect servers to VLANs that sometimes stretch more than one data center (because why not) and want to use a single IP address per server. That means the only control-plane protocol one can use between a server and an adjacent switch is a layer-2 protocol, and the only choice we usually have is LACP. Welcome to the beautifully complex world of [Multi-Chassis Link Aggregation](/series/mlag.html) (MLAG)[^HC].

[^HC]: Most of MLAG's complexity is hidden from the server administrators, but that does not mean it's not there waiting to explode in your face.

Using LACP/MLAG[^MLON] to detect path failure is a brilliant application of RFC 1925 Rule 6. Let the networking vendors figure out which switch can reach the rest of the fabric, hoping the other member of the MLAG cluster will shut down its interfaces or stop participating in LACP. Guess what -- they might be as clueless as you are; [getting a majority vote in a cluster with two members is an exercise in futility](/2017/01/never-take-two-chronometers-to-sea.html). At least they have a [peer link bundle](https://blog.ipspace.net/2022/06/mlag-deep-dive-overview.html) between the switches that they can use to shuffle the traffic toward the healthy switch, but not if you use a [virtual peer link](https://blog.ipspace.net/2023/05/mlag-without-peer-link.html). Cisco [claims to have all sorts of resiliency mechanisms in its vPC Fabric Peering implementation](https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/103x/configuration/vxlan/cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-release-103x/m_configuring_vpc_fabric_peering_93x.html), but I couldn't find any details. I still don't know whether they are implemented in the Nexus OS code or PowerPoint[^CLP].

[^MLON]: Vendors use different names like vPC for MLAG functionality. Some also call a *link aggregation group* (LAG) a *Port Channel* or an *EtherChannel*.

[^CLP]: The details are probably described in some Cisco Live presentation, but my Google-Fu is failing me.

### In a World without LAG

Now let's assume you got burned by MLAG[^DCMD], want to follow the vendor design guidelines[^VDG], or want to use all uplinks for iSCSI MPIO or vMotion[^VMLG]. What could you do?

[^DCMD]: I know about quite a few data center meltdowns caused by MLAG bugs, but I guess not everyone gets exposed to so many pathological cases.

[^VDG]: For example, VMware recommends independent uplinks in NSX-T deployments.

[^VMLG]: Multi-interface vMotion or iSCSI MPIO [needs multiple IP addresses per host](/kb/Layer3Fabrics/20-apps.html) with traffic for an individual IP address tied to a particular uplink. You cannot implement that with a link aggregation group.

Some switches have uplink tracking -- the switch shuts down all server-facing interfaces when it loses all uplinks -- but I'm not sure this functionality is widely available in data center switches. I already mentioned Cisco's lack of details, and Arista seems no better. All I found was a brief mention of the **uplink-failure-detection** keyword without further explanation.

Maybe we could solve the problem on the server? VMware has beacon probing on ESX servers, but they don't believe in miracles in this case. You need at least three uplinks for beacon probing. Not exactly useful if you have servers with two uplinks (and few people need more than two 100GE uplinks per server).

Could we use the first-hop gateway as a witness node? Linux bonding driver supports ARP monitoring and sends periodic ARP requests to a specified destination IP address through all uplinks. Still, according to the engineer asking the Design Clinic question, that code isn't exactly bug-free.

Finally, you could accept the risk -- if your leaf switches have  [four](https://blog.ipspace.net/2023/03/leaf-spine-theory-reality.html) ([or six](/2023/03/leaf-switches-four-uplinks.html)) uplinks, the chance of a leaf switch becoming isolated from the rest of the fabric is pretty low, so you might just give up and stop worrying about [byzantine failures](https://en.wikipedia.org/wiki/Byzantine_fault).

### BGP Is the Answer. What Was the Question?

What's left? BGP, of course. You could install FRR on your Linux servers, run [BGP with the adjacent switches](https://blog.ipspace.net/2016/02/running-bgp-on-servers.html) and advertise the server's loopback IP address. To be honest, properly implemented RIP would also work, and I can't fathom why we couldn't get a decent host-to-network protocol in the last 40 years[^ESIS]. All we need is a protocol that:

-   Allows a multi-homed host to advertise its addresses
-   Prevents route leaks that could [cause servers to become routers](https://blog.ipspace.net/2016/09/why-would-i-use-bgp-and-not-ospf.html)[^IBM]. BGP does that automatically; we'd have to use hop count to filter RIP updates sent by the servers[^NHC].
-   Bonus point: run that protocol over an unnumbered switch-to-server link.

[^ESIS]: OSI had ES-IS protocol from day one. Did the IETF community [feel the urge to be different](https://blog.ipspace.net/2016/11/could-you-use-is-is-instead-of-bgp-for.html), or was everything OSI touched considered cooties?

[^IBM]: IBM was running OSPF on mainframes, and it was [perfectly possible to turn your mainframe into the most expensive core router](https://blog.ipspace.net/2016/03/dont-run-ospf-with-your-customers.html) you've ever seen with a dismal packet forwarding performance.

[^NHC]: Probably doable with a route map matching on metric.

It sounds like a great idea, but it would require OS vendor support[^VMF] and [coordination between server- and network administrators](https://blog.ipspace.net/2016/03/sysadmins-shouldnt-be-involved-with.html). Nah, that's never going to happen in enterprise IT.

No worries, I'm pretty sure one or the other SmartNIC[^DPU] vendor will eventually start selling "a perfect solution": run BGP from the SmartNIC and adjust the link state reported to the server based on routes received over such session -- another perfect example of RFC 1925 rule 6a.

[^VMF]: I'm looking at you, VMware.

[^DPU]: Known as Data Processing Unit in marketese.

### More Details

* Server-to-network multihoming is one of many topics covered in  _[Site and Host Multihoming](https://blog.ipspace.net/series/multihoming.html)_ resources.
* You might want to explore _[Redundant Layer-3-Only Data Center Fabrics](/kb/Layer3Fabrics/)_

[ipSpace.net subscribers](https://www.ipspace.net/Subscription/) can also:

* Read the [Redundant Server-to-Network Connectivity](https://www.ipspace.net/Redundant_Server-to-Network_Connectivity) case study.
* Watch the [dual-homed servers discussion](https://my.ipspace.net/bin/get/Design/21.12.03%20-%20Multi-Homed%20Servers.mp4?doccode=Design) in the [ipSpace.net Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic).
