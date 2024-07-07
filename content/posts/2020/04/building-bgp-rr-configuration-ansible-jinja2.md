---
title: "Building BGP Route Reflector Configuration with Ansible/Jinja2"
date: 2020-04-08 06:57:00
tags: [ Ansible, BGP, automation ]
---
One of our subscribers sent me this email when trying to use ideas from [Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers) webinar to build BGP route reflector configuration:

> I'm currently discovering Ansible/Jinja2 and trying to create BGP route reflector configuration from Jinja2 template using Ansible playbook. As part of **group\_vars** YAML file, I wish to list all route reflector clients IP address. When I have 50+ neighbors, the YAML file gets quite unreadable and it's hard to see data model anymore.

Whenever you hit a roadblock like this one, you should start with the bigger picture and maybe redefine the problem.
<!--more-->
In this particular case, your problem shouldn't be "*I want to configure BGP neighbors on my route reflector*" but "*I want to configure IBGP sessions in my network*" or even “*want to configure BGP routing in my network*”. With this scope in mind:

* Create an inventory file listing all BGP routers in your network (you'll need it anyway), preferably in YAML format.
* Define loopback IP address for every router. You could define them in the inventory file, in **host\_vars** if you need per-host variables for some other reason, or in an external file that you'll include with **include\_vars**.
* Group RR clients. You could use Ansible groups, or list them somewhere in a YAML file, or add a variable like **rr_group** to every RR client host.

{{<note>}}Ansible calls variables _facts_ just to confuse people with a bit of programming background.{{</note>}}

Whatever you do, make sure you don’t have the same information (like router loopback IP) stored in multiple places. You want to have a **single** [source of truth](/2019/02/building-network-automation-source-of/) for every bit of information, or as [Elisa Jasinska](https://www.ipspace.net/Author:Elisa_Jasinska) explained in [her presentation in Building Network Automation Solutions](https://my.ipspace.net/bin/list?id=NetAutSol&module=1#M1S3) online course: “*duplicate data makes rockets explode*”

Let's assume that after you're done your data model looks like this:

* BGP Route Reflector clients are in **rr\_clients** Ansible group;
* Each router has its loopback IP defined in **loopback\_ip** variable;
* There's a global variable **bgp\_as** defined in **all.yml** group variable file.

Furthermore, to simplify the example, assume you have a single route reflector cluster in your autonomous system.

Using that data model, it's easy to build the route reflector BGP configuration with a Jinja2 template:

* Iterate over all hosts in specified group
* For every host fetch the loopback IP to create the neighbor statement.

Here's the relevant part of a Jinja2 template:

```
{% for bgp_node in groups['rr_clients'] %}
neighbor {{ hostvars[bgp_node].loopback_ip }} remote-as {{ bgp_as }}
{% endfor %}
```

You can use the same trick on the RR client side to create a list of IBGP sessions to all route reflectors in your network, and on the reflectors to create a full mesh of IBGP sessions between reflectors.

## More examples

* I did something very similar in [MPLS Infrastructure](https://github.com/ipspace/mpls-infrastructure) example, but using a slightly different data structure and a data model transformation.
* Explore another [data model transformation example](/kb/DataModels/)
