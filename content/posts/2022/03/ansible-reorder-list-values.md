---
title: "Beware: Ansible Reorders List Values in Loops"
date: 2022-03-24 07:27:00
tags: [ Ansible ]
pre_scroll: True
---
**TL&DR**: Ansible might decide to reorder list values in a **loop** parameter, resulting in unexpected order of execution and (in my case) totally borked device configuration.

A bit of a background first: I'm using an Ansible playbook within *[netlab](https://netlab.tools/)* to deploy [initial device configurations](https://netlab.tools/netlab/initial/). Among other things, that playbook deploys configuration snippets for [numerous configuration modules](https://netlab.tools/modules/), and the order of deployment is absolutely crucial. For example, you cannot activate BGP neighbors in Labeled Unicast (BGP-LU) address family (**mpls** module) before configuring BGP neighbors (**bgp** module).
<!--more-->
To make the ordered deployment of configuration snippets work, every *host* (Ansible term for *managed device*) has a list of modules in the **module** fact (Ansible term for *variable*) in its *host_vars*. For example, these are the values of the **module** fact for all devices in the [BGP-LU lab](https://github.com/ipspace/netlab-examples/tree/master/MPLS/ldp-bgp-lu):

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

The only workaround I could find *within Ansible* was to set **serial** (batch size) to one[^FREE] to deploy configurations on a single device at a time (so Ansible has nothing to optimize). It works, but it also makes lab deployment way slower than it should have been.

Maybe I made a wrong choice and shouldn't use something that thinks a data structure is a programming language for any serious work, but as they say, _the road to (automation) hell is paved with good intentions_.

### Simple Tasks Are Not Affected

I found it pretty impossible that something so unexpected would not get noticed and fixed, so I did something similar with a simple **debug** task:

```
- hosts: all
  tasks:
  - debug:
      msg: "{{ item }} on {{ inventory_hostname }}"
    loop: "{{ module }}"
    when: module is defined
```

This time, the items did not get rearranged -- the debugging messages were printed in the order the modules were listed in **module** lists. The interleaving of tasks across multiple devices was interesting, but within a single device the order was correct.

```
TASK [debug] **************************
ok: [p] => (item=ospf) =>
  msg: ospf on p
ok: [ce1] => (item=bgp) =>
  msg: bgp on ce1
ok: [pe2] => (item=ospf) =>
  msg: ospf on pe2
ok: [ce2] => (item=bgp) =>
  msg: bgp on ce2
ok: [pe1] => (item=ospf) =>
  msg: ospf on pe1
ok: [rr] => (item=ospf) =>
  msg: ospf on rr
ok: [p] => (item=mpls) =>
  msg: mpls on p
ok: [ce1] => (item=mpls) =>
  msg: mpls on ce1
ok: [rr] => (item=bgp) =>
  msg: bgp on rr
ok: [rr] => (item=mpls) =>
  msg: mpls on rr
ok: [pe2] => (item=bgp) =>
  msg: bgp on pe2
ok: [pe2] => (item=mpls) =>
  msg: mpls on pe2
ok: [ce2] => (item=mpls) =>
  msg: mpls on ce2
ok: [pe1] => (item=bgp) =>
  msg: bgp on pe1
ok: [pe1] => (item=mpls) =>
  msg: mpls on pe1
```

**Conclusion**: The weird rearranging behavior applies to **include_tasks**, but not to regular tasks.

### But Wait, It Gets Worse

As the Ansible playbook I described above gets used from within *netlab*, it might be possible to work around the "Ansible optimization strategy 🤪":

* Create a new group (*modules*) that will contain only the devices with configuration modules, eliminating the need for a complex **when** condition and default values. Use this new group (instead of **all**) in the Ansible play.
* Create a global list of modules (**netlab\_module**) in the correct order and save it as a group variable to make sure all hosts get the same value
* Iterate over the global list of modules and include the *deploy module* task list only for those modules that are needed by individual devices (when the loop variable is in **module** list).

The next iteration of the _Deploy module-specific configurations_ play was thus something along these lines:

```
- name: Deploy module-specific configurations
  hosts: modules
  strategy: "{{ netsim_strategy|default('linear') }}"
  tags: [ module,test ]
  tasks:
  - include_tasks: "tasks/deploy-module.yml"
    loop: "{{ netlab_module }}"
    loop_control:
      loop_var: config_module
    when: config_module in module
```

Guess what... **it doesn't work**. The moment there's a *when* condition in the *include_tasks* task, Ansible starts rearranging the loop iterations. In the end, there's absolutely no difference between the original code (where we iterated over different lists for different devices) and the one above (where the list we iterate over is the same, but the task is not always executed).

### The Final Workaround

In the end, I decided that the only possible result of fighting software windmills is a damage to one's sanity, and gave up. I moved the **when** condition into the included task list -- the top-level includes are always executed, but then the tasks within the included task list might be skipped.

The details are in [this commit](https://github.com/ipspace/netlab/commit/da013c44d85bb0fd210ad478b70ffcb24bc762cd).

[^FREE]: One would expect the **free** strategy to work as well, but it doesn't -- it behaves in exactly the same way as the **linear** strategy.
