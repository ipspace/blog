---
kb_section: DataModels
minimal_sidebar: true
title: Nodes-and-Links Data Model
url: /kb/DataModels/20-Restructure.html
pre_scroll: true
---
[After rigorous deduplication](10-Removing%20Duplicate%20Data.html) we got a pretty clean data model, but still has a significant drawback: it's not the best representation of reality.

Based on our history of dealing with independent device configurations we usually model our networks as a set of nodes with interfaces. In reality, networks are *graphs* with nodes and edges (and interfaces happen to connect the two).

How about restructuring our data model into a set of nodes and links? Here’s the first attempt in which we'll keep the stub (VLAN) interfaces tied to individual nodes and describe the core links as graph edges:

{{<cc>}}Data structure describing S1 attributes and stub interfaces{{</cc>}}

    ---
    hostname: S1
    bgp_as: 65001
    interfaces:
      Vlan101:
        ip: 192.168.1.1/24

{{<cc>}}Data structure describing S2 attributes and stub interfaces{{</cc>}}

    ---
    hostname: S2
    bgp_as: 65002
    interfaces:
      Vlan101:
        ip: 192.168.2.1/24

{{<cc>}}Data structure describing core link(s) in our network{{</cc>}}

    links:
    - left_node: S1
      left_interface: GigabitEthernet0/1
      left_ip: 172.16.0.1/30
      right_node: S2
      right_interface: GigabitEthernet0/1
      right_ip: 172.16.0.2/30

{{<note note>}}You can store this data structure in *group_vars/all.yml* or in a separate YAML file included in an Ansible playbook with **include_vars** module. Sample playbooks use the latter approach.{{</note>}}

All of a sudden, the network topology becomes explicit, and we can use it to test all sorts of things, from correct wiring to BGP sessions. On the other hand, the configuration templates become extremely convoluted because we always have to deal with three scenarios:

* Stub interfaces (listed in data structure describing nodes)
* Left node of a link
* Right node of a link

For example, this is Jinja2 code dealing with interface configurations:

{{<cc>}}Generating interface configuration from stub interfaces and network links{{</cc>}}

    {# stub interfaces #}
    {% for ifname,ifdata in interfaces|dictsort %}
    !
    interface {{ ifname }}
     ip address {{ ifdata.ip|ipaddr('address') }} {{ ifdata.ip|ipaddr('netmask') }}
    {% endfor %}
    {# nodes on the left side of a link #}
    {% for link in links if link.left_node == inventory_hostname %}
    !
    interface {{ link.left_interface }}
     ip address {{ link.left_ip|ipaddr('address') }} {{ link.left_ip|ipaddr('netmask') }}
    {% endfor %}
    {# nodes on the right side of a link #}
    {% for link in links if link.right_node == inventory_hostname %}
    !
    interface {{ link.right_interface }}
     ip address {{ link.right_ip|ipaddr('address') }} {{ link.right_ip|ipaddr('netmask') }}
    {% endfor %}

Likewise, we have to deal with *left* and *right* nodes when generating BGP neighbor configuration:

{{<cc>}}Generating BGP neighbor configuration network links{{</cc>}}

    router bgp {{ bgp_as }}
    {# nodes on the left side of a link #}
    {% for link in links if link.left_node == inventory_hostname %}
    {% set neighbor = link.right_node %}
    {% set n_ip = link.right_ip|ipaddr('address') %}
     neighbor {{ n_ip }} remote-as {{ hostvars[neighbor].bgp_as }}
     neighbor {{ n_ip }} description {{ neighbor }}
    {% endfor %}
    {# nodes on the right side of a link #}
    {% for link in links if link.right_node == inventory_hostname %}
    {% set neighbor = link.left_node %}
    {% set n_ip = link.left_ip|ipaddr('address') %}
     neighbor {{ n_ip }} remote-as {{ hostvars[neighbor].bgp_as }}
     neighbor {{ n_ip }} description {{ neighbor }}
    {% endfor %}

{{<cc>}}Generating BGP network statements from stub interfaces{{</cc>}}

    router bgp {{ bgp_as }}
    ...
    !
    {# stub interfaces #}
    {% for ifname,ifdata in interfaces|dictsort %}
     network {{ ifdata.ip|ipaddr('network') }} {{ ifdata.ip|ipaddr('netmask') }}
    {% endfor %}

Net result: removing redundant data from the data model forced us to use multiple almost-identical configuration blocks in configuration templates. Even worse, because the configuration blocks dealing with *left* and *right* side of the link aren't identical, we're even likelier to make errors when adjusting or adding configuration commands to the templates. On the positive side, the data model clearly differentiates between core links and stub interfaces, so we no longer have to check the interface name when generating **network** configuration commands.

Programmers learned how to deal with this type of redundancy ages ago by using subroutines, functions, or macros (depending on your programming language features and terminology). Jinja2 calls them *macros* and using them makes our configuration template more consistent although we still have to think about *left* and *right* side of point-to-point links. Here's the revised interface configuration template:

{{<cc>}}Generating interface configuration using Jinja2 macros{{</cc>}}

    {#
      Interface macro
    #}
    {% macro interface(name,addr) -%}
    !
    interface {{ name }}
     ip address {{ addr|ipaddr('address') }} {{ addr|ipaddr('netmask') }}
    {%- endmacro %}
    {#
      Stub interfaces
    #}
    {% for ifname,ifdata in interfaces|dictsort %}
    {{ interface(ifname,ifdata.ip) }}
    {% endfor %}
    {#
      Nodes on the left side of links
    #}
    {% for link in links if link.left_node == inventory_hostname %}
    {{ interface(link.left_interface,link.left_ip) }}
    {% endfor %}
    {#
      Nodes on the right side of links
    #}
    {% for link in links if link.right_node == inventory_hostname %}
    {{ interface(link.right_interface,link.right_ip) }}
    {% endfor %}

And here's the revised BGP configuration template:

{{<cc>}}Generating BGP neighbor configuration using Jinja2 macros{{</cc>}}

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
      Nodes on the left side of links
    #}
    {% for link in links if link.left_node == inventory_hostname %}
    {{ neighbor(link.right_node,link.right_ip) }}
    {% endfor %}
    {#
      Nodes on the right side of links
    #}
    {% for link in links if link.right_node == inventory_hostname %}
    {{ neighbor(link.left_node,link.left_ip) }}
    {% endfor %}

Can we do any better? Can we get rid of *left* and *right* side of a link? Try to figure it out before moving on.
