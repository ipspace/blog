title: Network Automation Data Model Optimization
index: yes
toc_title: Introduction
publish: 2019-05-10

One of the toughest challenges in the hands-on part of [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course is the [create a data model describing your service](https://my.ipspace.net/bin/list?id=NetAutSol&module=3#M3S6) exercise. Networking engineers never had to think about data models describing their networks or services, data deduplication, or normalized data structures, and the first attempt often results in something that looks like simplified device configuration in YAML or JSON format.

A very typical scenario models a leaf-and-spine fabric using BGP as a routing protocol. We’ll be using Ansible as tool-of-choice throughout this article because it’s usually easier to master than a full-blown programming language, and the way Ansible inventory is structured usually nudges the engineer solving the challenge into this approach:

* We’ll describe the leaf-and-spine fabric using node (device) attributes;
* Device attributes will be stored in YAML files in host_vars directory.

## Initial Device-Focused Data Model

This is how you could describe a two-switch fabric using BGP on a single interface connecting them:

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

CAPTION: Data structure describing S1 in host_vars/S1.yml

    hostname: S2
    bgp_as: 65002
    interfaces:
    - name: GigabitEthernet0/1
      ip: 172.16.0.2/30
    - name: Vlan101
      ip: 192.168.2.1/24

    neighbors:
    - ip: 172.16.0.1
      bgp_as: 65001

CAPTION: Data structure describing S2 in host_vars/S2.yml

Having a data model that closely matches target device configuration results in a very simple configuration template:

    hostname {{ hostname }}
    {% for intf in interfaces %}
    !
    interface {{ intf.name }}
     ip address {{ intf.ip|ipaddr('address') }} {{ intf.ip|ipaddr('netmask') }}
    {% endfor %}
    !
    router bgp {{ bgp_as }}
    {% for n in neighbors %}
     neighbor {{ n.ip }} remote-as {{ n.bgp_as }}
    {% endfor %}
    {% for intf in interfaces if 'Vlan' in intf.name %}
     network {{ intf.ip|ipaddr('network') }} {{ intf.ip|ipaddr('netmask') }}
    {% endfor %}

CAPTION: Jinja2 template used to create interface and BGP configuration

## Duplicate Data in the Initial Data Model

There are a few things obviously wrong with our initial data model:

* Every IP address is specified in two places (as an IP address of an interface, and as a BGP peer IP address) in two different files;
* Every AS number is specified at least twice (in node definition and in peer BGP AS number) in at least two different files;
* Since copies of the same value are stored in different files, it's almost certain that after a while someone will change one of them but not the other.

As Elisa Jasinska loved to say in her *[Design Your Network Automation Systems](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S3)* presentation in the [Getting Started](https://my.ipspace.net/bin/list?id=NetAutSol&module=1) module of our [network automation course](https://www.ipspace.net/Building_Network_Automation_Solutions): “*data duplication makes rockets explode*”

NOTE: It was really [code reuse from an older version](https://around.com/ariane.html) not data duplication but the statement does sound great.

Now what? First rule: don’t panic. As Frederick Brooks explained in The Mythical Man-Month: “*the first system will fail. It’s just a question whether someone promised it to the customer*”... or as Ron Broersma usually says when talking about IPv6 addressing plans: “*Don’t waste time on your first IPv6 addressing plan. You’ll get it wrong no matter what.*”

Fortunately we’re not the first ones dealing with data deduplication. Whole books have been written on database normalization, and while the relational database concepts might not apply directly to our data models, the generic ideas still hold true.

## Exercise

Before moving on, try to reduce or eliminate duplicate data from the above data model.