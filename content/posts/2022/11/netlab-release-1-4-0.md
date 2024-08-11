---
date: 2022-11-07 07:41:00+00:00
netlab_tag: release
series_title: EVPN Asymmetric IRB, Anycast Gateways, VRRP (Release 1.4.0)
tags:
- netlab
title: 'netlab Release 1.4.0: EVPN Asymmetric IRB, Anycast Gateways, VRRP'
---
The big three features of the [*netlab* release 1.4.0](https://netlab.tools/release/1.4/) are:

-   [EVPN asymmetric IRB](https://netlab.tools/module/evpn/#asymmetric-irb) on Arista EOS, Cumulus Linux, Dell OS10, Nokia SR Linux, Nokia SR OS and VyOS
-   [Anycast gateway](https://netlab.tools/module/gateway/#anycast-gateway) on Arista EOS, Cumulus Linux, Nokia SR OS and Nokia SR Linux
-   [VRRP](https://netlab.tools/module/gateway/#virtual-router-redundancy-protocol-vrrp) on Arista EOS, Cisco IOSv/CSR, Cisco Nexus OS, Cumulus Linux and Nokia SR OS

We also added tons of new functionality, including:
<!--more-->
-   [EVPN MPLS transport](https://netlab.tools/module/evpn/#platform-support) (currently implemented on Arista EOS and Nokia SR Linux)
-   MPLS/LDP support on Nokia SR OS
-   New address allocation algorithm for links with small IPv4 prefixes
-   VLAN interfaces are [created for all VLANs listed in node **vlans** dictionary](https://netlab.tools/module/vlan/#create-vlan-interfaces-and-routed-subinterfaces) even when there’s no physical interface using a particular VLAN.
-   Routing protocols could be [disabled for the whole VRF](https://netlab.tools/module/routing/#disabling-a-routing-protocol-in-vrf)

We added a few nerd knobs for users who want to connect virtual lab devices with external devices (see [External Connectivity](https://netlab.tools/example/external/) for more details):

-   [**unmanaged** devices](https://netlab.tools/example/external/#unmanaged-devices) participate in data transformation process but are not part of virtual lab topology.
-   [Devices in **unprovisioned** group](https://netlab.tools/example/external/#unprovisioned-devices) are not configured during the **netlab initial** process.

It's easier to have a tight control on which VLANs and VRFs use VXLAN transport or EVPN control plane:

-   [Control allocation of VNI identifiers](https://netlab.tools/module/vxlan/#selecting-vxlan-enabled-vlans) with **vxlan.vlans** attribute
-   [Specify EVPN-enabled VLANs and VRFs](https://netlab.tools/module/evpn/#global-evpn-parameters) with **evpn.vlans** and **evpn.vrfs** lists
-   VLANs and VRFs mentioned in group **vlans**/**vrfs** dictionaries are [copied into all group members](https://netlab.tools/groups/#using-group-node-data-with-vrfs-and-vlans), resulting in VLAN interfaces and VRFs on all group members.

Finally, a few long-overdue items:

-   **node\_data** is deprecated – you can [specify node attributes directly in group data](https://netlab.tools/groups/#setting-node-data-in-groups).
-   Strict validation of topology, node, group, VLAN, VRF, and addressing attributes (see also [Breaking changes](https://netlab.tools/release/1.4/#breaking-changes))
-   ‘Device quirks’ framework deals with implementation limitations of individual virtual network devices

Upgrading is as easy as ever: execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

### Revision History

2024-08-10
: MPLS data plane works in cEOS release 4.32.1F and is supported in _netlab_ release 1.9.0. Removed a mention of MPLS on cEOS as a device quirk.

