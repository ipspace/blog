---
title: "Beware: Ansible Reorders List Values in Loops"
date: 2022-03-24 07:27:00
tags: [ Ansible ]
pre_scroll: True
---
**TL&DR**: Ansible might decide to reorder list values in a **loop** parameter, resulting in unexpected order of execution and (in my case) totally borked device configuration.

A bit of a background first: I'm using an Ansible playbook within *[netsim-tools](https://netsim-tools.readthedocs.io/en/latest/)* to deploy [initial device configurations](https://netsim-tools.readthedocs.io/en/latest/netlab/initial.html). Among other things, that playbook deploys configuration snippets for [numerous configuration modules](https://netsim-tools.readthedocs.io/en/latest/modules.html), and the order of deployment is absolutely crucial. For example, you cannot activate BGP neighbors in Labeled Unicast (BGP-LU) address family (**mpls** module) before configuring BGP neighbors (**bgp** module).
<!--more-->
To make the ordered deployment of configuration snippets work, every *host* (Ansible term for *managed device*) has a list of modules in the **module** fact (Ansible term for *variable*) in its *host_vars*. For example, these are the values of the **module** fact for all devices in the [BGP-LU lab](https://github.com/ipspace/netsim-examples/tree/master/MPLS/ldp-bgp-lu):

```
pe1:
  module: [ ospf, bgp, mpls ]
pe2:
  module: [ ospf, bgp, mpls ]
p:
  module: [ ospf, mpls ]
rr:
  module: [ ospf, bgp, mpls ]
ce1:
  module: [ bgp, mpls ]
ce2:
  module: [ bgp, mpls ]
```

The **module** variable is used in an Ansible play to include a *deploy module* task list (which then includes device-and-module-specific tasks) for each module used by a network device :

```
- name: Deploy module-specific configurations
  hosts: all
  tasks:
  - include_tasks: "tasks/deploy-module.yml"
    tags: [ module,test ]
    loop: "{{ module | default([]) }}"
    loop_control:
      loop_var: config_module
    when: module is defined and (not(modlist is defined) or config_module in modlist)
```

The convoluted `when` condition is used to:

* Ensure the task is not executed for devices that do not have optional configuration modules
* Deploy a subset of configuration modules specified in an optional `modlist` fact (set with `-e` CLI parameter).

Looking at that code, one would assume the modules will be deployed in the order they are listed in the **module** variable, right? Tough luck, this is what happens (tested with various Ansible versions between 2.9 and 5.5):

```
TASK [include_tasks] ***************************************************************************************************************
included: /home/pipi/net101/tools/netsim/ansible/tasks/deploy-module.yml for p, pe1, pe2, rr => (item=ospf)
included: /home/pipi/net101/tools/netsim/ansible/tasks/deploy-module.yml for p, pe1, pe2, rr, ce1 => (item=mpls)
included: /home/pipi/net101/tools/netsim/ansible/tasks/deploy-module.yml for pe1, pe2, rr, ce1 => (item=bgp)

```

The first device in the batch has **module** set to `[ ospf, mpls ]`, and it looks like Ansible in its infinite optimization wisdom decides it's OK to use the same order for all other devices in the same batch. Even though PE1 (for example) has **module** set to `[ ospf, bgp, mpls ]`, the actual order of execution is `ospf, mpls, bgp`, and the BGP neighbors are never activated in the BGP-LU address family because they configuration snippets try to activate them before they are defined.

The only workaround I could find was to set **serial** (batch size) to one[^FREE] to deploy configurations on a single device at a time (so Ansible has nothing to optimize). It works, but it also makes lab deployment way slower than it should have been.

Maybe I made a wrong choice and shouldn't use something that thinks a data structure is a programming language for any serious work, but as they say, _the road to (automation) hell is paved with good intentions_.

[^FREE]: One would expect the **free** strategy to work as well, but it doesn't -- it behaves in exactly the same way as the **linear** strategy.
