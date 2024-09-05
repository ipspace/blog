---
title: "EVPN Designs: Scaling IBGP with Route Reflectors"
series_title: "Scaling IBGP with Route Reflectors"
date: 2024-09-05 11:47:00+0200
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In the previous blog posts, we explored the [simplest possible IBGP-based EVPN design](/2024/05/evpn-designs-ibgp-full-mesh/) and tried to figure out whether [BGP route reflectors do more harm than good](/2024/05/bgp-rr-considered-harmful/). Ignoring that tiny detail for the moment, let's see how we could add route reflectors to our leaf-and-spine fabric.

As before, this is the fabric we're working with:
<!--more-->
{{<figure src="/2024/04/evpn-design-fabric.png" caption="Leaf-and-spine fabric with two VLANs">}}

As we're discussing an IBGP-based design:

* Leaf- and spine switches are running OSPF
* IBGP is used solely to transport EVPN address family.

The crucial question for today's discussion is where to place the route reflectors and whether we can use spine switches as route reflectors.

The CPU load on spine switches is usually pretty low (assuming they do packet forwarding in hardware), so they seem to be the perfect candidates for BGP route reflectors. There are just a few reasons why one wouldn't do that:
{#caveats}

* You bought spine switches that do IP forwarding but don't support EVPN.
* You didn't want to pay for the EVPN license on the spine switches.
* You bought leaf- and spine switches from different vendors and are worried about interoperability.
* Your network has so many endpoints that you're worried about the control-plane performance of spine switches[^SRB]
* The number of BGP neighbors (leaf switches) or the size of the EVPN BGP table exceeds the vendor-recommended limits.

[^SRB]: In which case, you should stop reading random blogs and focus on your network ;)

Adding route reflectors to an IBGP-based EVPN network is trivial:

* Configure IBGP sessions between every leaf switch and every spine switch.
* On the spine switches, configure all leaf switches to be route-reflector clients
* Don't forget to activate the EVPN address family on the IBGP sessions.

{{<note>}}It's also easy to *migrate* from an IBGP full mesh to a RR-based setup. The details are left as an exercise for the reader.{{</note>}}

Let's set up a lab and try it out. We'll use a lab setup similar to the [IBGP Full Mesh Between Leaf Switches](/2024/05/evpn-designs-ibgp-full-mesh/); read that blog post as well as the *[Creating the Lab Environment](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab)* section of the first blog post in this series to get more details.

### Leaf-and-Spine EVPN IBGP/RR Lab Topology

This is the [_netlab_ lab topology description](https://github.com/ipspace/netlab-examples/blob/master/EVPN/ibgp-rr/topology.yml) we'll use to set up the hub-and-spoke IBGP sessions using spine switches as route reflectors:

{{<printout>}}
defaults.device: eos
provider: clab

plugin: [ fabric ]
fabric.spines: 2
fabric.leafs: 4

bgp.as: 65000
bgp.activate.ipv4: []

groups:
  _auto_create: True
  leafs:
    module: [ ospf, bgp, vlan, vxlan, evpn ]
  spines:
    module: [ ospf, bgp, evpn ]
    bgp.rr: True
  hosts:
    members: [ H1, H2, H3, H4 ]
    device: linux

vlan.mode: bridge
vlans:
  orange:
    links: [ H1-L1, H2-L3 ]
  blue:
    links: [ H3-L2, H4-L4 ]

tools:
  graphite:
{{</printout>}}

Most of the topology file is explained in the previous blog posts ([basics](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#topo), [IBGP](/2024/05/evpn-designs-ibgp-full-mesh/#topo)); all we had to do to add route reflectors were two changes:

* Line 16: The spine switches are running OSPF, BGP, and EVPN
* Line 17: The spine switches are BGP route reflectors

Assuming you already did the previous homework, it's time to start the lab with the **netlab up** command. You can also [start the lab in a GitHub Codespace](/2024/07/netlab-examples-codespaces/) (the directory is `EVPN/ibgp-rr`); you'll still have to [import the Arista cEOS container](/2024/07/arista-eos-codespaces/), though.

### Behind the Scenes

This is the relevant part of the configuration of L1 running Arista EOS (you can view [complete configurations for all switches](https://github.com/ipspace/netlab-examples/tree/master/EVPN/ibgp-rr/config) on GitHub).

{{<printout>}}
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor 10.0.0.5 remote-as 65000
   neighbor 10.0.0.5 update-source Loopback0
   neighbor 10.0.0.5 description S1
   neighbor 10.0.0.5 send-community standard extended large
   neighbor 10.0.0.6 remote-as 65000
   neighbor 10.0.0.6 update-source Loopback0
   neighbor 10.0.0.6 description S2
   neighbor 10.0.0.6 send-community standard extended large
   !
   vlan 1000
      rd 10.0.0.1:1000
      route-target import 65000:1000
      route-target export 65000:1000
      redistribute learned
   !
   address-family evpn
      neighbor 10.0.0.5 activate
      neighbor 10.0.0.6 activate
{{</printout>}}

Let's walk through the changes:

* Lines 5-12: We must define the IBGP sessions with spine switches. There are no IBGP sessions between leaf switches.
* Lines 20-22: We must exchange EVPN routes with the spine switches. 

The spine switch configuration (S1) is very similar:

{{<printout>}}
router bgp 65000
   router-id 10.0.0.5
   no bgp default ipv4-unicast
   bgp cluster-id 10.0.0.5
   bgp advertise-inactive
   neighbor 10.0.0.1 remote-as 65000
   neighbor 10.0.0.1 update-source Loopback0
   neighbor 10.0.0.1 description L1
   neighbor 10.0.0.1 route-reflector-client
   neighbor 10.0.0.1 send-community standard extended large
   neighbor 10.0.0.2 remote-as 65000
   neighbor 10.0.0.2 update-source Loopback0
   neighbor 10.0.0.2 description L2
   neighbor 10.0.0.2 route-reflector-client
   neighbor 10.0.0.2 send-community standard extended large
   neighbor 10.0.0.3 remote-as 65000
   neighbor 10.0.0.3 update-source Loopback0
   neighbor 10.0.0.3 description L3
   neighbor 10.0.0.3 route-reflector-client
   neighbor 10.0.0.3 send-community standard extended large
   neighbor 10.0.0.4 remote-as 65000
   neighbor 10.0.0.4 update-source Loopback0
   neighbor 10.0.0.4 description L4
   neighbor 10.0.0.4 route-reflector-client
   neighbor 10.0.0.4 send-community standard extended large
   neighbor 10.0.0.6 remote-as 65000
   neighbor 10.0.0.6 update-source Loopback0
   neighbor 10.0.0.6 description S2
   neighbor 10.0.0.6 send-community standard extended large
   !
   address-family evpn
      neighbor 10.0.0.1 activate
      neighbor 10.0.0.2 activate
      neighbor 10.0.0.3 activate
      neighbor 10.0.0.4 activate
      neighbor 10.0.0.6 activate
{{</printout>}}

We had to:

* Configure IBGP sessions with all leaf switches and configure them as route-reflector clients (lines 6-25)
* (Optionally) configure a regular IBGP session with the other spine switch (lines 26-29)
* Activate the EVPN address family (but not IPv4 AF) on all IBGP sessions.

### Does It Work?

Of course, it does. Route reflectors don't change the attributes of the reflected routes. The EVPN updates sent from L1 to S1/S2 are forwarded almost intact[^CLA] to the other leaf switches.

[^CLA]: Apart from the insertion of the *originator* and *cluster-list* BGP attributes

The following printout shows L2's view of one of the EVPN routes advertised from L1. Note that we have two identical EVPN routes in the BGP table, reflected by S1 (10.0.0.5) and S2 (10.0.0.6).

```
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for mac-ip aac1.ab47.22a3, Route Distinguisher: 10.0.0.1:1000
 Paths: 2 available
  Local
    10.0.0.1 from 10.0.0.5 (10.0.0.5)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, ECMP head, ECMP, best, ECMP contributor
      Originator: 10.0.0.1, Cluster list: 10.0.0.5
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000 ESI: 0000:0000:0000:0000:0000
  Local
    10.0.0.1 from 10.0.0.6 (10.0.0.6)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, ECMP, ECMP contributor
      Originator: 10.0.0.1, Cluster list: 10.0.0.5
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000 ESI: 0000:0000:0000:0000:0000
```

### Was It Worth the Effort?

**TL&DR:** Absolutely (assuming you decided you want to have the EVPN control plane [no matter what](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/)).

Let's start with the **benefits**:

* It's easier to add new leaf switches. After adding a switch, you don't have to configure an additional IBGP session on every other leaf switch (assuming you decided *network automation* is not worth the effort).
* The network behavior is more consistent. A leaf switch either has information from other leaf switches or doesn't. Troubleshooting a misconfigured IBGP sessions in a full mesh of sessions is always great fun.
* You could use *passive neighbors* on spine switches to save 0.001% of the CPU cycles when a leaf switch is down.
* You could also use the *dynamic BGP neighbors* on the spine switches to establish IBGP sessions with new leaf switches without any configuration change (that's not [necessarily a good idea](https://bgplabs.net/session/9-dynamic/#impact-of-bgp-session-loss))

What about the **drawbacks**?

* We introduced BGP and EVPN to the spine switches. More complexity → more potential bugs → more frequent problems.
* You might experience spine (control-plane) performance problems in very large fabrics due to many BGP neighbors or a large EVPN BGP table.
* The leaf switches will get a copy of every EVPN route from every spine switch, increasing memory utilization.
* The spine switch configuration can become quite lengthy unless you're using peer groups, [policy templates](https://bgplabs.net/session/7-policy/), or [session templates](https://bgplabs.net/session/6-templates/).

Should you use route reflectors when building an EVPN-based leaf-and-spine fabric? I would. Should you deploy them on spine switches? Most probably, yes (but see the [caveats I already mentioned](#caveats)). Would you deploy them on all spine switches (assuming there are more than two)? It depends; it's a tradeoff between resilience and memory utilization.

{{<next-in-series page="/posts/2024/09/tbc.md" />}}