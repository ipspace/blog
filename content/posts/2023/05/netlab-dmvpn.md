---
title: "Building a DMVPN Test Lab with netlab"
date: 2023-05-08 06:40:00
tags: [ netlab, DMVPN ]
netlab_tag: [ use ]
pre_scroll: True
---
I always love to hear about real-life [netlab](https://netlab.tools/) use cases, and try to make them even easier to implement with new netlab features -- that's how netlab got [custom Vagrant configuration templates](https://blog.ipspace.net/2022/06/netsim-custom-vagrant-boxes.html) and [per-node configuration templates](https://blog.ipspace.net/2023/04/netlab-merge-config.html). 

When [Anne Baretta](/kb/NetAutJourney/index.html) sent me his initial DMVPN solution, we quickly figured out we could make it even cleaner if netlab supported [tunnel interfaces](https://netlab.tools/links/#links-tunnel); you can enjoy the results in [release 1.5.2](https://netlab.tools/release/1.5/#release-1-5-2), and [explore Anne's solution on GitHub](https://github.com/ipspace/netlab-examples/tree/master/DMVPN).
<!--more-->
Let me just point out a few minor details of that solution, starting with [lab topology](https://github.com/ipspace/netlab-examples/blob/master/DMVPN/topology.yml):

* Anne used custom node attributes (**dmvpn**) to define DMVPN tunnel parameters (NHRP and IPsec keys). He defined them within groups to eliminate redundant data; note how he used hierarchical groups to apply the same data to hub- and spoke routers while using different configuration templates for hubs and spokes.

```
groups:
  hubs:
    members: [ hub1, hub2 ]
    config: hub.j2
  spokes:
    members: [ spoke1, spoke2 ]
    config: spoke.j2
  vpn: 
    members: [ hubs, spokes ]
    dmvpn:
      nhrp_keys: {"hub1": "nhrp1234","hub2": "nhrp4321"}
      isakmp_key: "isakmp1234"
```

* Starting with release 1.5.0, you have to define custom attributes within system defaults. This is how Anne defined **dmvpn** node attribute:

```
defaults:
  attributes:
    node:
      dmvpn: dict
```

{{<note>}}**dmvpn** attribute is a dictionary, so you could define its internal structure (allowed keys) instead of just specifying its type if you wanted stricter data validation.{{</note>}}

* Anne also used **tunnel** interface type to create tunnel interfaces on various devices, and manage IP addressing on DMVPN and IPsec tunnels:

```
links:
- hub1:
  spoke1:
  spoke2:
  type: tunnel
  prefix: 192.168.1.0/24
- hub2:
  spoke1:
  spoke2:
  type: tunnel
  prefix: 192.168.2.0/24
- iotprovider:
  firewall:
  type: tunnel
  prefix: 10.10.0.0/30
```

The tunnel links result in tunnel interfaces with configuration parameters supported by _netlab_ (IP addresses, OSPF routing...). You have to use custom configuration templates to configure the tunnel parameters. Here's how Anne configured DMVPN tunnel parameters in his spoke configuration template (slightly edited for clarity):

```
{% for intf in interfaces if intf.type == "tunnel" %}
interface {{ intf.ifname }}
 description DMVPN Tunnel
 ip mtu 1400
{%   for i in intf.neighbors %}
{%     if i.node is regex('hub.*$') %}
 ip nhrp authentication {{ dmvpn.nhrp_keys[i.node] }}
 ip nhrp nhs {{ i.ipv4|ipaddr('address') }}
 ip nhrp network-id 1
 ip nhrp map multicast {{ i.ipv4|ipaddr('address') }}
...
{%       for intunderlay in hostvars['firewall'].interfaces 
           if intunderlay.type is defined
             and intunderlay.type == "lan" %}
{%         for j in intunderlay.neighbors if j.node == i.node %}
 ip nhrp map {{ i.ipv4|ipaddr('address') }} {{ j.ipv4|ipaddr('address') }} 
 tunnel destination {{ j.ipv4|ipaddr('address') }}
{%         endfor %}
{%       endfor %}
{%     endif %}
{%   endfor %}
 ip nhrp map multicast dynamic
 ip tcp adjust-mss 1360
 keepalive 5 10
 tunnel path-mtu-discovery
!
{% endfor %}
```

Translated into English:

* Iterate over all spoke interfaces and find tunnel interfaces
* For every tunnel interface, configure MTU and a few other parameters
* Iterate over neighbors reachable over the tunnel interface.
* If a neighbor is a hub[^AGM], configure NHRP authentication using the hub-specific DMVPN key and NHRP server using the hub tunnel IP address
* Next, find the WAN interface of the hub router.

[^AGM]: I would use Ansible group membership check like `i.node in groups.hubs` instead of a regular expression.

{{<note>}}This is where Anne's template becomes convoluted. I would use link **role** attribute to identify WAN links and match on those.{{</note>}}

* Configure NHRP map and tunnel destination using the IP address of the hub's WAN interface.

For more details, explore the [netlab examples GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/DMVPN), and once you decide to give _netlab_ a try, start with the [installation guide](https://netlab.tools/install/) and [getting started](https://netlab.tools/tutorials/) tutorial.
