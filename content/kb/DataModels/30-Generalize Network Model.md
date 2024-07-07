---
kb_section: DataModels
minimal_sidebar: true
title: Generalize the Network Data Model
url: /kb/DataModels/30-Generalize Network Model/
pre_scroll: true
---
After starting with [simplistic data model full of duplicate data](index.html), [removing duplicate data](10-Removing%20Duplicate%20Data.html), and [restructuring the data model into a network-focused one](20-Restructure.html) we're pretty close to an ideal solution. The only thing that still annoys me is the *left* and *right* part of an edge (link). In an undirected graph, we shouldn’t differentiate between the two ends of a connection. Furthermore, our data model can’t cope with rare multi-access links we might still find in real-life networks (examples: Carrier Ethernet E-LAN, DMVPN tunnels, wireless...).

{{<note note>}}At this point, we’re slightly diverging from “*network is a graph*” paradigm. Modeling multi-access network as a graph requires an extra node representing the network... in case you ever wondered why OSPF needs type-2 LSAs ;){{</note>}}

We can solve both challenges by replacing the left/right attributes of a link with a dictionary of nodes. Our revised data model would look like this:

{{<cc>}}Data structure describing all links in our fabric{{</cc>}}

    links:
    #
    # Core link connecting S1 and S2
    #
    - S1:
        GigabitEthernet0/1: 172.16.0.1/30
      S2:
        GigabitEthernet0/1: 172.16.0.2/30

    #
    # Edge (stub) links on S1 and S2
    #
    - S1:
        Vlan101: 192.168.1.1/24
    - S2:
        Vlan101: 192.168.2.1/24

Not only have we made our data model cleaner, but it also allows us to express corner cases like:

* **multi-access interfaces**: a dictionary of nodes has more than two elements;
* **stub interfaces**: a dictionary of nodes has just one element.

The only parameters left in the per-node **host_vars** files would be the node name and the AS number.

{{<cc>}}Host variables for S1{{</cc>}}

    ---
    hostname: S1
    bgp_as: 65001

## Generating Configuration from Revised Data Model

Revised data model uses the same data structure for point-to-point and multi-access transit links as well as stub interfaces, resulting in simpler Jinja2 templates. All we have to do is to traverse the whole data structure:

* Iterate over all links
* Iterate over all nodes within a link data structure and perform some action when encountering the local node name
* Iterate over all interfaces within the local node name

Here's the part of the Jinja2 template that generates interface configuration:

    {% macro interface(name,addr) -%}
    !
    interface {{ name }}
     ip address {{ addr|ipaddr('address') }} {{ addr|ipaddr('netmask') }}
    {%- endmacro %}
    {#
      Interfaces
    #}
    {% for link in links %}
    {%   for node,iflist in link|dictsort if node == inventory_hostname %}
    {%     for ifname,ip in iflist|dictsort %}
    {{ interface(ifname,ip) }}
    {%     endfor %}
    {%   endfor %}
    {% endfor %}

The template generating BGP **network** statements is almost identical to the interface code. All we need is an additional check: we need the **network** statements only for links that have a single node:

    router bgp {{ bgp_as }}
    ...
    {% for link in links if link|length == 1 %}
    {% for node,iflist in link|dictsort if node == inventory_hostname %}
    {% for ifname,ip in iflist|dictsort %}
     network {{ ip|ipaddr('network') }} {{ ip|ipaddr('netmask') }}
    {% endfor %}
    {% endfor %}
    {% endfor %}

The BGP **neighbor** template is a bit more convoluted: we have to check whether the link is connected to the local node, and create **neighbor** statements for all other nodes connected to the same subnet:

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
    {% for node,iflist in link|dictsort if node != inventory_hostname %}
    {% for ifname,ip in iflist|dictsort %}
    {{ neighbor(node,ip) }}
    {% endfor %}
    {% endfor %}
    {% endfor %}

Not too bad, right? Can we do better? How about getting rid of IP addresses? You might want to try to do that step yourself before moving on.
