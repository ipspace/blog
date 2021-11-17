---
title: "Anycast Works Just Fine with MPLS/LDP"
date: 2021-11-17 07:24:00
tags: [ MPLS, LDP ]
series: netsim-tools
series_tag: use
lastmod: 2021-11-17 17:58:00
---
I stumbled upon an article praising the beauties of SR-MPLS that claimed:

> Yet MPLS, until recently, was deprived of anycast routing. This is because MPLS is not a pure packet switching technology, but has a control plane based on virtual circuit switching.

My first reaction was "_that's not how MPLS works_,"[^1] followed by "_that would be fun to test_" a few seconds later.
<!--more-->
[^1]: At least not on any device I worked with.

I created a tree network to test the *anycast with MPLS* idea:

{{<figure src="/2021/11/MPLS-anycast-ospf-topo.png" caption="Anycast test network">}}

The whole network is running OSPF, and MPLS/LDP is enabled on all links. A1, A2 and A3 will advertise the same prefix (10.0.0.42/32) into OSPF. According to the "_no anycast with MPLS_" claim, L1 should not be able to reach all three anycast nodes.

You probably know I prefer typing CLI commands over chasing rodents, so I used *[netsim-tools](https://netsim-tools.readthedocs.io/en/latest/)* to build the lab. Here's the [topology file](https://github.com/ipspace/netsim-examples/blob/master/routing/anycast-mpls/ospf.yml) (I don't think it can get any simpler than that)

```
module: ospf

defaults:
  device: iosv

nodes: [ l1, l2, l3, s1, a1, a2, a3 ]

links: [ s1-l1, s1-l2, s1-l3, l2-a1, l2-a2, l3-a3 ]
```

I [created the network diagram](https://netsim-tools.readthedocs.io/en/latest/outputs/graph.html) with **netlab create -o graph** command followed by **‌dot -Grankdir=RL -T png -o graph.ospf.png graph.dot** (using the [*rankdir* trick Jeroen van Bemmel taught me](https://blog.ipspace.net/2021/11/bgp-multipath-netsim-tools.html#off-topic-nicer-looking-graphs)).

Next step: starting the lab with **[netlab up](https://netsim-tools.readthedocs.io/en/latest/netlab/up.html)** and waiting a minute or so.

Now for the fun part: *netsim-tools* don't support MPLS/LDP or anycast yet. Time for some custom Jinja2 templates.

I used **netlab create -o yaml** to get the final data structure   that would be passed to Ansible playbooks [in YAML format](https://netsim-tools.readthedocs.io/en/latest/outputs/yaml-or-json.html) -- there's a **links** element in every lab node describing its links. Alternatively, you could look into Ansible inventory created with **[netlab create](https://netsim-tools.readthedocs.io/en/latest/netlab/create.html)** command.

{{<cc>}}Ansible inventory data for S1{{</cc>}}
```
---
box: cisco/iosv
links:
- ifindex: 1
  ifname: GigabitEthernet0/1
  ipv4: 10.1.0.2/30
  linkindex: 1
  name: s1 -> l1
  neighbors:
    l1:
      ifname: GigabitEthernet0/1
      ipv4: 10.1.0.1/30
  remote_id: 1
  remote_ifindex: 1
  type: p2p
- ifindex: 2
  ifname: GigabitEthernet0/2
  ipv4: 10.1.0.6/30
  linkindex: 2
  name: s1 -> l2
  neighbors:
    l2:
      ifname: GigabitEthernet0/1
      ipv4: 10.1.0.5/30
  remote_id: 2
  remote_ifindex: 1
  type: p2p
...
```

Using the **links** element to configure MPLS with LDP is a piece of cake:

```
mpls ldp explicit-null
mpls ldp router-id Loopback 0
{% for l in links %}
!
interface {{ l.ifname }}
 mpls ip
{% endfor %}
```

**[netlab config](https://netsim-tools.readthedocs.io/en/latest/netlab/config.html)** command allows you to configure lab devices with a custom Jinja2 template. **netlab config mpls-ldp.j2** was all I needed to configure MPLS in my lab.

---

Please note that the above template configures two LDP parameters:

* Advertise explicit NULL to make the LFIB table on L2 and L3 look nicer;
* Set LDP router ID to a loopback interface with a unique IP address (more about that at the end of the blog post)

---

Configuring anycast was even easier -- add another loopback interface:

```
interface loopback 42
 ip address 10.0.0.42 255.255.255.255
 ip ospf 1 area 0
```

I had to be careful when running **netlab config**. The loopback interface should be added only to A1, A2, and A3, but I thought about that use case when writing **netlab config** code -- any parameter after the template name is passed to the internal Ansible playbook. Presto: **netlab config ospf-anycast-loopback.j2 \-\-limit a1,a2,a3**

### Smoke Test

Let's inspect the routing tables first (hint: **[netlab connect](https://netsim-tools.readthedocs.io/en/latest/netlab/connect.html)** is an easy way to connect to lab devices without bothering with their IP addresses or /etc/hosts file). 

Here's the routing table entry for 10.0.0.42 on L2:

{{<cc>}}Anycast routing entry on L2{{</cc>}}
```
l2#show ip route 10.0.0.42
Routing entry for 10.0.0.42/32
  Known via "ospf 1", distance 110, metric 2, type intra area
  Last update from 10.1.0.17 on GigabitEthernet0/3, 08:38:23 ago
  Routing Descriptor Blocks:
    10.1.0.17, from 10.0.0.6, 08:38:23 ago, via GigabitEthernet0/3
      Route metric is 2, traffic share count is 1
  * 10.1.0.13, from 10.0.0.5, 08:38:23 ago, via GigabitEthernet0/2
      Route metric is 2, traffic share count is 1
```

Likewise, S1 has two paths to the anycast prefix (through L2 and L3):

{{<cc>}}Anycast routing entry on S1{{</cc>}}
```
s1#show ip route 10.0.0.42
Routing entry for 10.0.0.42/32
  Known via "ospf 1", distance 110, metric 3, type intra area
  Last update from 10.1.0.9 on GigabitEthernet0/3, 08:41:20 ago
  Routing Descriptor Blocks:
    10.1.0.9, from 10.0.0.7, 08:41:20 ago, via GigabitEthernet0/3
      Route metric is 3, traffic share count is 1
  * 10.1.0.5, from 10.0.0.5, 08:41:20 ago, via GigabitEthernet0/2
      Route metric is 3, traffic share count is 1
```

What about MPLS forwarding table? Here's the LFIB entry for 10.0.0.42 or S1. Please note that a single incoming label maps into two outgoing labels, interfaces, and next hops. 

{{<cc>}}Anycast MPLS entry on S1{{</cc>}}
```
s1#show mpls forwarding-table 10.0.0.42 detail
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label      Label      or Tunnel Id     Switched      interface
25         25         10.0.0.42/32     0             Gi0/2      10.1.0.5
	MAC/Encaps=14/18, MRU=1500, Label Stack{25}
	525400D2EC095254000324028847 00019000
	No output feature configured
    Per-destination load-sharing, slots: 0
           26         10.0.0.42/32     0             Gi0/3      10.1.0.9
	MAC/Encaps=14/18, MRU=1500, Label Stack{26}
	525400474CE15254008857F68847 0001A000
	No output feature configured
    Per-destination load-sharing, slots: 1
```

And here's the corresponding LFIB entry from L2. Please note that the anycast nodes advertise the anycast prefix with *explicit-null* label because I configured **‌mpls ldp explicit-null**.

{{<cc>}}Anycast MPLS entry on S1{{</cc>}}
```
l2#show mpls forwarding-table 10.0.0.42 detail
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label      Label      or Tunnel Id     Switched      interface
25         explicit-n 10.0.0.42/32     0             Gi0/2      10.1.0.13
	MAC/Encaps=14/18, MRU=1500, Label Stack{}
	525400AE15B4525400A4C6208847 00000000
	No output feature configured
    Per-destination load-sharing, slots: 0
           explicit-n 10.0.0.42/32     0             Gi0/3      10.1.0.17
	MAC/Encaps=14/18, MRU=1500, Label Stack{}
	5254006D57E7525400CAEC468847 00000000
	No output feature configured
    Per-destination load-sharing, slots: 1
```

The final test: **traceroute** from L1 to anycast IP address. I had to configure **ip cef load-sharing algorithm include-ports source destination** to change the IOS load balancing algorithm to 5-tuple load balancing. After that, **traceroute** commands ended on different anycast nodes:

{{<cc>}}Traceroute from L1 to anycast IP{{</cc>}}
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

**Myth busted**. Traditional MPLS offers more than P2P virtual circuits. MPLS forwarding entries follow the IP routing table entries. While I like SR-MPLS (as opposed to its ugly cousin SRv6), you don't need it to run anycast services; LDP works just fine.

### The Curse of Duplicate Addresses

While anycast works with MPLS/LDP (as demonstrated), LDP is not completely happy with the setup.

Worst case, anycast servers choose the anycast IP address as the LDP Identifier, and the adjacent devices try to connect to the anycast IP address when establishing LDP TCP session. That can't end well. To fix this one, use **mpls ldp router-id** on Cisco IOS (and an equivalent command on your platform-of-choice).

LDP also advertises all local IP addresses to LDP neighbors to help them map FIB next hops to LDP neighbors[^PLINK]. Multiple LDP neighbors advertising the same IP address make L2 decidedly unhappy[^LDPDup], resulting in syslog messages like this one:

```
%TAGCON-3-DUP_ADDR_RCVD: Duplicate Address 10.0.0.42 advertised ↩︎
by peer 10.0.0.6:0 is already bound to 10.0.0.5:0
%TAGCON-3-TDPID: peer 10.0.0.6:0, TDP Id/Addr mapping problem ↩︎
(rcvd TDP address PIE, bind failed)
```

The setup still works, but the extraneous syslog messages might upset an overly fastidious networking engineer. To make LDP happy, run BGP (not OSPF) with the anycast servers, and distribute labels for anycast addresses with IPv4/IPv6 labeled unicast (BGP-LU) address family. 

Yeah, I know I have to set up another lab to prove that ;) Mañana...

[^PLINK]: You can also use the list of local addresses to identify parallel links.

[^LDPDup]: The error messages appear only on devices that have more than one LDP session to anycast servers (L2 in our lab topology).

### Revision History

2021-11-17
: The _curse of duplicate addresses_ section has been added based on [feedback from Dmytro Shypovalov](https://twitter.com/routingcraft/status/1461007769511907331). Thanks a million for keeping me on the straight and narrow!