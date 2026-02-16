---
title: "Explore Configurations of Unfamiliar Devices with netlab"
date: 2026-02-16 08:28:00+0100
tags: [ netlab ]
netlab_tag: use
---
Apart from IP multicast and QoS, _netlab_ can configure [commonly used networking technologies](https://netlab.tools/platforms/#supported-configuration-modules) across [dozens of devices](https://netlab.tools/platforms/#supported-virtual-network-devices) from most networking vendors. Why don't you use all that embedded knowledge (supported by [hundreds of integration tests](https://release.netlab.tools/)) to help you configure unfamiliar devices?

You don't have to install VM or container managers (Vagrant/containerlab), or beg vendors to give you access to device VMs/containers, to get working device configurations. All you need is a Python package that works on Windows[^WSL], macOS, or Linux.

It's as simple as this:
<!--more-->
* Install **networklab** Python package. As we're dealing with a one-off test, use a virtual environment:

```bash
$ python3 -m venv nlt
$ source ./nlt/bin/activate
$ pip3 install networklab
```

{{<note info>}}
If you feel adventurous and don't mind running a script downloaded from a random website through **sh**, use the phenomenal **[uvx.sh](https://uvx.sh/)** service to install *netlab* (visit uvx.sh to find out the corresponding Windows command):

```
$ curl -LsSf uvx.sh/networklab/install.sh | sh
```

Compared to what [we had to deal with](https://xkcd.com/1987/), UVX is condensed [PFM](https://idioms.thefreedictionary.com/P.F.M).
{{</note>}}

* Even better, [open the *netlab-examples* repository as a GitHub Codespace](/2024/07/netlab-examples-codespaces/).
* Find the most appropriate lab topology in [netlab examples](https://github.com/ipspace/netlab-examples), [integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration), [BGP labs](https://github.com/bgplab/bgplab), [IS-IS labs](https://github.com/bgplab/isis), or [EVPN/VXLAN](https://github.com/bgplab/evpn) labs[^SL]. You could also [try to cajole your AI buddy](/2025/05/chatgpt-netlab-topology/) into creating a working netlab topology[^WBP].
* Copy the topology URL
* Find the _netlab_ device name in the [supported platforms](https://netlab.tools/platforms/#supported-virtual-network-devices) table
* Download the topology and create all the configuration files with **netlab create -d *device* -o config *url***. If you want to use a device that's only available as a container (Cisco IOL, SR Linux), add **-p clab** option.

  For example, use the following command to create EVPN/VXLAN bridging configuration for a Cisco IOS/XE router (IOL):

[^WSL]: I know of people using _netlab_ on Windows Subsystem for Linux. As we'll be using only Python functionality, everything should also work on Windows.

[^WBP]: It works better if you include pointers to https://netlab.tools/ and https://github.com/ipspace/netlab-examples in the prompt.

[^SL]: Some labs include `solution.yml` topology.

```bash
$ netlab create -d iol -p clab -o config https://github.com/bgplab/evpn/blob/main/evpn/1-bridging/solution.yml
```

{{<note info>}}
* Treat the downloaded lab topology as a scratchpad and adjust it to your needs.
* Some topologies have hard-coded devices. Edit them and remove all mentions of **device** attributes
* Integration tests often include **validation** part or extra **plugins** that help make tests work (with warnings) across semi-supported devices. Edit that out.
* Retry as often as needed ;), replacing the URL with **downloaded.yml** (the name of the downloaded topology file). 
{{</note>}}

* Explore the `node_files` directory. It has a separate subdirectory for each node in the lab topology; each subdirectory contains a file for every configuration module (technology) used on the node. For example, these are the files we'd get for the S1 switch running Cisco IOL:

```
$ ls node_files/s1
bgp     evpn    ifstate initial ospf    vlan    vxlan
```

Here's a sample Cisco IOL VLAN and VXLAN configuration:

```
!
bridge-domain 100
 member Ethernet0/2 service-instance 100
!
interface Ethernet0/2
 service instance 100 ethernet
  encapsulation untagged
```

```
interface nve1
 no shutdown
 source-interface Loopback0
 host-reachability protocol bgp
 member vni 100100 ingress-replication
```

And here's the EVPN part (it has an extra **route-map** that is used only on EBGP sessions):

```
! 
bridge-domain 100
 member evpn-instance 100 vni 100100
!
l2vpn evpn instance 100 vlan-based
 encapsulation vxlan
 replication-type ingress
 rd 10.0.0.1:100
 route-target import 65000:100
 route-target export 65000:100
!
route-map evpn_nh_unchanged permit 10
 set ip next-hop unchanged
!
router bgp 65000
 address-family l2vpn evpn
  neighbor 10.0.0.2 activate
  neighbor 10.0.0.2 send-community both
```

Obviously, you could also ask your favorite AI buddy to create the device configs directly ;)
