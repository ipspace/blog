---
kb_section: DataModels
minimal_sidebar: true
title: Replace IP Addresses with Per-Link Prefixes
url: /kb/DataModels/40-Link Prefixes/
pre_scroll: true
---
We got very far from the [initial simplistic data model full of duplicate data](/kb/DataModels/): we [removed duplicate data](/kb/DataModels/10-Removing%20Duplicate%20Data/), [restructured the data model into a network-focused one](/kb/DataModels/20-Restructure/), and [optimized data structure to represent stub, P2P and multi-access links](/kb/DataModels/30-Generalize%20Network%20Model/). However, there's still a hidden redundancy in our data model. Consider the following bit of our data model describing a single P2P link:

{{<cc>}}Can you spot the redundancy in the data structure describing a single P2P link?{{</cc>}}

    - S1:
        GigabitEthernet0/1: 172.16.0.1/30
      S2:
        GigabitEthernet0/1: 172.16.0.2/30

The data structure defines two IP addresses which (usually) have to belong to the same prefix and have the same subnet mask (or we'd make some routing protocols extremely unhappy). It might make sense to make the IP prefix a property of the link (subnet) and number interfaces automatically using a data structure similar to this one:

{{<cc>}}Making the subnet prefix a link attribute{{</cc>}}

    - prefix: 172.16.0.0/30
      nodes:
        S1:
          GigabitEthernet0/1:
        S2:
          GigabitEthernet0/1:

The above data structure is optimal from the programming perspective:

* Nodes are just an attribute of the link, making it easier to extend link attributes
* Node interfaces are still a dictionary, allowing us to add interface attributes if needed

It's also quite counter-intuitive which makes it prone to operator errors, so you might want to consider an alternate representation along these lines that is easier to understand but harder to work with.

{{<cc>}}This data model might be easier to grasp{{</cc>}}

    - prefix: 172.16.0.0/30
      S1: GigabitEthernet0/1
      S2: GigabitEthernet0/1

As a punishment for discussing the additional complexity we'll use the second data model in Jinja2 templates... and considering that the prior definition of edge links was pretty handy, we'll keep supporting both data representations.

{{<cc>}}Edge link representation{{</cc>}}

    - S1:
        Vlan101: 192.168.1.1/24

## Generating Node IP Addresses

We did most of the hard work in the previous step where we defined the **interface** and **neighbor** macros, so our Jinja2 template needs just a few small adjustments to cope with the new data structures... but we'll nonetheless split it into two parts to make troubleshooting easier. The master template will be nothing more than a framework including interface- and BGP templates:

{{<cc>}}Master configuration template{{</cc>}}

    hostname {{ hostname }}
    !
    {% include 'interfaces.j2' %}
    !
    {% include 'bgp.j2' %}

The interface configuration template loops across the **links** dictionary and uses a slightly different logic using **ipaddr** filter to generate node IP addresses whenever the link has **prefix** attribute:

{{<cc>}}Generating interface configuration{{</cc>}}

    {#
      Interface macro
    #}
    {% macro interface(name,addr) -%}
    !
    interface {{ name }}
     ip address {{ addr|ipaddr('address') }} {{ addr|ipaddr('netmask') }}
    {%- endmacro %}
    {#
      Interfaces
    #}
    {% for link in links %}
    {%   for node,iflist in link|dictsort if node != 'prefix' %}
    {%     if node == inventory_hostname %}
    {%       if link.prefix is defined %}
    {{         interface(iflist,link.prefix|ipaddr(loop.index)) }}
    {%       else %}
    {%         for ifname,ip in iflist|dictsort %}
    {{           interface(ifname,ip) }}
    {%         endfor %}
    {%       endif %}
    {%     endif %}
    {%   endfor %}
    {% endfor %}

Likewise, the BGP template creates **neighbor** statements whenever a link has more than one attribute (skipping **prefix** attribute), and a **network** statement for edge links with a single attribute (node name):

    {#
      BGP neighbor macro
    #}
    {% macro neighbor(name,ip) -%}
    {% set n_ip = ip|ipaddr('address') %}
     neighbor {{ n_ip }} remote-as {{ hostvars[name].bgp_as }}
     neighbor {{ n_ip }} description {{ name }}
    {%- endmacro %}
    {#
      BGP routing protocol configuration
    #}
    router bgp {{ bgp_as }}
    {#
      BGP neighbors - find links that contain local nodename and create
      neighbors for all other nodenames
    #}
    {% for link in links if link|length > 1 and inventory_hostname in link.keys() %}
    {%   for node,ifname in link|dictsort if node != 'prefix' %}
    {%     if node != inventory_hostname %}
    {{       neighbor(node,link.prefix|ipaddr(loop.index)) }}
    {%     endif %}
    {%   endfor %}
    {% endfor %}
    !
    {% for link in links if link|length == 1 %}
    {%   for node,iflist in link|dictsort if node == inventory_hostname %}
    {%     for ifname,ip in iflist|dictsort %}
     network {{ ip|ipaddr('network') }} {{ ip|ipaddr('netmask') }}
    {%     endfor %}
    {%   endfor %}
    {% endfor %}

Can we do even better than this? Of course - we could automatically assign prefixes for core subnets and node IP addresses from a larger IP prefix. The last optimization step is left as an exercise for the reader.
