---
title: "Configuring SRv6 Layer-3 Services on Junos"
date: 2026-10-14 08:15:00+0200
tags: [ SRv6 ]
srv6_tag: config
---
Now that we know what we need to make layer-3 services ([BGP-free core](/2012/01/bgp-free-service-provider-core-in/) transporting IPv4 and IPv6 traffic) [work with SRv6](/2026/10/srv6-bgp-free-core/), let's go through the steps needed to configure them on Junos, continuing from the [baseline SRv6 with IS-IS configuration](/2026/09/srv6-junos/) (and again relying on the excellent SRv6 Micro-SID (uSID) Basics article[^GF] by [Krzysztof Szarkowicz](https://www.ipspace.net/Author:Krzysztof_Grzegorz_Szarkowicz)).

In the [BGP-Free Network Core with SRv6](/2026/10/srv6-bgp-free-core/), we identified the components we need (assuming IBGP+IGP design):
<!--more-->
[^GF]: The last time I checked, HPE marketing decided to redirect all Juniper community pages to the generic New HPE Networking Community starting page (what could possibly go wrong, right?). If your GoogleFu is strong enough, you might still be able to find it.

* IPv6 routing tables with SRv6 locators (the [IS-IS + locator configuration](/2026/09/srv6-junos/) should give us that)
* IBGP sessions between IPv6 endpoints (out of scope, but you can find plenty of stuff on the Internet)
* [*extended nexthop* capability](/2022/01/bgp-af-nerd-knobs/) negotiated between IBGP neighbors
* The IPv4 address family, activated over the IPv6 transport session (this is where the fun starts)
* IPv4 routes using RFC 8950-style IPv6 next hops.
* SRv6 prefix SID attribute attached to IPv4/IPv6 BGP routes.

It's relatively easy to configure these nerd knobs on Junos.

Activating IPv4 address family on an IPv6 IBGP session is trivial[^PG]:

[^PG]: The **ibgp-peers-ipv6** peer group sets neighbor type to **internal**.

{{<printout caption="Activating IPv4 address family on an IPv6 IBGP session">}}
protocols {
  bgp {
    group ibgp-peers-ipv6 {
      neighbor 2001:db8:0:3::1 {
        family inet {
          unicast;
        }
      }
    }
  }
}
{{</printout>}}

However, we also have to enable *extended nexthop* capability (or the routes will get some useless IPv4 next hops), and while doing that, we should also tell the router to attach an SRv6 prefix SID to these routes and accept the SRv6 prefix SID attribute from the neighbor. Here's the full neighbor configuration:

{{<printout caption="Junos SRv6 IBGP neighbor configuration">}}
protocols {
  bgp {
    group ibgp-peers-ipv6 {
      neighbor 2001:db8:0:3::1 {
        family inet {
          unicast {
            extended-nexthop;
            advertise-srv6-service;
            accept-srv6-service;
          }
        }
      }
    }
  }
}
{{</printout>}}

Unfortunately, you can do all that, and it won't work. Junos expects you to tell the BGP process to allocate an IPv4 (or IPv6) End.DT4 SID. Why it can't figure that out based on the *I want to advertise SRv6 service* is beyond me, but that's how we roll 🤷🏻‍♂️ Here's the required config for IPv4 and IPv6 layer-3 services:

{{<printout caption="Junos BGP SRv6 SID configuration" highlight="sure">}}
protocols {
  bgp {
    source-packet-routing {
      srv6 {
        locator <i>your-srv6-locator</i> {
            micro-dt4-sid;
            micro-dt6-sid;
        }
      }
    }
  }
}
{{</printout>}}

That's all, right? Sort of. It works for the directly connected subnets, but not for the IPv4 routes received from a CE router. This is how a customer IPv4 BGP route looks when received by the remote PE router.

{{<printout caption="Useless IPv4 next hop on a BGP IPv4 route">}}
pe2# show bgp ipv4 192.168.0.3
BGP routing table entry for 192.168.0.3/32, version 9
Paths: (1 available, no best path)
  Not advertised to any peer
  65101
    10.1.0.1 (inaccessible, import-check enabled) from 2001:db8:0:1::1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, invalid, internal
      Last update: Mon Oct  5 15:41:31 2026
{{</printout>}}

Hint: advertising an IPv4 next hop over an IPv6-only network rarely results in a usable route.

Let's recap:

* The IPv4 address family is configured over IPv6 IBGP session.
* We explicitely configured *extended nexthop* and *SRv6 SIDs*
* And yet, Junos happily advertises IPv4 next hops for IPv4 routes 🤦‍♂️

If you're a long-time BGP user, you're probably screaming **NEXT-HOP SELF** by now. Unfortunately, that's not an option in Junos BGP neighbor configuration (or at least I haven't found it). A route map applied as an export policy does the trick:

{{<printout caption="Enforcing (local) IPv6 next hop on all IPv4 routes">}}
policy-statement next-hop-all-ipv4 {
    term next-hop-self-ipv4 {
        from family inet;
        then {
            next-hop self;
        }
    }
}
{{</printout>}}

{{<note>}}
Applying this route map on a route reflector is probably a bad idea. The proof is left as an exercise for the reader ;)
{{</note>}}

### Generating Junos Configurations with netlab

If you're looking for working (albeit probably not optimal) Junos SRv6 configurations, you can [generate them with netlab](https://blog.ipspace.net/2026/02/netlab-device-configs/):

* Install the [**networklab** Python package](https://blog.ipspace.net/2026/02/netlab-device-configs/) (or [full netlab environment](https://netlab.tools/install/))
* Find a suitable topology in the [SRv6 examples](https://github.com/ipspace/srv6-examples).
* Execute **netlab create -d _your_device_ _topo_url_** (in an empty directory), where _your_device_ is the netlab device type from [this table](https://netlab.tools/platforms/#supported-virtual-network-devices) (assuming netlab can [configure SRv6](https://netlab.tools/module/srv6/) on it), and the _topo_url_ is the GitHub URL of the lab topology, for example:

```
$ netlab create -d vjunos-switch https://github.com/ipspace/srv6-examples/blob/main/2-services/1-ipv4-islands/topology.yml
```

Presto: the device configuration files are in the **node_files** directory tree. Explore and enjoy ;)

There are a few extra steps if you want to use the topologies from the [SRv6 integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration/srv6):

* On the web page with the lab topology, click on the *download raw file* link next to the **raw** button.
* Open the downloaded YAML file and delete the **validate** section (it uses timeout constants that are defined in another directory)
* Execute **netlab up -d _your_device_ _topology_file_**

Obviously, it's much easier if you just clone the whole *netlab* repository with `git clone https://github.com/ipspace/netlab.git`
