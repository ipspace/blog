---
title: "Tagged VLAN 1 In a Trunk Is a Really Bad Idea"
date: 2025-02-11 08:05:00+0100
tags: [ bridging, LAN ]
---
It all started with a [netlab](https://github.com/ipspace/netlab) issue describing [different interpretations of VLAN 1 in a trunk](https://github.com/ipspace/netlab/issues/1876). While  Cumulus NVUE (the way the [_netlab_ configuration template](https://github.com/ipspace/netlab/blob/dev/netsim/ansible/templates/vlan/cumulus_nvue.j2) configures it) assumes that the VLAN 1 in a trunk is tagged, Arista EOS assumes it's the native VLAN.

At that point, I should have said, "_that's crazy, we shouldn't allow that_" and enforce the "_VLAN 1 has to be used as a native VLAN_" rule. Alas, 20/20 hindsight never helped anyone.

**TL&DR:** Do not use VLAN 1 in VLAN trunks; if you have to, use it as a native VLAN.
<!--more-->
### A Bit of a History

Let's try to figure out what quirks of ancient history[^AH] brought us to the current quagmire before going into the weird stuff I encountered while trying to implement the tagged VLAN 1 idea:

[^AH]: Based on my vague personal recollections. Most of the stuff from the early 1990s has been lost, and contrary to IETF, IEEE never wanted to expose how the sausage was being made. Please let me know if you have better sources, and I'll update the blog post.

* Cisco (or one of its acquisitions) got a great idea that one could [add an extra Ethernet header](https://en.wikipedia.org/wiki/Cisco_Inter-Switch_Link) to run multiple bridging domains across the same physical links. The VLANs were born ([more details by Daniel Dib](https://lostintransit.se/2024/07/18/some-history-on-vlan-1-in-cisco-switches))
* It was evident that one had to support tagged and untagged packets on the same 802.1Q link. If nothing else, the [layer-2 control-plane protocols had to use untagged packets](https://blog.ipspace.net/2025/01/ethernet-8021-protocol-stack/) ([more details by Daniel Dib](https://lostintransit.se/2024/07/08/why-do-we-have-native-vlans/)).
* Assigning a fake VLAN to untagged packets makes forwarding hardware simpler -- you can use the same VLAN MAC FIB to forward tagged and untagged packets.
* Assigning VLAN 0 to untagged packets would be an obvious choice, but IEEE decided to [use VLAN 0 as a fake VLAN when reusing 802.1q header](https://en.wikipedia.org/wiki/IEEE_802.1Q) for [802.1p priority bits](https://en.wikipedia.org/wiki/IEEE_P802.1p) on untagged packets.
* VLAN 1 thus became the *default VLAN* (as in: this is what we use for untagged packets).

However, as people started using VLANs on things that have to be auto-provisioned (servers, access switches), they discovered an interesting conundrum:[^PC]

[^PC]: Also known as "painting yourself into a corner and blaming technology" ;)

* The auto-provisioned devices have no idea they should use a VLAN trunk on their uplink before they are configured.
* DHCP requests are thus sent as untagged packets and would land in VLAN 1.
* Using the same VLAN 1 everywhere for auto-provisioning would trigger alerts during any semi-competent security audit, so we needed another solution.
* Vendors[^BEPO] quickly realised one could assign any VLAN tag to untagged packets and we got the functionality to use any VLAN as a native VLAN in a VLAN trunk. After all, an access VLAN port is nothing else but a trunk port with a single native VLAN.

[^BEPO]: When faced with a big-enough purchase order and a clear threat that "_the competition is already doing that_"

Anyway, while it's perfectly OK not to allow VLAN 1 on a VLAN trunk, most (sane) people developing network operating systems kept assuming that if one wants to use VLAN 1 in a trunk, it would be used as the native VLAN.

### A Maze of Tiny Rabbit Trails, All Alike

Back to 2025. Instead of posting the above paragraph in response to the above-mentioned GitHub issue and closing it, I decided to do the crazy thing and figure out which vendors could be persuaded to send and receive tagged packets in VLAN 1 on a VLAN trunk.

I created a [new integration test with three VLAN trunks](https://github.com/ipspace/netlab/blob/dev/tests/integration/vlan/70-vlan-1-trunk.yml):

1. Tagged VLAN 700 and VLAN 1 
2. Native VLAN 1 and tagged VLAN 700
3. Native VLAN 700 and tagged VLAN 1

Next, I [ran the test](https://tests.netlab.tools/_html/coverage.vlan) on most devices [supported by the _netlab_ VLAN configuration module](https://netlab.tools/module/vlan/). Some of them passed with flying colors; many needed configuration tweaks ranging from a single command to horrible things one should not do in a real-life network:

* [Aruba CX](https://github.com/ipspace/netlab/commit/35d07d4d44dc20072938f2ca9bd7ac1c9a54af1e) and [Arista EOS](https://github.com/ipspace/netlab/commit/12f7487cf17530d9f97958a573aa2cc17913869a) needed a configuration command saying, "_we want to tag native VLAN packets._" Yeah, I know that sounds like a square circle, but that's the device CLI for you.
* There is no such command on Cisco IOS[^TNG] or Nexus OS, but I could make VLAN 1 tagged by configuring a fake VLAN as a native VLAN. I [used VLAN 1002 on Cisco IOS layer-2 images](https://github.com/ipspace/netlab/commit/a6fdc6e6d839fbb50745399de4f6a27bb1a8e02e) and the [highest available VLAN on Nexus OS](https://github.com/ipspace/netlab/commit/154f7da4a512a8abf18bb0f3b27fbc0dea950f3b). For more Cisco IOS details, read [Encapsulation of PDUs On Trunk Ports](https://lostintransit.se/2024/07/16/encapsulation-of-pdus-on-trunk-ports/) by Daniel Dib.
* Cisco IOSv uses subinterfaces to implement bridging, and there's no way to say, "_this subinterface uses tagged VLAN 1_". The **encapsulation dot1q 1** command always gets the **native** keyword attached to it.
* I had to change the VyOS configuration template to [configure VLAN 1 directly on the built-in bridge interface](https://github.com/ipspace/netlab/commit/96a55ceb34126219926fe6a364ef9f06af2f276e) (all other VLANs are configured on **vif** subinterfaces of **br0**)
* Junos switches worked like a charm, but our router configuration template uses [fake VLAN 1 configuration on unit 0](https://github.com/ipspace/netlab/blob/dev/netsim/ansible/templates/initial/junos.vlan.j2#L53). We could change that to _use another fake VLAN_, but I would love a cleaner approach[^FFSP].
* Dell OS10 uses VLAN 1 as an internal VLAN, and flat-out refuses to use it in a VLAN trunk unless you [change the internal VLAN to something else](https://github.com/ipspace/netlab/pull/1911).

[^TNG]: The **vlan dot1q tag native** is a global command and applies to all VLAN trunk ports.

[^FFSP]: Feel free to submit a pull request ;)

**To recap:** Do not use tagged VLAN 1 in VLAN trunks. Just because you could does not mean that you should.