---
kb_section: DataModels
minimal_sidebar: true
title: Removing Duplicate Data
url: /kb/DataModels/10-Removing Duplicate Data/
pre_scroll: true
---
I started this article with a typical first attempt at describing a leaf-and-spine fabric using BGP as the routing protocol. Before moving on, make sure you [understand the original data model](/kb/DataModels/). Now let's see how we can reduce the amount of duplicate data.

## Removing Duplicate AS Numbers

Assuming we’re designing a reasonable EBGP-based fabric (as opposed to [IBGP-over-EBGP monstrosity](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics#IBGP-Based_EVPN_on_Top_of_EBGP-Based_Fabric_Routing) with [**neighbor local-as** cheating all over the place](/2018/05/dissecting-ibgpebgp-junos-configuration/)) each switch in the fabric has a single AS number.

Specifying AS numbers for the BGP peers is thus unnecessary - all you need to do is to specify the peer name and look up the AS number specified in the peer data structure when creating BGP configuration.

{{<cc>}}Data structure describing S1 interfaces and BGP neighbors{{</cc>}}

    ---
    hostname: S1
    bgp_as: 65001
    interfaces:
    - name: GigabitEthernet0/1
      ip: 172.16.0.1/30
    - name: Vlan101
      ip: 192.168.1.1/24
    !
    neighbors:
    - ip: 172.16.0.2
      name: S2

{{<cc>}}Data structure describing S2 interfaces and BGP neighbors{{</cc>}}

    hostname: S2
    bgp_as: 65002
    interfaces:
    - name: GigabitEthernet0/1
      ip: 172.16.0.2/30
    - name: Vlan101
      ip: 192.168.2.1/24
    !
    neighbors:
    - ip: 172.16.0.1
      name: S1


Making just that one change, we already reduced the amount of duplicate data in our data model. However, no good deed ever goes unpunished. We have to compensate reduced data model complexity with increased template complexity:

{{<cc>}}Generating BGP neighbors from partially-deduplicated data model{{</cc>}}

    router bgp {{ bgp_as }}
    {% for n in neighbors %}
     neighbor {{ n.ip }} remote-as {{ hostvars[n.name].bgp_as }}
     neighbor {{ n.ip }} description {{ n.name }}
    {% endfor %}

On the other hand, having explicit neighbor information (instead of neighbor IP address and AS number) in the data model allows us to generate neighbor descriptions. Getting BGP neighbor name in the [old data model](/kb/DataModels/) where all we had were neighbor IP addresses would require interestingly-complex lookup code.

## Removing Peer IP Addresses

Our data model still contains a significant amount of duplicate data. For example, every IP address appears twice - once as the IP address of an interface, the second time as the IP address of a BGP peer.

Could we eliminate duplicate IP address information? How about replacing peer IP addresses with peer interface names, and looking up peer IP addresses when building BGP configuration?

{{<cc>}}Minimal data structure describing S1 interfaces and BGP neighbors{{</cc>}}

    ---
    hostname: S1
    bgp_as: 65001
    interfaces:
      GigabitEthernet0/1:
        ip: 172.16.0.1/30
      Vlan101:
        ip: 192.168.1.1/24

    neighbors:
    - name: S2
      interface: GigabitEthernet0/1

{{<cc>}}Minimal data structure describing S2 interfaces and BGP neighbors{{</cc>}}

    ---
    hostname: S2
    bgp_as: 65002
    interfaces:
      GigabitEthernet0/1:
        ip: 172.16.0.2/30
      Vlan101:
        ip: 192.168.2.1/24

    neighbors:
    - name: S1
      interface: GigabitEthernet0/1

{{<note info>}}I restructured the *interfaces* list into a dictionary to simplify lookups based on interface names. While Jinja2 provides filters that perform lookups in lists they usually result in messy templates, so it's better to restructure input data (assuming you can do it).{{</note>}}

This data model has a few unexpected benefits:

* Connectivity between node is specified explicitly (peer name + interface) instead of being implicitly encoded into IP addresses (hoping you got the subnets right);
* Explicit connectivity allows you to do easy wiring validation: does LLDP neighbor name/interface match the neighbor/interface specified in the data model?
* It’s also pretty easy to check whether we used matching subnet on both ends of the link.

{{<note note>}}A careful reader might notice that we could get rid of IP addresses in the data model and compute them on-the-fly.{{</note>}}

Not surprisingly, the lookups needed to get BGP neighbor IP address got even more complicated:

{{<cc>}}Generating BGP neighbors from fully-deduplicated data model{{</cc>}}

    router bgp {{ bgp_as }}
    {% for n in neighbors %}
    {% set n_ip = hostvars[n.name].interfaces[n.interface].ip|ipaddr('address') %}
     neighbor {{ n_ip }} remote-as {{ hostvars[n.name].bgp_as }}
     neighbor {{ n_ip }} description {{ n.name }}
    {% endfor %}

Is data deduplication worth the increase in template complexity? As always, it depends, this time on how often you change the data describing your network versus how often you expect to change configuration templates. In most environments, data changes way more often than configuration templates.
