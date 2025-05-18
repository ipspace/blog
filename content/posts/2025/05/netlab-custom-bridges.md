---
title: "netlab 2.0: Use Custom Bridges on Multi-Access Links"
series_title: "Use Custom Bridges on Multi-Access Links"
date: 2025-05-20 08:17:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
_netlab_ uses [point-to-point links provided by the underlying virtualization software](/2025/02/virtual-labs-p2p-links/) to implement links with two nodes and [Linux bridges to implement links with more than two nodes connected to them](/2025/02/virtual-lab-links/). That's usually OK if you don't care about the bridge implementation details, but what if you'd like to use a bridge (or a layer-2 switch if you happen to be of marketing persuasion) you're familiar with?

You could always implement a bridged segment with a set of links connecting edge nodes to a VLAN-capable device. For example, you could use the following topology to connect two Linux hosts through a bridge running Arista EOS:
<!--more-->
{{<printout>}}
defaults:
  device: linux
  provider: clab

vlans:
  hosts:
    mode: bridge

nodes:
  h1:
  h2:
  mybridge:
    device: eos
    module: [ vlan ]

links:
- interfaces: [h1, mybridge]
  vlan.access: hosts
- interfaces: [h2, mybridge]
  vlan.access: hosts
{{</printout>}}

**Notes:**

* The **mybridge** device is running Arista EOS (line 13) using VLANs (line 14)
* We have to define a VLAN we'll use to connect the hosts (lines 5-6) and put it into **mybridge** mode (line 7) to ensure the bridge device does not get an IP address on the VLAN interface.
* Finally, we have to define two VLAN access links connecting H1 and H2 to the bridge (lines 17-20)

Wouldn't it be better if we could just tell _netlab_ to use an Arista EOS node as a bridge to implement a link? That's precisely what you can do with [*bridge* nodes](https://netlab.tools/node-roles/#node-role-bridge) in [netlab release 2.0](https://netlab.tools/release/2.0/).

Here's a quick summary of what you have to do:

* Define the node you want to use as a bridge and set its **role** to **bridge**. You don't have to set any other parameter on that node (apart from specifying the **device** type you want to use)
* Use the bridge node in the **bridge** link attribute.
* You can use the same bridge node to implement multiple links. Each link will be implemented with a separate isolated VLAN.

Using a **bridge** node, the above topology becomes significantly simpler:

{{<printout>}}
defaults:
  device: linux
  provider: clab

nodes:
  h1:
  h2:
  mybridge:
    device: eos
    role: bridge

links:
- interfaces: [h1, h2]
  bridge: mybridge
{{</printout>}}

**Notes:**

* The **mybridge** device is used as a custom bridge (line 10). You don't have to specify that it's using the **vlan** module, and you no longer have to define the VLAN connecting H1 and H2
* You have to define a single link connecting H1 with H2 (line 13) and specify that the link is using a custom bridge (line 14).

After starting the lab (and waiting for 30 seconds for STP to figure out what to do), H1 can ping H2.

Finally, this is the Arista EOS configuration _netlab_ generated to implement the custom bridge:

```text
spanning-tree mode mstp
!
vlan 1
   name br_default
!
vlan 100
   name br_vlan_100
!
interface Ethernet1
   description [Access VLAN br_vlan_100] mybridge -> h1
   mac-address 52:dc:ca:fe:03:01
   switchport access vlan 100
!
interface Ethernet2
   description [Access VLAN br_vlan_100] mybridge -> h2
   mac-address 52:dc:ca:fe:03:02
   switchport access vlan 100
!
interface Management0
   vrf management
   ip address 192.168.121.103/24
   no lldp transmit
   no lldp receive
!
interface Vlan100
   description VLAN br_vlan_100 (100) -> [h1,h2] [stub]
!
no ip routing
```

**Notes:**

* A **bridge** node does not have a loopback interface and does not perform IP forwarding.
* A separate VLAN is created for each multi-access link implemented with a bridge node. _netlab_ created VLAN 100 to connect H1 with H2
* Links to edge nodes are implemented as VLAN access links.
* There is no IP address on the VLAN interface. A **bridge** node is a transparent bridge.
