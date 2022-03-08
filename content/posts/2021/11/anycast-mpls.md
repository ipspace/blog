---
title: "Anycast Works Just Fine with MPLS/LDP"
date: 2021-11-17 07:24:00
tags: [ MPLS, LDP ]
series: netsim
netsim_tag: use
lastmod: 2022-02-16 16:15:00
pre_scroll: True
---
I stumbled upon an article praising the beauties of SR-MPLS that claimed:

> Yet MPLS, until recently, was deprived of anycast routing. This is because MPLS is not a pure packet switching technology, but has a control plane based on virtual circuit switching.

My first reaction was "_that's not how MPLS works_,"[^1] followed by "_that would be fun to test_" a few seconds later.
<!--more-->
[^1]: At least not on any device I worked with.

I created a tree network to test the *anycast with MPLS* idea:

{{<figure src="/2021/11/MPLS-anycast-ospf-topo.png" caption="Anycast test network">}}

The lab is built from Arista EOS containers running under *containerlab* (build instructions). The whole network is running OSPF, and MPLS/LDP will be enabled on all links. A1, A2 and A3 will advertise the same prefix (10.0.0.42/32) into OSPF. According to the "*no anycast with MPLS*" claim, L1 should not be able to reach all three anycast nodes.

You probably know I prefer typing CLI commands over chasing rodents, so I used *[netsim-tools](https://netsim-tools.readthedocs.io/en/latest/)* to build the lab. Here's the [topology file](https://github.com/ipspace/netsim-examples/blob/master/routing/anycast-mpls-ospf/topology.yml) (I don't think it can get any simpler than that)

{{<cc>}}Initial version of the topology file{{</cc>}}
```
module: ospf

defaults.device: eos
provider: clab

nodes: [ l1, l2, l3, s1, a1, a2, a3 ]

links: [ s1-l1, s1-l2, s1-l3, l2-a1, l2-a2, l3-a3 ]
```

{{<note info>}}I [created the network diagram](https://netsim-tools.readthedocs.io/en/latest/outputs/graph.html) with **netlab create -o graph** command followed by **‌dot -Grankdir=RL -T png -o graph.ospf.png graph.dot** (using the [*rankdir* trick Jeroen van Bemmel taught me](https://blog.ipspace.net/2021/11/bgp-multipath-netsim-tools.html#off-topic-nicer-looking-graphs)).{{</note>}}

**Next step**: starting the lab with **[netlab up](https://netsim-tools.readthedocs.io/en/latest/netlab/up.html)** and waiting a minute or so.

Now for the fun part: *netsim-tools* don't support MPLS/LDP or anycast yet[^R113]. Time for some custom Jinja2 templates. 

[^R113]: As of release 1.1.3

Fortunately, Arista EOS doesn't need any interface-level configuration to enable MPLS and LDP. The [configuration template](https://github.com/ipspace/netsim-examples/blob/master/routing/anycast-mpls-ospf/mpls-ldp.j2) is thus as simple as it can get:

{{<cc>}}mpls-ldp.j2: Enable MPLS and LDP on Arista EOS{{</cc>}}
```
mpls ip
!
mpls ldp
 router-id interface Loopback0
 label local-termination explicit-null
 no shutdown
```

Please note that the above template configures two LDP parameters:

* Advertise explicit NULL to make the LFIB table on L2 and L3 look nicer;
* Set LDP router ID to a loopback interface with a unique IP address (more about that at the [end of the blog post](#the-curse-of-duplicate-addresses))

I needed [another custom template](https://github.com/ipspace/netsim-examples/blob/master/routing/anycast-mpls-ospf/ospf-anycast-loopback.j2) to create the loopback interface on the anycast nodes and advertise it into OSPF:

{{<cc>}}ospf-anycast-loopback.j2: Advertise anycast prefix from anycast nodes{{</cc>}}
```
interface Loopback42
 ip address 10.0.0.42/32
 ip ospf area 0.0.0.0
```

I could use **[netlab config](https://netsim-tools.readthedocs.io/en/latest/netlab/config.html)** command to configure lab devices with a custom Jinja2 template, but decided to make the custom configuration part of the lab topology -- MPLS/LDP and anycast loopbacks will be configured every time the lab is started with **netlab up**. I used *[groups](https://netsim-tools.readthedocs.io/en/latest/groups.html)* to apply the configuration templates to groups of lab devices:

{{<cc>}}Lab topology with custom configuration templates{{</cc>}}
```
module: [ ospf ]

defaults.device: eos
provider: clab

groups:
  anycast:
    members: [ a1, a2, a3 ]
    config: [ ospf-anycast-loopback.j2 ]
  all:
    config: [ mpls-ldp.j2 ]

nodes: [ l1, l2, l3, s1, a1, a2, a3 ]

links: [ s1-l1, s1-l2, s1-l3, l2-a1, l2-a2, l3-a3 ]
```

### Smoke Test

Let's inspect the routing tables first (hint: **[netlab connect](https://netsim-tools.readthedocs.io/en/latest/netlab/connect.html)** is an easy way to connect to lab devices without bothering with their IP addresses or /etc/hosts file). 

Here's the routing table entry for 10.0.0.42 on L2:

{{<cc>}}Anycast routing entry on L2{{</cc>}}
```
l2>show ip route detail | section 10.0.0.42
 O        10.0.0.42/32 [110/20] via 10.1.0.13, Ethernet2 l2 -> a1
                                via 10.1.0.17, Ethernet3 l2 -> a2
```

Likewise, S1 has two paths to the anycast prefix (through L2 and L3):

{{<cc>}}Anycast routing entry on S1{{</cc>}}
```
s1>show ip route detail | section 10.0.0.42
 O        10.0.0.42/32 [110/30] via 10.1.0.5, Ethernet2 s1 -> l2
                                via 10.1.0.9, Ethernet3 s1 -> l3
```

What about MPLS forwarding table? Here's the LFIB entry for 10.0.0.42 or S1. Please note that a single incoming label maps into two outgoing labels, interfaces, and next hops. 

{{<cc>}}Anycast MPLS entry on S1{{</cc>}}
```
s1>show mpls lfib route detail | section 10.0.0.42
 L     116386   [1], 10.0.0.42/32
                via M, 10.1.0.9, swap 116385
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet3
                via M, 10.1.0.5, swap 116384
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet2
```

And here's the corresponding LFIB entry from L2. Please note that the anycast nodes advertise the anycast prefix with *explicit-null* label because I configured **‌label local-termination explicit-null**.

{{<cc>}}Anycast MPLS entry on L2{{</cc>}}
```
l2>show mpls lfib route detail | section 10.0.0.42
 L     116384   [1], 10.0.0.42/32
                via M, 10.1.0.13, swap 0
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet2
                via M, 10.1.0.17, swap 0
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet3
```

The final test (**traceroute** from L1 to anycast IP address) failed on Arista cEOS or vEOS. The data plane implementation of Arista's virtual devices seems to be a bit limited: even though there are several next hops in the EOS routing table and LFIB, I couldn't find a nerd knob to force more than one entry into Linux routing table (which is used for packet forwarding).

However, if you repeat the same tests on Cisco IOS with **ip cef load-sharing algorithm include-ports source destination** configured, you'll see **traceroute** printouts ending on different anycast nodes:

{{<cc>}}Cisco IOS traceroute from L1 to anycast IP{{</cc>}}
```
l1#traceroute 10.0.0.42 port 80
Type escape sequence to abort.
Tracing the route to 10.0.0.42
VRF info: (vrf in name/id, vrf out name/id)
  1 s1 (10.1.0.2) [MPLS: Label 25 Exp 0] 1 msec 1 msec 1 msec
  2 l2 (10.1.0.5) [MPLS: Label 25 Exp 0] 1 msec 1 msec
    l3 (10.1.0.9) [MPLS: Label 26 Exp 0] 1 msec
  3 a3 (10.1.0.21) 1 msec *
    a2 (10.1.0.17) 1 msec
```

After increasing the probe count (as suggested by _Anonymous_ in the comments), the trace reaches all three anycast servers:

{{<cc>}}Increasing the probe count on traceroute from L1 to anycast IP{{</cc>}}
```
l1#traceroute 10.0.0.42 port 80 probe 10
Type escape sequence to abort.
Tracing the route to 10.0.0.42
VRF info: (vrf in name/id, vrf out name/id)
  1 s1 (10.1.0.2) [MPLS: Label 25 Exp 0] 1 msec 1 msec...
  2 l3 (10.1.0.9) [MPLS: Label 26 Exp 0] 1 msec 1 msec
    l2 (10.1.0.5) [MPLS: Label 25 Exp 0] 1 msec 1 msec...
  3 a2 (10.1.0.17) 1 msec *
    a3 (10.1.0.21) 1 msec *
    a1 (10.1.0.13) 1 msec *
    a3 (10.1.0.21) 1 msec *
    a1 (10.1.0.13) 1 msec *
```

**Myth busted**. Traditional MPLS offers more than P2P virtual circuits. MPLS forwarding entries follow the IP routing table entries. While I like SR-MPLS (as opposed to its ugly cousin SRv6), you don't need it to run anycast services; LDP works just fine.

### The Curse of Duplicate Addresses

While anycast works with MPLS/LDP (as demonstrated), LDP is not completely happy with the setup.

Worst case, anycast servers choose the anycast IP address as the LDP Identifier, and the adjacent devices try to connect to the anycast IP address when establishing LDP TCP session. That can't end well -- you have to set the LDP router ID to the loopback interface with unique IP address.

LDP also advertises all local IP addresses to LDP neighbors to help them map FIB next hops to LDP neighbors[^PLINK]. Multiple LDP neighbors advertising the same IP address make L2 decidedly unhappy[^LDPDup], resulting in syslog messages like this one:

```
Feb 16 17:57:25 l2 LdpAgent: %LDP-6-SESSION_UP: Peer LDP ID: 10.0.0.4:0, Peer IP: 10.0.0.4, Local LDP ID: 10.0.0.2:0, VRF: default
Feb 16 17:57:25 l2 LdpAgent: %LDP-6-SESSION_UP: Peer LDP ID: 10.0.0.6:0, Peer IP: 10.0.0.6, Local LDP ID: 10.0.0.2:0, VRF: default
Feb 16 17:57:25 l2 LdpAgent: %LDP-6-SESSION_UP: Peer LDP ID: 10.0.0.5:0, Peer IP: 10.0.0.5, Local LDP ID: 10.0.0.2:0, VRF: default
Feb 16 17:57:25 l2 LdpAgent: %LDP-4-DUPLICATE_PEER_INTERFACE_IP: Duplicate interface IP 10.0.0.42 detected on 10.0.0.5:0
```

The setup still works, but the extraneous syslog messages might upset an overly fastidious networking engineer. To make LDP happy, run BGP (not OSPF) with the anycast servers, and distribute labels for anycast addresses with IPv4/IPv6 labeled unicast (BGP-LU) address family. 

Yeah, I know I have to set up another lab to prove that ;) Mañana...

[^PLINK]: You can also use the list of local addresses to identify parallel links.

[^LDPDup]: The error messages appear only on devices that have more than one LDP session to anycast servers (L2 in our lab topology).

### Build Your Own Lab

To replicate this experiment:

* [Set up a Linux server or virtual machine](https://netsim-tools.readthedocs.io/en/latest/install.html#creating-the-lab-environment). If you don't have a preferred distribution, use Ubuntu.
* [Install netsim-tools](https://netsim-tools.readthedocs.io/en/latest/install.html#installing-netsim-tools-package)
* [Install Docker and containerlab](https://netsim-tools.readthedocs.io/en/latest/labs/clab.html) (**[netlab install containerlab](https://netsim-tools.readthedocs.io/en/latest/netlab/install.html)** is the easiest way to do it on Ubuntu).
* Install Ansible

The easiest way to do all of the above is to [follow these instructions](https://netsim-tools.readthedocs.io/en/latest/labs/virtualbox.html).

Next:
 
* [Download and install Arista cEOS image](https://netsim-tools.readthedocs.io/en/latest/labs/clab.html#container-images) -- I can't automate that, as you have to register on Arista's web site to get access to the cEOS image.
* Download the [lab topology file](https://github.com/ipspace/netsim-examples/blob/master/routing/anycast-mpls-ospf/topology.yml) into an empty directory
* Execute **netlab up**

Alternatively, you can [download the configuration tarball into an empty directory](https://github.com/ipspace/netsim-examples/raw/master/routing/anycast-mpls-ospf/anycast-mpls-ospf.tar.gz), extract configuration files from it, and start the lab with *containerlab.*

### Revision History

2021-11-17
: The _curse of duplicate addresses_ section has been added based on [feedback from Dmytro Shypovalov](https://twitter.com/routingcraft/status/1461007769511907331). Thanks a million for keeping me on the straight and narrow!

2021-11-18
: Added a _traceroute_ printout with larger probe count as suggested by an anonymous commenter.

2022-02-16
: Rewrote the blog post to use Arista cEOS. Also added lab setup instructions.

2022-03-08
: Added a link to configuration tarball
