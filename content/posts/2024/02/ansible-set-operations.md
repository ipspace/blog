---
title: "Ansible Set Operations Do Not Preserve List Order"
date: 2024-02-26 07:08:00+0100
tags: [ Ansible ]
---
Here's another Ansible quirk, this time caused by Python set behavior.

When I created the [initial device configuration deployment](https://netlab.tools/netlab/initial/) playbook in *[netlab](https://netlab.tools/)*, I wanted to:

* Be able to specify a list of modules to provision.[^DAM]
* Provision just the modules used in the topology _and_ specified in the list of modules.

[^DAM]: The default value is all modules used in the lab topology.

This allows you to use `netlab initial` to deploy all configuration modules used in a lab topology or `netlab initial -m ospf` to deploy just OSPF while surviving `netlab initial -m foo` (which would do nothing).
<!--more-->
We covered the first part of this saga in [Precedence of Ansible Extra Variables](/2024/01/ansible-extra-variable-precedence/):

```
- set_fact:
    mod_select: "{{ modlist.split(',') if modlist is defined else netlab_module }}"
```

That would generate a list of modules, either those specified on the command line with the `modlist` extra variable or all modules used in the topology (specified in the `netlab_module` inventory variable).

It's worth noting that the order of configuration deployment matters. For example, you have to configure VLANs before OSPF to have the VLAN interfaces that can be specified in the OSPF process.[^OD] To get that done, I decided to create a loop that would iterate over all modules _specified in the lab topology and in the `mod_select` variable_ (I had to use this approach instead of just iterating over device modules due to [another Ansible quirk](/2022/03/ansible-reorder-list-values/)):

[^OD]: In case you're curious: _netlab_ modules specify which modules have to be configured before them, and _netlab_ uses that information to do a [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) and store the results in the `netlab_module` Ansible inventory variable.

```
- include_tasks: "tasks/deploy-module.yml"
  loop: "{{ netlab_module|intersect(mod_select) }}"
  loop_control:
    loop_var: config_module
```

Now for the fun part: this approach works most of the time[^90P], but when I combined DHCP and OSPF modules, their order was swapped approximately half of the time (and yes, it's non-deterministic, which makes it even more annoying).

It turned out the root cause was the **intersect** filter. While all the examples in the [Ansible documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html#selecting-from-sets-or-lists-set-theory) imply that the order of elements is preserved, in reality _it is not_. The **intersect** filter [turns both arguments into sets](https://github.com/ansible/ansible/blob/1b209d742e39900e676e6a43f900801e67cc9154/lib/ansible/plugins/filter/mathstuff.py#L84), does the intersection operation, and returns a list. Python documentation is quite clear: sets are [*unordered* collections](https://docs.python.org/3/tutorial/datastructures.html#sets), and so we could get the elements in the intersection list *in a completely different order*.

Workaround: replace the **intersect** filter with a **when** condition:

```
- include_tasks: "tasks/deploy-module.yml"
  loop: "{{ netlab_module }}"
  when: config_module in mod_select
  loop_control:
    loop_var: config_module
```

On a totally unrelated train of thought: isn't it great that we have enough time to waste half the Sunday morning chasing such gremlins?

[^90P]: OK, it works all the time 90% of the time 🤪