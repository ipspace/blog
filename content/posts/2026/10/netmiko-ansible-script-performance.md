---
title: "Netmiko vs Ansible: Executing Scripts"
date: 2026-10-15 07:52:00+0200
tags: [ netlab ]
netlab_tag: details
---
My initial "_[configuring Arista cEOS with Netmiko or Ansible](/2026/10/netmiko-ansible-performance/)_" test was a bit biased. netlab generates the final configuration snippets in both cases (due to [Ansible FUBARs](/2025/11/ansible-12-different/) we had to deal with), but then Netmiko just sends the configuration commands to the switch (after entering configuration mode), while the Ansible **eos_config** module executes **show running**, identifies the difference, and sends only the changes to the device.

While that use case is highly relevant (after all, we're configuring network devices ;) I really should have done an apples-to-apples comparison, and FRRouting virtual machines are the ideal playground.
<!--more-->
The FRRouting virtual machines are always configured with **bash** or **vtysh** scripts. The script is first sent to the device, then executed on it. This is the relevant Ansible task list[^CVS]:

[^CVS]: We're still checking for **bash** or **vtysh** scripts; we should clean this up, but it doesn't matter.

{{<printout>}}
- template:
    src: "{{ config_template }}"
    dest: /tmp/config.sh

- set_fact: deployed_config={{ lookup('template',config_template) }}

- name: "run /tmp/config.sh to deploy {{netsim_action}} config from {{ config_template }}"
  command: bash /tmp/config.sh
  when: not ansible_check_mode and ("#!/bin/bash" in deployed_config or "#!/bin/sh" in deployed_config)
  become: true

- name: "run vtysh to import {{netsim_action}} config from {{ config_template }}"
  command: vtysh -f /tmp/config.sh
  when: not ansible_check_mode and not ("#!/bin/bash" in deployed_config or "#!/bin/sh" in deployed_config)
  become: true
{{</printout>}}

The equivalent Netmiko code is (almost) trivial. It uses the **scp** library to push the script to the device, and then executes the script over an already-opened SSH session using a [crazy workaround](https://github.com/ipspace/netlab/blob/9efd2ddb1cff03cbd831dfbe2b2c6fa4b705c26f/netsim/providers/libvirt/configs.py#L74) to detect script errors:

```
    cmd_marker = "__NETMIKO_RC:" # Use a marker to get back the return code
    cmd = f'chmod a+x {cfg_file}; {cfg_file} 2>&1; rc=$?; echo {cmd_marker}$rc'
```

Like in the [previous test](/2026/10/netmiko-ansible-performance/), I used an EVPN lab and measured the startup (Vagrant starting Linux VMs) and configuration (Netmiko or Ansible doing their job) times.

Here are the results:

| Operation | netlab CPU time[^NCP] | Elapsed time |
|-----------|----------------:|-------------:|
| Starting the lab | 4.5 s | 25.7 s |
| Configuration with Netmiko | 0.5 s | 2.2 s |
| Configuration with Ansible | 3.0 s | 11.4 s |
{.fmtTable}

[^NCP]: Includes the CPU time spent in child processes, for example, **vagrant** or **ansible-playbook**.

It takes almost half a minute to start the Linux virtual machines[^MBN], but then Netmiko delivers blazingly fast performance, while Ansible remains Ansible. Admittedly, the "push template and execute a script" operations are much faster than the equivalent **eos_config** operations (which took over half a minute), but it's still five times slower than the alternative.

[^MBN]: Still peanuts compared to Nexus OS, Junos, or IOS XR.
