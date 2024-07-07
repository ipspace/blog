---
date: 2022-05-30 05:57:00+00:00
netlab_tag: vlan_vrf
series_title: Simple VLAN Example
tags:
- netlab
title: netlab Simple VLAN Example
---
I had no idea how convoluted VLANs could get until I tried to [implement them in *netlab*](https://netlab.tools/module/vlan/).

We'll start with the simplest option: [a single VLAN](https://github.com/ipspace/netlab-examples/tree/master/VLAN/vlan-access-stretch) stretched across two ~~bridges~~ switches with two Linux hosts connected to it. *netlab* can [configure VLANs](https://netlab.tools/module/vlan/#platform-support) on Arista EOS, Cisco IOSv, Cisco Nexus OS, VyOS, Dell OS10, and Nokia SR Linux. We'll use the quickest (deployment-wise) option: Arista EOS on *containerlab*.

{{<figure src="/2022/05/vlan-simple.png" caption="Simple VLAN topology">}}
<!--more-->
We'll use *[groups](/2021/11/netsim-groups-deployment-templates/)* in the [lab topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-access-stretch/topology.yml) to define our devices. Members of the *hosts* group will be Linux containers, members of the *switches* group will be Arista EOS containers using *vlan* configuration module:

{{<cc>}}Defining nodes and groups{{</cc>}}
```
provider: clab

nodes: [ h1, h2, s1, s2 ]

groups:
  hosts:
    members: [ h1, h2 ]
    device: linux
  switches:
    members: [ s1, s2 ]
    module: [ vlan ]
    device: eos
```

Next step: defining VLANs. All we have to do is to define the VLAN name. 802.1q tag and VXLAN VNI are assigned automatically.

{{<cc>}}Defining *red* VLAN{{</cc>}}
```
vlans:
  red:
```

Finally, we have to specify the links in our lab. We'll set the access VLAN name with `vlan.access` attribute. On the switch-to-host links, we have to specify the access VLAN on the switch interface. On the inter-switch link we can set `vlan.access` as a link attribute -- it will be propagated to all switches connected to the link.

{{<cc>}}Links in our lab topology{{</cc>}}
```
links:
- h1:
  s1:
    vlan.access: red
- s1:
  s2:
  vlan.access: red
- s2:
    vlan.access: red
  h2:
```

VLAN configuration on s1 and s2 is performed automatically as part of the **netlab up** process. Here's the VLAN-related configuration from s1:

{{<cc>}}VLAN *red* configuration on s1 running Arista cEOS{{</cc>}}
```
vlan 1000
   name red
!
interface Ethernet1
   mac-address 52:dc:ca:fe:03:01
   switchport access vlan 1000
!
interface Ethernet2
   mac-address 52:dc:ca:fe:03:02
   switchport access vlan 1000
!
interface Vlan1000
   description VLAN red (1000) -> [h1,s2,h2]
   ip address 172.16.0.3/24
```

Here's the corresponding configuration on Cisco IOSv[^BVI]:

[^BVI]: You don't want to know how long it took me to remember how to configure bridging on Cisco IOS router (not switch) image. CSR 1000v is a totally different beast, and I haven't even tried to get VLANs to work on it -- feel free to fix that and submit a pull request.

{{<cc>}}VLAN *red* configuration on Cisco IOSv{{</cc>}}
```
bridge irb
!
interface GigabitEthernet0/1
 bridge-group 1
!
interface GigabitEthernet0/2
 bridge-group 1
!
interface BVI1
 description VLAN red (1000) -> [h1,s2,h2]
 ip address 172.16.0.3 255.255.255.0
!
bridge 1 protocol ieee
bridge 1 route ip
```

### VLAN IP Addressing

A *netlab* VLAN segment is a single subnet; the IPv4 and IPv6 prefixes are allocated from the `lan` [address pool](https://netlab.tools/example/addressing-tutorial/). All physical links and VLAN interfaces belonging to the same access VLAN use the same IP subnet. The IPv4 addresses in our lab are thus set up as follows:

| Node   | IP address in red VLAN |
|--------|-----------------------:|
| h1     |             172.16.0.1 |
| h2     |             172.16.0.2 |
| s1     |             172.16.0.3 |
| s2     |             172.16.0.4 |
{class="fmtTable" style="width: auto;"}

The Linux hosts (OK, containers) can ping the IPv4 addresses assigned to the switch VLAN interfaces, but not the loopback IP addresses of both switches -- the Linux hosts have a default route pointing to one of the switches, and there's no routing configured between the switches:

{{<cc>}}Pinging from Linux container{{</cc>}}
```
$ netlab connect h1
Connecting to container clab-vlan-access-stretch-h1, starting bash
h1:/# ping -c 5 -q h2
PING h2 (172.16.0.2): 56 data bytes
--- h2 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 3.261/3.475/3.598 ms
h1:/# ping -c 5 -q s1
PING s1 (10.0.0.3): 56 data bytes
--- s1 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 1.616/1.734/1.823 ms
h1:/# ping -c 5 -q s2
PING s2 (10.0.0.4): 56 data bytes
--- s2 ping statistics ---
5 packets transmitted, 0 packets received, 100% packet loss
h1:/# ping -c 5 -q 172.16.0.4
PING 172.16.0.4 (172.16.0.4): 56 data bytes
--- 172.16.0.4 ping statistics ---
5 packets transmitted, 5 packets received, 0% packet loss
round-trip min/avg/max = 3.040/3.232/3.363 ms
```

Next time, we'll fix IP routing and add OSPF routing process to the switches. You could also do it on your own:

* [Set up a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/) or a bare-metal server with netlab, Docker and containerlab
* [Install Arista cEOS container image](https://netlab.tools/labs/clab/)
* Copy the [lab topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-access-stretch/topology.yml) into an empty directory
* Start the lab with **netlab up** and start exploring
