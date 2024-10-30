---
title: "EVPN Designs: EVPN EBGP over IPv4 EBGP"
series_title: "EVPN EBGP over IPv4 EBGP"
date: 2024-10-29 08:12:00+0200
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In the previous blog posts, we explored three fundamental EVPN designs: [we don't need EVPN](/2024/04/evpn-designs-vxlan-leaf-spine-fabric/), [IBGP EVPN AF over IGP-advertised loopbacks](/2024/09/evpn-designs-ibgp-rr/) (the way EVPN was designed to be used) and [EBGP-only EVPN](/2024/10/evpn-designs-ebgp/) (running the EVPN AF in parallel with the IPv4 AF).

Now we're entering Wonderland: the somewhat unusual[^MH] things vendors do to make their existing stuff work while also pretending to look cool[^MR]. We'll start with EBGP-over-EBGP, and to understand why someone would want to do something like that, we have to go back to the basics.
<!--more-->
[^MH]: That sounds better than _Mad Hatter_, right?
[^MR]: In the mirror and the True Fans in the audience

This is how EVPN was designed to be used:

* IGP sessions are established on physical interfaces.
* IGP exchanges loopback IP addresses.
* IBGP sessions are established between loopback IP addresses.

{{<figure src="/2024/10/evpn-design-ibgp.png" caption="Oversimplified IBGP-over-IGP design">}}

This is how the vendors that decided to go all-in with EBGP-only data centers implemented EVPN:

* EBGP sessions are established on physical interfaces.
* IPv4 and EVPN address families are activated on those EBGP sessions.

{{<figure src="/2024/10/evpn-design-ebgp.png" caption="Oversimplified EBGP-only design">}}

And this is how some vendors think you should implement your EBGP-only data center:

{{<figure src="/2024/10/evpn-design-ebgp-over-ebgp.png" caption="Oversimplified EBGP-only design">}}

Why would anyone want to recommend something like that? I have two words for you: Route Churn.

### IBGP-based EVPN Has No Core-Generated Route Churn

The way EVPN was envisioned to work kept the IBGP EVPN sessions stable. Whatever happened to the links in your network, as long as there was a single path between the IBGP peers, the IBGP session was up, and the only routing updates generated by EVPN were the ones triggered by topology or endpoint changes at the network edges.

Route reflector failures are a different story. Unless you implemented [non-stop routing](https://blog.ipspace.net/2021/11/non-stop-routing/) on the route reflector, you'd lose the IBGP sessions, and it would take a while to get them back and exchange the EVPN routes. However, if you can make a sandwich[^TCM] while your data center switch is booting, the EVPN update processing speed is the least of your concerns.

[^TCM]: Or, in some cases, a three-course meal

Finally, when an edge node fails, all bets are off, and you better have a high-availability mechanism in place anyway.

### EBGP-only EVPN Route Churn After a Core Failure

All of those goodies are gone with the EBGP-only design. The EBGP session is gone the moment the underlying link goes down, and once the connectivity is reestablished, you have to exchange all EVPN routes (and there might be tens of thousands of them). Even worse, the spine switch has revoked the leaf routes in the meantime and is now busily readvertising them to the other leaf switches.

It's worth noting that the heavy lifting described in the previous paragraph is a control-plane-only activity. There has been no change in the end-to-end reachability, but the EVPN routes temporarily had one less alternate path while *all other attributes were unchanged*, and the CPUs were busy. 

### Fixing the Route Churn with EBGP-over-EBGP

Now imagine that your Product Manager rushes into the room yelling, "_We MUST have EVPN over EBGP. The competitors are looking cooler than we are and are beating us_." At the same time, you know your EVPN implementation does not perform well when faced with an onslaught of tens of thousands of updates. What do you do? You tell the PM that he better spin a great story about why EVPN AF on an EBGP session between loopbacks advertised by a regular EBGP session makes perfect sense. I've seen some of those arguments parroted in blog comments, and they did not make a lot of sense apart from the underlying "_this is how we minimize route churn_" part, but then you might as well [admit you have an implementation issue](https://blog.ipspace.net/2019/04/dont-sugarcoat-challenges-you-have/) and move on.

Oh, and you still have to deal with [all the drawbacks of the EBGP-only EVPN design](/2024/10/evpn-designs-ebgp/#evpn-considerations).

At this point, it might be worth comparing the (FRRouting) configuration needed to make this work[^FRPV] with the [one we need for the EBGP-only design](/2024/10/evpn-designs-ebgp/#bds) (just in case someone tells you how this is less complex):

{{<cc>}}FRRouting configuration implementing EBGP-over-EBGP design{{</cc>}}
```
router bgp 65001
 bgp router-id 10.0.0.1
 no bgp default ipv4-unicast
 bgp bestpath as-path multipath-relax
 neighbor eth1 interface remote-as 65100
 neighbor eth1 description S1
 neighbor eth2 interface remote-as 65100
 neighbor eth2 description S2
 neighbor 10.0.0.5 remote-as 65100
 neighbor 10.0.0.5 description S1
 neighbor 10.0.0.5 ebgp-multihop
 neighbor 10.0.0.5 update-source lo
 neighbor 10.0.0.6 remote-as 65100
 neighbor 10.0.0.6 description S2
 neighbor 10.0.0.6 ebgp-multihop
 neighbor 10.0.0.6 update-source lo
 !
 address-family ipv4 unicast
  network 10.0.0.1/32
  neighbor eth1 activate
  neighbor eth2 activate
  maximum-paths 8
 exit-address-family
 !
 address-family l2vpn evpn
  neighbor 10.0.0.5 activate
  neighbor 10.0.0.5 soft-reconfiguration inbound
  neighbor 10.0.0.6 activate
  neighbor 10.0.0.6 soft-reconfiguration inbound
  advertise-all-vni
  vni 101000
   rd 10.0.0.1:1000
   route-target import 65000:1000
   route-target export 65000:1000
  exit-vni
  advertise-svi-ip
  advertise ipv4 unicast
 exit-address-family
exit
!
```

[^FRPV]: I'm using FRRouting to ensure nobody accuses me of picking on any specific vendor.

The final nail in this coffin: unless you advertise the loopbacks across all potential paths (violating the [valley-free routing principle](/2018/09/valley-free-routing-in-data-center/) and losing the only advantage EBGP might have over an IGP like OSPF), you won't be able to exchange updates over the EVPN EBGP session (because the EBGP peer is not reachable). The EBGP session will stay up (unless you run BFD between loopbacks), but the information will be stale, potentially leading to highly stimulating forwarding challenges. EVPN route type 2 (MAC+IP) updates should do just fine because they were designed to deal with MAC mobility, but you might have an issue with EVPN route type 5 (IP prefix) updates[^DLER].

[^DLER]: The details are left as an exercise for the reader.

I've seen a vendor "recommended design" solving this problem with different AS numbers on the spine switches. They got EBGP sessions between loopbacks to work correctly but also turned EBGP into a more complex version of RIP, with the EBGP sessions running between loopbacks being a more complex version of IBGP. But hey, they were as cool as Microsoft!

### Leaf-and-Spine EBGP-Everywhere Lab Topology

Want to test this design in a lab? This is the [_netlab_ lab topology description](https://github.com/ipspace/netlab-examples/blob/master/EVPN/ebgp-ebgp/topology.yml) we'll use to set it up.

{{<printout>}}
defaults.device: eos
provider: clab

plugin: [ ebgp.multihop ]

addressing.p2p.ipv4: True
evpn.as: 65000
evpn.session: [ ]                               # Do not activate EVPN AF on any BGP session
bgp.multihop.activate.ipv4: [ evpn ]            # ... apart from the multihop sessions
bgp.community.ebgp: [ standard, extended ]      # Propagate extended community over EBGP
bgp.sessions.ipv4: [ ebgp ]                     # ... and activate IPv4 AF only on EBGP sessions

bgp.multihop.sessions:                          # Add loopback-to-loopback EBGP multihop sessions
- L1-S1
- L1-S2
- L2-S1
- L2-S2
- L3-S1
- L3-S2
- L4-S1
- L4-S2

fabric:
  spines: 2
  leafs: 4
  spine.bgp.as: 65100
  leaf.bgp.as: '{ 65000 + count }'

groups:
  _auto_create: True
  leafs:
    module: [ bgp, vlan, vxlan, evpn ]
  spines:
    module: [ bgp, evpn ]
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

We had to make these changes to the [EBGP everywhere topology](/2024/10/evpn-designs-ebgp/#lab) to make it work:

* The EBGP sessions between loopbacks are multihop, so we need the **[ebgp.multihop](https://netlab.tools/plugins/ebgp.multihop/)** plugin (line 4)
* We do not want to run EVPN on any regular BGP session (line 8) but only on multihop EBGP sessions (like 9)
* Finally, we have to build the multihop sessions (lines 13-21)

Assuming you already set up the lab infrastructure, you can start the lab with the **netlab up** command. You can also [start the lab in a GitHub Codespace](/2024/07/netlab-examples-codespaces/) (the directory is `EVPN/ebgp-ebgp`); you'll still have to [import the Arista cEOS container](/2024/07/arista-eos-codespaces/), though.

### Does It Work?

Of course, it does. Is it worth it? No.

I understand that some people love trying out EBGP as a better IGP, but if your vendor tells you to run EVPN AF over an EBGP session between loopback interfaces, it's time to change your vendor or your design (and go for IBGP-over-IGP).

{{<next-in-series page="/posts/2024/11/evpn-designs-ibgp-ebgp.md" />}}