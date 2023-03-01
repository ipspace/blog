---
date: 2022-11-07 07:41:00+00:00
netlab_tag: release
series_title: EVPN Asymmetric IRB, Anycast Gateways, VRRP (Release 1.4.0)
tags:
- netlab
title: 'netlab Release 1.4.0: EVPN Asymmetric IRB, Anycast Gateways, VRRP'
---
The big three features of the [*netlab* release 1.4.0](https://netsim-tools.readthedocs.io/en/latest/release/1.4.html) are:

-   [EVPN asymmetric IRB](https://netsim-tools.readthedocs.io/en/latest/module/evpn.html#asymmetric-irb) on Arista EOS, Cumulus Linux, Dell OS10, Nokia SR Linux, Nokia SR OS and VyOS
-   [Anycast gateway](https://netsim-tools.readthedocs.io/en/latest/module/gateway.html#anycast-gateway) on Arista EOS, Cumulus Linux, Nokia SR OS and Nokia SR Linux
-   [VRRP](https://netsim-tools.readthedocs.io/en/latest/module/gateway.html#virtual-router-redundancy-protocol-vrrp) on Arista EOS, Cisco IOSv/CSR, Cisco Nexus OS, Cumulus Linux and Nokia SR OS

We also added tons of new functionality, including:
<!--more-->
-   [EVPN MPLS transport](https://netsim-tools.readthedocs.io/en/latest/module/evpn.html#platform-support) (currently implemented on Arista EOS and Nokia SR Linux)
-   MPLS/LDP support on Nokia SR OS
-   New address allocation algorithm for links with small IPv4 prefixes
-   VLAN interfaces are [created for all VLANs listed in node **vlans** dictionary](https://netsim-tools.readthedocs.io/en/latest/module/vlan.html#creating-vlan-interfaces-and-routed-subinterfaces) even when there’s no physical interface using a particular VLAN.
-   Routing protocols could be [disabled for the whole VRF](https://netsim-tools.readthedocs.io/en/latest/module/routing.html#disabling-a-routing-protocol-in-vrf)

We added a few nerd knobs for users who want to connect virtual lab devices with external devices (see [External Connectivity](https://netsim-tools.readthedocs.io/en/latest/example/external.html) for more details):

-   [**unmanaged** devices](https://netsim-tools.readthedocs.io/en/latest/example/external.html#unmanaged-devices) participate in data transformation process but are not part of virtual lab topology.
-   [Devices in **unprovisioned** group](https://netsim-tools.readthedocs.io/en/latest/example/external.html#unprovisioned-devices) are not configured during the **netlab initial** process.

It's easier to have a tight control on which VLANs and VRFs use VXLAN transport or EVPN control plane:

-   [Control allocation of VNI identifiers](https://netsim-tools.readthedocs.io/en/latest/module/vxlan.html#selecting-vxlan-enabled-vlans) with **vxlan.vlans** attribute
-   [Specify EVPN-enabled VLANs and VRFs](https://netsim-tools.readthedocs.io/en/latest/module/evpn.html#global-evpn-parameters) with **evpn.vlans** and **evpn.vrfs** lists
-   VLANs and VRFs mentioned in group **vlans**/**vrfs** dictionaries are [copied into all group members](https://netsim-tools.readthedocs.io/en/latest/groups.html#using-group-node-data-with-vrfs-and-vlans), resulting in VLAN interfaces and VRFs on all group members.

Finally, a few long-overdue items:

-   **node\_data** is deprecated – you can [specify node attributes directly in group data](https://netsim-tools.readthedocs.io/en/latest/groups.html#setting-node-data-in-groups).
-   Strict validation of topology, node, group, VLAN, VRF, and addressing attributes (see also [Breaking changes](https://netsim-tools.readthedocs.io/en/latest/release/1.4.html#breaking-changes))
-   ‘Device quirks’ framework deals with implementation limitations of individual virtual network devices (example: Arista cEOS does not support MPLS transport)

Upgrading is as easy as ever: execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netsim-tools.readthedocs.io/en/latest/tutorials.html) and the [installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html).
