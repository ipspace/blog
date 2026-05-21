---
title: "SR Linux MPLS/VPN Configuration Notes"
date: 2026-05-27 07:57:00+0200
tags: [ MPLS VPN ]
---
After fixing the SR Linux LDP configuration template, I decided to add MPLS/VPN to the _netlab_ SR Linux MPLS features. After all, the [one-page recipe](https://documentation.nokia.com/srlinux/26-3/books/vpn-services/ip-vpn-services.html#configuring-ip-vpn-services) seemed simple enough, more so as we already have tested VRF and EVPN templates.

Alas, nothing is as simple as it looks. There were two details that tripped me pretty badly.
<!--more-->
### BGP Address Families

SR Linux configures BGP address families in two places: within the BGP protocol and within individual BGP neighbors. I should have just copied the documentation recipe, but of course, I didn't. _netlab_ SR Linux BGP configuration already has per-neighbor BGP address families, so I just activated `l3vpn-ipv4-unicast` AF within all IBGP neighbors, and the weirdest thing happened:

* The L3VPN address family was negotiated on the IBGP sessions.
* The BGP neighbor sent its routes over the L3VPN address family, and SR Linux silently[^ON] ignored them.
* When I was inspecting the L3VPN IPv4 unicast routes, I could see none, but there was also no error message.

[^ON]: Or not, maybe it was screaming into a log file I haven't found yet.

{{<printout caption="L3VPN routes on SR Linux (or lack of them)">}}
A:admin@dut# show protocols bgp routes l3vpn-ipv4-unicast summary
------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "default"
------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale, b=backup, w=unused-weight-only
Origin codes: i=IGP, e=EGP, ?=incomplete
------------------------------------------------------------------------------------------------------------------------------------
+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|     Status      |      Route      |     Network     |    Next Hop     |       MED       |     LocPref     |    Path Val     |
|                 |  Distinguisher  |                 |                 |                 |                 |                 |
+=================+=================+=================+=================+=================+=================+=================+
+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+-----------------+
------------------------------------------------------------------------------------------------------------------------------------
0 received BGP routes: 0 used, 0 valid, 0 stale
0 available destinations: 0 with ECMP multipaths
------------------------------------------------------------------------------------------------------------------------------------
{{</printout>}}

After adding the L3VPN IPv4 unicast address family and configuring **keep-all-routes**, I could see the routes advertised by the BGP peer, but they were still not used. Detailed printouts told me the routes were *rejected*:

{{<printout caption="Details of a single L3VPN BGP route">}}
A:admin@dut# show protocols bgp routes l3vpn-ipv4-unicast prefix 172.16.1.0/24 detail
------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP routes to network "172.16.1.0/24" network-instance  "default"
------------------------------------------------------------------------------------------------------------------------------------
Route-distinguisher: 65000:1  Network: 172.16.1.0/24
Received Paths: 1
  Path 1: <>
    Route source      : neighbor 10.0.0.6
    Route Preference  : MED is -, LocalPref is 100
    BGP next-hop      : 10.0.0.6
    Path              :  i
    Domain Path       : None
    Communities       : target:65000:1
    RR Attributes     : No Originator-ID, Cluster-List is [ - ]
    Aggregation       : Not an aggregate route
    Unknown Attr      : None
    Invalid Reason    : Rejected_Route
    Tie Break Reason  : none
    Route Flap Damping: None
------------------------------------------------------------------------------------------------------------------------------------
{{</printout>}}

### It's the Labels, STUPID!

I wasted hours before figuring out I had to read the small print  in that IP-VPN SR Linux recipe:

> As a prerequisite, a label block must be configured using the system mpls services network-instance dynamic-label-block _name_ configuration.

The small print included a pointer to another document explaining how to configure the label block. I added the prerequisite label block, and all of a sudden, everything worked.

Here's the label block configuration _netlab_ uses. It sure would have been nice to have it included in the configuration recipe.

{{<printout caption="SR Linux MPLS/VPN label block configuration">}}
--{ + running }--[ system mpls ]--
A:admin@dut# info
    label-ranges {
        dynamic ldp {
            start-label 10000
            end-label 15000
        }
        dynamic vpn {
            start-label 20000
            end-label 30000
        }
    }
    services {
        network-instance {
            dynamic-label-block vpn
        }
    }
{{</printout>}}

It also turned out that the address-family configuration at the `protocols bgp` level was a red herring. All you have to configure to have a working MPLS/VPN network (assuming you have already configured VRF network instances and LDP) are the *services* label block and per-neighbor L3VPN address families. 

Alternatively, you could just configure the L3VPN address family at the `protocols bgp` level, and it would be activated for all BGP neighbors.

### A Note On Route Distinguishers and Route Targets

The SR Linux IP-VPN recipe I keep mentioning glosses over an important detail: if you don't set the route distinguisher and route targets in the `protocols bgp-vpn` configuration of a VRF network instance, the system uses EVPN auto-derived RD/RT values, which might not be the best solution for an MPLS/VPN network.

Here's how _netlab_ sets them when configuring SR Linux for the "connect subnets" [MPLS/VPN integration test](https://github.com/ipspace/netlab/blob/dev/tests/integration/mpls/10-vpn-connected.yml):

{{<printout caption="SR Linux VRF RD/RT configuration">}}
--{ + running }--[ network-instance t1 ]--
A:admin@dut# info protocols bgp-vpn
    bgp-instance 1 {
        route-distinguisher {
            rd 65000:1
        }
        route-target {
            export-rt target:65000:1
            import-rt target:65000:1
        }
    }
{{</printout>}}

{{<note warning>}}
I couldn't figure out how to set multiple import/export route targets for a network instance. For the moment, _netlab_ cannot configure more complex VPN architectures (for example, the _common services_ VPN) on SR Linux.
{{</note>}}

### Want to Kick the Tires?

The MPLS/VPN on SR Linux functionality will be part of the 26.06 release. It is already merged into the _netlab_ dev branch, so you can check it out from a [local copy of the _netlab_ repository](https://netlab.tools/install/clone/).

To make MPLS/VPN work on SR Linux, you'll have to set the **clab.type** node attribute to `ixr-6e` or similar ([details](https://netlab.tools/caveats/#nokia-sr-linux)), or change the **defaults.devices.srlinux.clab.node.type** [default setting](https://netlab.tools/defaults/). You'll also need a license file; its location can be specified in the **clab.license** node attribute or **defaults.devices.srlinux.clab.node.license** default setting.
