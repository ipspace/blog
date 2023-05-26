---
kb_section: DataModels
minimal_sidebar: true
pre_scroll: true
title: Data Transformation Example
url: /kb/DataModels/66-Transformation-Example.html
---
Let's illustrate the data transformation concepts with a simple example: we'll transform our [highly optimized data model with automatic IP address allocation](40-Link%20Prefixes.html) into a set of device-level data models [identical to what we started with](index.html). Our transformation should take data describing nodes and links...

{{<cc>}}Data structure describing routers, links, and stub VLAN interfaces{{</cc>}}
```
nodes:
  S1:
    bgp_as: 65001
  S2:
    bgp_as: 65002

links:
# Core links
#
- prefix: 172.16.0.0/30
  S1: GigabitEthernet0/1
  S2: GigabitEthernet0/1
#
# Edge links
#
- S1:
    Vlan101: 192.168.1.1/24
- S2:
    Vlan101: 192.168.2.1/24
```

...and generate device-level data describing device attributes (BGP AS number), interfaces, and IP addresses:

{{<cc>}}Data structure describing an individual device{{</cc>}}
```
---
hostname: S1
bgp_as: 65001
interfaces:
- name: GigabitEthernet0/1
  ip: 172.16.0.1/30
- name: Vlan101
  ip: 192.168.1.1/24

neighbors:
- ip: 172.16.0.2
  bgp_as: 65002
```

The transformation rules are pretty simple (after all, we're working with a proof-of-concept-level example):

---

For every key in the **nodes** dictionary create a YAML file with the following data:
  
* **hostname** is set to the dictionary key
* **bgp_as** is set to the **bgp_as** value.

Iterating through **links** dictionary, whenever you find an element with a single dictionary key equal to current device name, it's a stub interface:

* Add an element to **interfaces** list. **name** attribute is set to the key of the child dictionary, **ip** attribute is set to its value.

Iterating through **links** dictionary, whenever you find an element with more than one key, it must be a router-to-router link:
  
* From the alphabetic order of devices connected to the link find the host portion of the IP address of the current device
* Add an element to **interfaces** list. **name** attribute is set to the dictionary value (interface name), **ip** address is set to the **prefix** plus per-link device ID.

Repeat the iteration through **links** dictionary, and whenever you find an element with more than one key, add BGP neighbor information:
  
* Take **bgp_as** value from neighbor's data
* Calculate the neighbor's IP address on the link and use it as **ip** value.

---

Not surprisingly, the logic is almost exactly the same as [what we used to create device configurations](40-Link%20Prefixes.html#generatingnodeipaddresses).

## Jinja2 Transformation Template

Creating a [Jinja2 transformation template](https://github.com/ipspace/ansible-examples/blob/master/Data-Models/Transformation/device-data.j2) was surprisingly easy &ndash; I started with the template used to create device configurations from the [final data model](40-Link%20Prefixes.html) as it already contained the necessary business logic, and changed its output from device configuration statements to YAML elements:

{{<cc>}}Data Transformation Template{{</cc>}}
```
{#
  Jinja2 macros to create interface- and BGP neighbor data structure.
  Be very careful about proper indentation - it's YAML after all.
#}
{% macro interface(name,addr) -%}
- name: {{ name }}
  ip: {{ addr }}
{%- endmacro %}
{% macro neighbor(name,ip) -%}
- bgp_as: {{ nodes[name].bgp_as }}
  ip: {{ ip|ipaddr('address') }}
{%- endmacro %}
#
# host_vars data for {{ hostname }} generated from network device data model
#
---
hostname: {{ hostname }}
bgp_as: {{ nodes[hostname].bgp_as }}

interfaces:
{% for link in links %}
{%   for node,iflist in link|dictsort if node != 'prefix' %}
{%     if node == hostname %}
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

neighbors:
{% for link in links if link|length > 1 and hostname in link.keys() %}
{%   for node,ifname in link|dictsort if node != 'prefix' %}
{%     if node != hostname %}
{{       neighbor(node,link.prefix|ipaddr(loop.index)) }}
{%     endif %}
{%   endfor %}
{% endfor %}
```

I also created a [simple template](https://github.com/ipspace/ansible-examples/blob/master/Data-Models/Transformation/inventory.j2) that would generate a skeleton Ansible inventory in YAML format:

{{<cc>}}Creating skeleton Ansible inventory from **nodes** element in the network data model{{</cc>}}
```
# Ansible inventory generated from network data model
#
---
all:
  hosts:
{% for hostname in nodes.keys() %}
    {{ hostname }}:
{% endfor %}
```

Finally, we need a [playbook](https://github.com/ipspace/ansible-examples/blob/master/Data-Models/Transformation/transform-data.yml) that would read the network data model and create device data as individual YAML files in **host_vars** directory:

{{<cc>}}Ansible playbook that generates Ansible inventory and device data{{</cc>}}
```
#!/usr/bin/env ansible-playbook
#
---
- name: Transform network data model into device data model(s)
  hosts: localhost
  tasks:
  - name: Read network data model
    include_vars: network.yml
  - name: Create per-device data model(s)
    template:
      src: device-data.j2
      dest: host_vars/{{ hostname }}.yml
    loop: "{{ nodes.keys() }}"
    loop_control:
      loop_var: hostname
  - name: Create Ansible inventory
    template:
      src: inventory.j2
      dest: hosts.yml
```

You could run that playbook every time you want to create device configurations, whenever new commit is merged into the master branch (as part of CI or CD pipeline), or as part of a *makefile* that would generate device configurations. Here's a sample **Makefile** that gets the job done (probably not in an optimal way):

{{<cc>}}This Makefile generates device configurations whenever the high-level data model changes{{</cc>}}
```
configs/%.cfg: host_vars/%.yml hosts.yml
	ansible-playbook -i hosts.yml create-configs.yml
	touch $@

hosts.yml: network.yml
	ansible-playbook transform-data.yml
	touch $@
```

**Notes:**

* As [stated previously](65-Data-Transformation.html#datatransformationimplementationoptions), using Ansible to perform data model manipulation is not always a good idea.
* It's almost always easier to write a Python program to transform the data than trying to get it done with a Jinja2 template.
* You don't need an Ansible playbook to use Jinja2 templates, but it's definitely a convenient way of using them.

## Transformation Results

The end result is exactly what we need: Ansible inventory in YAML format...

{{<cc>}}Skeleton Ansible inventory generated from network data model{{</cc>}}
```
# Ansible inventory generated from network data model
#
---
all:
  hosts:
    S1:
    S2:
```

...and device-level data for individual BGP speakers stored in **host_vars** directory:

{{<cc>}}Device-level data for S1{{</cc>}}
```
#
# host_vars data for S1 generated from network device data model
#
---
hostname: S1
bgp_as: 65001
interfaces:
- name: GigabitEthernet0/1
  ip: 172.16.0.1/30
- name: Vlan101
  ip: 192.168.1.1/24
neighbors:
- bgp_as: 65002
  ip: 172.16.0.2
```

Once we have the device-level data, we can use the templates from the [initial solution](index.html) to create device configurations.

<!-- need a comment -->
