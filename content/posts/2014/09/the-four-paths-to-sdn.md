---
date: 2014-09-16 06:57:00+02:00
dcbgp_tag: sdn
lastmod: 2023-02-28 17:46:00
series:
- dcbgp
tags:
- SDN
- OpenFlow
- BGP
title: The Four Paths to SDN
url: /2014/09/the-four-paths-to-sdn/
---
After the initial onslaught of SDN washing, four distinct approaches to SDN have started to emerge, from centralized control plane architectures to smart reuse of existing protocols.

As always, each approach has its benefits and drawbacks, and there's no universally best solution. You just got four more (somewhat immature) tools in your toolbox. And now for the details.
<!--more-->

### Control-Data Plane Separation

The "original" (or shall I say orthodox) [SDN definition](https://www.opennetworking.org/sdn-resources/sdn-definition) comes from Open Networking Foundation and calls for a strict separation of control- and data planes, with a single control plane being responsible for multiple data planes.

That definition, while [serving the goals of some ONF founding members](/2014/01/what-exactly-is-sdn-and-does-it-make/), is at the moment mostly irrelevant for most enterprise or service provider organizations, who cannot afford to [become a router manufacturer](/2012/05/openflow-google-brilliant-but-not/) to build a few dozens of WAN edge routers. Also, [almost nobody is using OpenFlow](/2022/05/openflow-still-kicking/) and [Open Daylight seemed to be pretty much dead in 2017](/2017/05/is-anyone-using-open-daylight/) (assuming you'd want to use an architecture with a [single central failure point](/2014/09/controller-cluster-is-single-failure/) in the first place).

FYI, I'm not blaming OpenFlow. OpenFlow is just a low level tool that could be extremely handy when you're trying to implement unusual ideas... if only it were implemented on recent gear.

I am positive there will always be people building [OpenFlow controllers controlling forwarding fabrics](/2013/09/openflow-fabric-controllers-are-light/) (see also: [Faucet](/2020/10/faucet-deep-dive/)), but they might eventually realize what a monumental task they undertook when they'll have to reinvent all the wheels networking industry invented in the last 30 years including:

-   Topology discovery;
-   Fast failure detection (including detection of bad links, not just lost links);
-   Fast reroute around failures;
-   Path-based forwarding and prefix-independent convergence;
-   Scalable linecard protocols (LACP, LLDP, STP, BFD ...).

### Overlay Virtual Networks

The proponents of overlay virtual networking solutions use the same architectural approach that worked well with Telnet (replacing X.25 PAD), VoIP (replacing telephone exchanges) or iSCSI, not to mention the global Internet -- reduce the complexity of the problem by decoupling transport fabric from edge functionality (a more cynical mind might be tempted to quote [RFC 1925](http://tools.ietf.org/html/rfc1925) section 2.6a).

The decoupling approach works well assuming there are no leaky abstractions (in other words, the overlay can ignore the transport network -- which wasn't exactly the case in Frame Relay or ATM networks). Overlay virtual networks work well over fabrics with equidistant endpoints, and fail as miserably as any other technology when being misused for long-distance VLAN extensions.

### Vendor-specific APIs

After the initial magical dust of SDN-washing settled down, only a few vendors remained standing (I'm skipping those that allow you to send configuration commands in XML envelope and call that programmability):

-   Arista has eAPI (access to EOS command line through JSON-formatted REST calls) as well as the capability to install any Linux component on their switches, and use programmatic access to EOS data structures (sysdb);
-   Cisco has NX-API which is slightly better than sending configuration commands in XML envelopes -- it can accept structured XML data.
-   Juniper has some SDK that's safely tucked behind a partner-only regwall. Just the right thing to do.
-   F5 had [iRules and iControl for years](https://devcentral.f5.com/articles/what-is-icontrol) (and [there's a Perl library to use it](https://metacpan.org/pod/BigIP::iControl), which is totally awesome).

Have I missed anyone? Please write a comment (and no, I don't want to hear about [NETCONF](/2012/06/netconf-expect-on-steroids/) support).

Not surprisingly, vendors love you to use their API. After all, that's the ultimate lock-in they can get.

### Reuse of Existing Protocol

While the vendors and the marketers were fighting the positioning battles, experienced engineers did what they do best -- they found a solution to a problem with the tools at hand. Many scalable real-life SDN implementations (as opposed to *works great in PowerPoint* ones) [use BGP to modify forwarding information in the network](/2013/10/exception-routing-with-bgp-sdn-done/) (or even filter traffic with BGP FlowSpec), and implement programmatic access to BGP with something like ExaBGP.

Also, don't forget that we've been using remote-triggered black holes for years ([the RFC describing it](http://tools.ietf.org/html/rfc5635) was published in 2009, but the technology itself is way older) -- we just didn't know [we were doing SDN back in those days](/2013/11/we-had-sdn-in-1993-and-didnt-know-it/).

Finally, controllers focused on device- or service provisioning or orchestration commonly use existing management plane protocols like NETCONF.


### Which one should I use?

You know the answer: it depends (you'll find the details in the [SDN Deployment Considerations](http://www.ipspace.net/SDN_Deployment_Considerations) webinar).

* If you're planning to implement novel ideas in the data center, overlay virtual networks might be the way to go (more so as you can change the edge functionality without touching the physical networking infrastructure).
* Do you need flexible dynamic ACLs or PBR? Use DirectFlow if you have Arista switches, or BGP FlowSpec.
* Looking for a large-scale solution that controls the traffic in LAN or WAN fabric? BGP might be exactly what you need.
* Finally, you can do things you cannot do with anything else with some vendor APIs (but do remember the price you're paying).

### Need More Information?

You'll find tons of real-life details vendors usually try to handwave over in the [ipSpace.net SDN resources](http://www.ipspace.net/SDN).

### Revision History

2023-02-28

: * OpenFlow and Open Daylight are mostly dead
: * Cisco OnePK is definitely gone for good
: * XMPP never really took off (apart from its use within Contrail)
: * OpFlex is still there, but I was told it's a royal pain to use, so I removed it from the blog post.
: * BGP FlowSpec is recommended as the tool to implement ACL/PBR instead of OpenFlow
