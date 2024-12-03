---
title: "netlab: Sample Cisco ASAv Topology"
series_title: "Sample Cisco ASAv Topology"
date: 2024-12-03 09:37:00+0100
tags: [ netlab ]
netlab_tag: use
---
A happy netlab user [asked for a sample Cisco ASAv topology](https://github.com/ipspace/netlab/discussions/1600) that would include an inside and an outside router.

We don't have anything similar in the [netlab examples](https://github.com/ipspace/netlab-examples) yet, so let's build a [simple topology](https://github.com/ipspace/netlab-examples/tree/master/multi-platform/asav) with two routers, a firewall, and a few hosts.

However, we have to start with a few caveats:
<!--more-->
* ASAv does not seem to be a beloved platform of [_netlab_ contributors](https://github.com/ipspace/netlab/graphs/contributors). The [initial contribution](https://github.com/ipspace/netlab/pull/635) included baseline IS-IS and BGP support, and nothing has changed ever since (see [supported platforms](https://netlab.tools/platforms/), [IS-IS platform support](https://netlab.tools/module/isis/#platform-support), and [BGP platform support](https://netlab.tools/module/bgp/#platform-support) for more details).
* Most firewall deployments use static default routing through the firewall. _netlab_ does not support static routes yet (but of course, you can add them with [custom configuration templates](https://netlab.tools/custom-config-templates/)).
* Firewalls block traffic without extra configuration, and _netlab_ does not support any firewall-related features (interface zones or security levels, NAT, or packet filters). Getting to a functioning network will inevitably require additional configuration on ASAv.

Now for the good news: ASAv supports BGP routing, so we could have an external (outside, WAN edge) router advertising the BGP default route and have ASAv propagate that default route to the inside router. The [simplest topology](https://github.com/ipspace/netlab-examples/tree/master/multi-platform/asav) would thus be:

* An outside router (**ext**) connected to ASAv outside interface.
* An inside router (**int**) connected to ASAv inside interface.
* A few hosts connected to the inside router.
* An external host connected to the outside router.

Here's how D2 thinks this topology looks like[^D2]:

{{<figure src="/2024/12/asav-topology.png">}}

[^D2]: I have no idea how it got that extra twist on the right-hand side.

And this is how I would describe that topology in a [_netlab_ topology file](https://github.com/ipspace/netlab-examples/blob/master/multi-platform/asav/topology.yml):

{{<printout>}}
message: >
  This topology contains a simple ASAv deployment scenario. ASAv is a WAN
  edge firewall. The wan edge router router is advertising the default BGP route
  that ASAv should propagate to the inside routers.

module: [ bgp ]
plugin: [ bgp.session ]

groups:
  _auto_create: True
  routers:
    members: [ ext, int ]
    device: frr
    provider: clab
  hosts:
    members: [ h1, h2, x ]
    provider: clab
    device: linux

nodes:
  fw:
    device: asav
    bgp.as: 65000
  int:
    bgp.as: 65001
  ext:
    bgp.as: 65100

links:
- h1-h2-int
- int-fw
- fw:
  ext:
    bgp.default_originate: True
- ext:
    bgp.advertise: False
  x:
{{</printout>}}

The basics:

* The lab is using BGP routing (line 6)
* We want the external router to advertise a default route, so we need the [**bgp.session** plugin](https://netlab.tools/plugins/bgp.session/) (line 7)
* The lab has two routers. We're using FRR containers (lines 11-14). You can use whatever device that [supports BGP](https://netlab.tools/platforms/#supported-configuration-modules). The external router should also support [default route origination](https://netlab.tools/plugins/bgp.session/#platform-support).
* We're using Linux containers as hosts (lines 15-18).

{{<note info>}}If you don't want to use containers, remove the **provider: clab** setting from the **routers** and **hosts** groups. To use different routers or switches, change the **device: frr** setting (line 13).{{</note>}}

* Most nodes are created from the group members (line 10), but we still need to define the firewall (lines 21-23) and set BGP AS numbers for the internal (line 25) and external (line 27) routers.

Now for the fun part: the links.

* H1 and H2 are connected to the internal router (line 30)
* The internal router is connected to the firewall (line 31)
* The firewall is connected to the external router (lines 32-34). The external router is advertising the BGP default route (line 34).
* The external host is connected to the external router (lines 35-37). The IP subnet of that link is not advertised in BGP (line 36) because we're using default routing.

Does it work? Sort of. Once you start the lab with **[netlab up](https://netlab.tools/netlab/up/)**  (after doing the mandatory *[some assembly required](https://netlab.tools/labs/asav/)* stuff because vendors don't want to ship Vagrant boxes), ASAv propagates the default route to the internal router:

{{<cc>}}BGP routing table on the internal router{{</cc>}}
```
$ netlab connect int --show ip bgp
Connecting to container clab-asav-int, executing vtysh -c "show ip bgp"
BGP table version is 4, local router ID is 10.0.0.2, vrf id 0
Default local pref 100, local AS 65001
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

    Network          Next Hop            Metric LocPrf Weight Path
 *> 0.0.0.0/0        172.16.1.1                             0 65000 65100 i
 *> 10.0.0.2/32      0.0.0.0(int)             0         32768 i
 *> 10.0.0.3/32      172.16.1.1                             0 65000 65100 i
 *> 172.16.0.0/24    0.0.0.0(int)             0         32768 i

Displayed 4 routes and 4 total paths
```

The internal subnet is also propagated to the external router:

{{<cc>}}BGP routing table on the external router{{</cc>}}
```
$ netlab connect ext --show ip bgp
Connecting to container clab-asav-ext, executing vtysh -c "show ip bgp"
BGP table version is 3, local router ID is 10.0.0.3, vrf id 0
Default local pref 100, local AS 65100
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

    Network          Next Hop            Metric LocPrf Weight Path
 *> 10.0.0.2/32      172.16.2.1                             0 65000 65001 i
 *> 10.0.0.3/32      0.0.0.0(ext)             0         32768 i
 *> 172.16.0.0/24    172.16.2.1                             0 65000 65001 i

Displayed 3 routes and 3 total paths
```

However, you cannot yet ping **x** from **h1**. The [initial device configurations](https://github.com/ipspace/netlab-examples/tree/master/multi-platform/asav/config) generated by **netlab up** do not include any firewall-related ASAv configuration.

I never had to work with ASAv, and I have no plans to change that. The minimal config enabling ICMP and TCP from **h1** to **x** would be most appreciated.

### Off-Topic: The Beauties of the Ancient SSH Implementations

My ASAv still uses the long-obsolete SSH cryptographic mechanisms, so I could not connect to it with **netlab connect fw** to configure it. Interestingly, **vagrant ssh fw** worked for me for whatever reason.

You might have to change the `~/.ssh/config` file to allow SSH to use older key exchange and encryption algorithms. If you use the _netlab_ release 1.9.2 you could also try setting **defaults.devices.asav.group_vars.netlab_ssh_args** to `-o KexAlgorithms=+diffie-hellman-group14-sha1 -o PubkeyAcceptedKeyTypes=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa` in the lab topology file. The permanent fix is coming in netlab release 1.9.3.


