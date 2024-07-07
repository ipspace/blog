---
date: 2022-04-25 07:07:00+00:00
netlab_tag: extend
pre_scroll: true
series_title: Multi-Platform Custom Configuration Templates
tags:
- netlab
title: netlab Multi-Platform Custom Configuration Templates
---
In the _[Building a BGP Anycast Lab](/2021/12/bgp-anycast-lab/)_ I described how you could use custom configuration templates to extend the *netlab* functionality. 

That example used Cisco IOS... but what if you want to test the same functionality on multiple platforms? *[netlab](https://netlab.tools/)* provides a nice trick: the [custom configuration template](https://netlab.tools/groups/#custom-configuration-templates) could point to a directory with platform-specific templates. Let me show you how that works...
<!--more-->
We'll start with the [BGP anycast topology](https://github.com/ipspace/netlab-examples/blob/master/routing/anycast-bgp-addpath/topology.yml), but change the lab devices to a mix of Cisco IOS, Arista EOS, and Cumulus VX:

* Most devices will run Cisco IOSv
* One of the leaf switches and one of the anycast nodes will run Arista EOS
* Another anycast node will run Cumulus VX

{{<figure src="/2022/04/multi-platform-bgp-anycast.png" caption="Physical lab topology">}}

{{<cc>}}Lab topology definition{{</cc>}}
```
module: [ ospf, bgp ]
defaults.bgp.extra_attributes.node: [ anycast ]

bgp:
  as_list:
    65000:
      members: [ l1, l2, l3, s1 ]
      rr: [ s1 ]
    65101:
      members: [ a1,a2,a3 ]

defaults.device: iosv

nodes: 
  l1:
  l2:
    device: eos
  l3:
  s1:
  a1:
  a2:
    device: eos
  a3:
    device: cumulus

links: [ s1-l1, s1-l2, s1-l3, l2-a1, l2-a2, l3-a3 ]
```

Now for the multi-platform custom configuration trick: we'll specify *directories* instead of *template file names* in group **config** attributes (read the [BGP anycast](/2021/12/bgp-anycast-lab/) blog post for more details).

{{<cc>}}Using directories as custom configuration templates{{</cc>}}
```
groups:
  as65000:
    config: [ bgp-addpath ]
  as65101:
    config: [ bgp-anycast ]
    node_data:
      bgp.anycast: 10.42.42.42/32
      bgp.advertise_loopback: False
```

The [final lab topology file](https://github.com/ipspace/netlab-examples/blob/master/multi-platform/bgp-anycast/topology.yml) is [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/multi-platform/bgp-anycast).

We'll have three files within the `bgp-anycast` directory: `ios.j2`, `eos.j2` and `cumulus.j2`:

{{<cc>}}Custom configuration template for Cisco IOS (bgp-anycast/ios.j2){{</cc>}}
```
{% if bgp is defined and bgp.anycast is defined %}
interface loopback 42
 ip address {{ bgp.anycast|ipaddr('address') }} {{ bgp.anycast|ipaddr('netmask') }}
!
router bgp {{ bgp.as }}
 address-family ipv4
  network {{ bgp.anycast|ipaddr('address') }} mask {{ bgp.anycast|ipaddr('netmask') }}
{% endif %}
```

{{<cc>}}Custom configuration template for Arista EOS (bgp-anycast/eos.j2){{</cc>}}
```
{% if bgp is defined and bgp.anycast is defined %}
interface loopback 42
 ip address {{ bgp.anycast }}
!
router bgp {{ bgp.as }}
 address-family ipv4
  network {{ bgp.anycast|ipaddr('0') }}
{% endif %}
```
 
{{<cc>}}Custom configuration template for Cumulus VX (bgp-anycast/cumulus.j2){{</cc>}}
```
{% if bgp is defined and bgp.anycast is defined %}
interface lo
 ip address {{ bgp.anycast }} label anycast
!
router bgp {{ bgp.as }}
 address-family ipv4
  network {{ bgp.anycast|ipaddr('0') }}
{% endif %}
```

Ansible playbook printout generated during the lab initialization (using **netlab up -q** command) displays the templates used to configure lab devices -- as you can see, every platform uses a different configuration template.

```
# ios_config: deploying bgp-anycast from /home/pipi/net101/multi-platform/bgp-anycast/bgp-anycast/ios.j2 ******************
  * a1                         - changed=True --  ---------------------------------------------
...
# eos_config: deploying bgp-anycast from /home/pipi/net101/multi-platform/bgp-anycast/bgp-anycast/eos.j2 ******************
  * a2                         - changed=True --  ---------------------------------------------
.....
# run vtysh to import bgp-anycast config from /home/pipi/net101/multi-platform/bgp-anycast/bgp-anycast/cumulus.j2 *********
  * a3                         - changed=True --  ---------------------------------------------
...
# ios_config: deploying bgp-addpath from /home/pipi/net101/multi-platform/bgp-anycast/bgp-addpath/ios.j2 ******************
  * l1                         - changed=True --  ---------------------------------------------
...
# eos_config: deploying bgp-addpath from /home/pipi/net101/multi-platform/bgp-anycast/bgp-addpath/eos.j2 ******************
  * l2                         - changed=True --  ---------------------------------------------
...
# ios_config: deploying bgp-addpath from /home/pipi/net101/multi-platform/bgp-anycast/bgp-addpath/ios.j2 ******************
  * l3                         - changed=True --  ---------------------------------------------
...
# ios_config: deploying bgp-addpath from /home/pipi/net101/multi-platform/bgp-anycast/bgp-addpath/ios.j2 ******************
  * s1                         - changed=True --  ---------------------------------------------
```

Want to test this functionality on your own? [Install netlab](https://netlab.tools/install/) (and a bunch of other stuff), [download the lab topology and custom configuration templates from GitHub](https://github.com/ipspace/netlab-examples/tree/master/multi-platform/bgp-anycast), and execute **netlab up**.