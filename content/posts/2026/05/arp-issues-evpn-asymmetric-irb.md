---
title: "ARP with EVPN Asymmetric IRB"
subtitle: "TL&DR: With the right nerd knob settings, it all works"
date: 2026-05-14 07:45:00+0200
tags: [ evpn ]
evpn_tag: details
---
In a [previous blog post](/2026/05/arp-issues-evpn-central-routing/), I described the ARP issues you'll encounter when using centralized routing (on a spine switch) between two EVPN MAC-VRF instances (a fancy name for a VLAN encapsulated in VXLAN or MPLS).

That blog post established a baseline that will help us unravel the ARP behavior in a more realistic scenario: asymmetric Integrated Routing and Bridging (IRB). That's a mouthful, but it's really quite a simple concept; the following diagram explains the _asymmetric_ forwarding behavior:

{{<figure src="/2026/05/evpn-fwd-asymmetric-irb.png" caption="Packet forwarding in an EVPN asymmetric IRB design">}}
<!--more-->

* Every PE device has an IP address in every VLAN (EVPN MAC-VRF instance)
* Today, we'll ignore fanboys yelling "*ANYCAST GATEWAY*" (we'll get there) and assume the PE devices have different IP addresses.
* Every host uses the closest PE device as its first-hop gateway.

{{<note>}}
If a host uses a remote PE device as the first-hop gateway, we're dealing with a lopsided variant of *[centralized routing](/2026/05/arp-issues-evpn-central-routing/)*; the proof is left as an exercise for the reader.
{{</note>}}

In our small topology, HB1 uses *Blue.1*[^B1] as the default gateway, and HR1 uses *Red.2*.

[^B1]: First IP address in the *Blue* prefix

Here's how HB1 sends the first packet to HR1:

* HB1 sends an ARP request for its default gateway. When L1 receives the ARP request, it REALLY SHOULD generate a MAC+IP route for HB1 (if this sounds like Latin, you REALLY SHOULD read the [previous blog post](/2026/05/arp-issues-evpn-central-routing/))
* HB1 sends the packet for HR1 to L1.
* If we're lucky, L1 already has an entry for HR1 in its ARP cache and can just forward the packet.
* Otherwise, L1 has to send an ARP request *over VXLAN* into the red VLAN, opening the can of worms we copiously investigated in the *[centralized routing](/2026/05/arp-issues-evpn-central-routing/)* blog post[^M3].

[^M3]: Did you notice I mentioned that blog post four times already? Take the hint if you haven't read it yet.

We'd all love to be lucky, right? Here are the mandatory prerequisites for reaching eternal bliss in this particular design:

* PE device MUST create ARP entries from MAC+IP routes[^MCA] 
* End-hosts MUST NOT be silent and MUST send an ARP request for the first-hop gateway early in their lifetime[^SS]. That's usually the case unless you're dealing with minimalistic containers running something like *syslog* servers.

[^MCA]: We're obviously in deep trouble if they're ignoring *those* hints, aren't we?

[^SS]: Silent hosts? You're clearly out of your daily allowance of luck.

### Do EVPN Implementations Work This Way?

Is that how EVPN devices work with their default settings? You can [try it out](#try) with [this netlab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/asymmetric-irb/topology.yml):

* Start the lab with your favorite devices (use `-d something` **[netlab up](https://netlab.tools/netlab/up/)** parameter).
* Ping L1 from HB1. Inspect the ARP cache in the *tenant* VRF on L1. It should include an entry for HB1 (172.16.1.4)[^addr]

```
l1#show arp vrf tenant
Legend:
 not learned: Associated MAC address is not present in the MAC address table
 -: Static (configuration or programmed by feature)
Address         Age (sec)  Hardware Addr   Interface
172.16.0.2        0:20:45  001c.7393.0e6a  Vlan1000, not learned
172.16.1.2        0:20:45  001c.7393.0e6a  Vlan1001, not learned
172.16.1.4        0:00:08  aac1.ab5c.859a  Vlan1001, Ethernet2
```

[^addr]: Hint: use **netlab report addressing** to display IP addresses used in the lab

* Inspect type-2 EVPN routes on L2. There should be a route for IP address 172.16.1.4:

```
l2#show bgp evpn route-type mac-ip 172.16.1.4 detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for mac-ip aac1.ab5c.859a 172.16.1.4, Route Distinguisher: 10.0.0.1:1001
 Paths: 1 available
  Local
    10.0.0.1 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1001 TunnelEncap:tunnelTypeVxlan
      VNI: 101001 ESI: 0000:0000:0000:0000:0000
```

* Check the ARP table for the tenant VRF on L2. It should include an entry for 172.16.1.4. The lack of age field on Arista EOS means 'we got this from EVPN':

```
l2#show arp vrf tenant
Legend:
 not learned: Associated MAC address is not present in the MAC address table
 -: Static (configuration or programmed by feature)
Address         Age (sec)  Hardware Addr   Interface
172.16.0.1        0:24:27  001c.7321.8ca9  Vlan1000, not learned
172.16.1.1        0:24:27  001c.7321.8ca9  Vlan1001, not learned
172.16.1.4              -  aac1.ab5c.859a  Vlan1001, Vxlan1
```

* Finally, Arista EOS includes a convenient **show bgp evpn arp** command:[^TSR]

```
l2#show bgp evpn arp
VLAN  Label  Encap IP                 MAC             Tunnel Endpoint    Seq#
----- ------ ----- ------------------ --------------- ------------------ ------
1001  101001 VXLAN 172.16.1.4         aac1.ab5c.859a  10.0.0.1           -
```

[^TSR]: But it's more fun to take the scenic route, right?

{{<note>}}
I noticed some absurd behavior when testing FRRouting -- being an old-timer, I used **arp** to display neighbor entries, and the remote IP addresses did not appear, BUT they were included in the **ip neigh** output. A comment explaining this mystery would be highly appreciated.
{{</note>}}

### Try It Out {#try}

The [lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/asymmetric-irb/topology.yml) I used in this blog post is in the [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/EVPN/central-routing). If you want to try it out:

* [Set up your lab environment](https://blog.ipspace.net/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab) (you can use free GitHub Codespaces)
* Change directory to `EVPN/asymmetric-irb`
* Execute **netlab up** and explore
