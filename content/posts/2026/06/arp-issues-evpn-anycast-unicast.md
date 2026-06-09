---
title: "ARP with Anycast Gateways in EVPN Asymmetric IRB"
subtitle: "TL&DR: The deeper we dig, the curiouser it gets."
date: 2026-06-17 08:19:00+0200
tags: [ evpn ]
evpn_tag: details
---
In previous blog posts, I described the ARP issues in EVPN environments, starting with [centralized routing](/2026/05/arp-issues-evpn-central-routing/), and then [asymmetric IRB with unicast (per-leaf-switch) first-hop gateways](/2026/05/arp-issues-evpn-asymmetric-irb/). Of course, no self-respecting vendor would tell you to do that; anycast gateways are all the rage these days.

As always, anycast gateways could mean different things, depending on which vendor documentation you read ;)

1. Active-active VRRP (one device is the active VRRP gateway, but all devices listen to the VRRP MAC address).
2. Shared MAC+IP address beside device-specific unicast MAC and IP addresses.
3. Shared MAC+IP address with no PE-specific IP address.
<!--more-->
The only difference between (1) and (2) is the mechanism used to derive the shared MAC/IP address, either a control-plane protocol (VRRP) or static configuration.

The main difference between (1+2) and (3) is the number of IP addresses on each PE device's VLAN interfaces. In the first two cases, the PE device has a unique IP address and can communicate with the directly-connected devices. For example, it could run a routing protocol with them. In the last case, the shared IP address is primarily usable as a target for ARP queries (sometimes even pings don't work).

This blog post describes the second scenario:

{{<figure src="/2026/06/evpn-fwd-asymmetric-anycast.png" caption="Packet forwarding in an EVPN asymmetric IRB design with anycast gateways">}}

* Every PE device has an IP address (yellow box in the diagram) in every VLAN (EVPN MAC-VRF instance)
* PE devices have a shared MAC and IP address (red box in the diagram) in every VLAN.
* Every host uses the shared VLAN anycast gateway as its first-hop gateway.

{{<note important>}}
All PE devices listen to the shared MAC address. Packets with the shared MAC address as the destination MAC address are never forwarded over VXLAN; they are intercepted by the local PE device.
{{</note>}}

In our small topology, HB1 uses *Blue.1*[^B1] as the default gateway, and HR1 uses *Red.1*.

[^B1]: First IP address in the *Blue* prefix

### ARP Resolution on the Sender Side

Here's how HB1 sends the first packet to HR1:

* HB1 sends an ARP request for its default gateway (*Blue.1*). When L1 receives the ARP request, it replies with the shared MAC address.
* HB1 sends the packet for HR1 to L1.

The *sends the ARP request* part is already funky. The HB1 ARP request is sent as a broadcast packet, but I couldn't see it forwarded to the VXLAN segment. It looks like Arista EOS intercepts ARP broadcasts for local IP addresses (which makes sense, but is not what one might expect).

Some implementations (for example, Arista EOS) send gratuitous ARPs for the shared MAC/IP address every few seconds (Arista EOS default seems to be 30 seconds) to ensure the attached hosts use the correct MAC address. What happens after HB1 sends the ARP request is even more interesting:

### ARP Resolution on the Ingress Switch

HB1 sent the packet destined for HR1 to L1. Now, L1 has to do its job, and the first step is another address resolution -- it needs to know the MAC address of HR1.

If we're lucky, L1 populated its ARP cache from the EVPN MAC+IP routes and can just forward the packet to HR1. Otherwise, it has to send an *answerable* ARP request over VXLAN.

Some implementations mess up that part and send the ARP request *over VXLAN* from anycast MAC/IP address. There's just a tiny glitch there -- the response never comes back (remember that the switch closest to the host catches all the traffic sent to the shared anycast MAC address).

{{<note info>}}
Some devices can cope with that complication, but (as always) things work best in a single-vendor environment and might get interestingly complex when mixing vendors. More about that in another blog post.
{{</note>}}

The simplest way to make anycast gateways work *in this scenario* is thus to configure unicast IP addresses on PE devices. The PE devices MUST then use the unicast IP addresses for all control-plane communication (including ARP requests).

Final twist: the ARP response from the destination host is sent to the ingress PE device's MAC address. If the ingress PE device does not advertise its MAC address in an EVPN route, the ARP response will be flooded to all PE devices participating in the same MAC VRF instance (see the [asymmetric IRB](/2026/05/arp-issues-evpn-asymmetric-irb/) blog post for more details). Not necessarily a disaster, but definitely something to keep in mind.

### Try It Out {#try}

The [lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/asymmetric-anycast/topology.yml) I used in this blog post is in the [netlab-examples GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/EVPN/asymmetric-anycast). If you want to try it out:

* [Set up your lab environment](https://blog.ipspace.net/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab) (you can use free GitHub Codespaces)
* Change directory to `EVPN/asymmetric-anycast`
* Execute `netlab up`
* Execute `netlab config --limit pe add_anycast` to configure the anycast gateways.

{{<note>}}
While _netlab_ supports [anycast gateways](https://netlab.tools/module/gateway/#anycast-gateway), I wanted a solution that would configure scenarios (2) or (3) from the above list
{{</note>}}

