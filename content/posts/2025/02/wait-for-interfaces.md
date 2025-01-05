---
title: "Please Wait While We're Preparing Your Interfaces"
date: 2025-02-05 07:59:00+0100
tags: [ virtualization ]
---
Once a virtual machine running a network operating system boots, you'd expect its data-plane interfaces to be operational, right? Some vendors disagree. It takes over a minute for some network operating systems to figure out they have this thing called *interfaces*.[^GN]

I would love to figure out what takes them so long (a minute is an eternity on modern CPUs), but I guess we'll never know.

[^GN]: Do they have to wake up a gnome and send it to the other side of the virtual machine to look at stuff and come back? I have no idea.

### Behind the Scenes

*netlab* uses two device provisioning mechanisms: it can start virtual machines with *Vagrant* or containers with *containerlab*. Some of those containers might use KVM/QEMU to run a hidden virtual machine (see also: RFC 1925 rule 6a).
<!--more-->
*Vagrant* waits for the virtual machine to have an operational SSH server. Once it logs into the VM with SSH, it declares the VM is ready.

*containerlab* assumes the containers are ready-for-use when they're started. *netlab* has to use *[device readiness scripts](https://github.com/ipspace/netlab/tree/dev/netsim/ansible/tasks/readiness-check)* to [wait for the network device SSH server to become operational](https://github.com/ipspace/netlab/blob/dev/netsim/ansible/tasks/readiness-check/vm-clab-ssh-check.yml).

Most devices can be configured once their SSH server works. Cisco Nexus OS and Junos disagree with that simple approach. Nexus OS throws an error if you try to configure interfaces it hasn't discovered yet, and Junos silently accepts the configuration and does nothing until the interfaces are ready.

The Nexus OS approach is clearly unacceptable if you try to configure the device immediately after it starts, and the Junos approach leads to further problems once you try to run integration tests (because you have no idea how long you have to wait).

_netlab_ tries to cope with that with an extra "wait for the device to be ready" step: it executes the **show interfaces** command until the printout contains the expected interface name.

### How Long Is Long

Before writing this blog post, I measured how long the *initial device configuration* Ansible playbook waits for the interfaces. 

I enabled the profiling callbacks with `export ANSIBLE_CALLBACKS_ENABLED=ansible.posix.profile_tasks`, started a [simple lab](https://github.com/ipspace/netlab/blob/dev/tests/integration/initial/01-interfaces.yml) with **netlab up --no-config** (to skip the initial configuration of all devices), and configured just the tested device with **netlab initial -l _device_name_** (to reduce the profiling clutter).

The resulting Ansible profiling printouts looked similar to this one:

{{<cc>}}Ansible profiling printout: configuring vPTX VM{{</cc>}}
```
===============================================================================
Wait for et-0/0/0 to appear ------------------------------------------------------------------------------------------------ 73.37s
junos_config: deploying initial from /home/****/net101/tools/netsim/ansible/templates/initial/junos.j2 ---------------------- 3.51s
Find configuration deployment deploy_script for initial --------------------------------------------------------------------- 0.04s
Find device readiness script ------------------------------------------------------------------------------------------------ 0.03s
Set variables that cannot be set with VARS ---------------------------------------------------------------------------------- 0.03s
Find configuration template for initial ------------------------------------------------------------------------------------- 0.03s
Figure out whether to deploy the module initial on current device ----------------------------------------------------------- 0.03s
Wait for device to become ready --------------------------------------------------------------------------------------------- 0.01s
Deploy initial configuration ------------------------------------------------------------------------------------------------ 0.01s
Deploy initial configuration ------------------------------------------------------------------------------------------------ 0.01s
Print deployed configuration when running in verbose mode ------------------------------------------------------------------- 0.01s
fail ------------------------------------------------------------------------------------------------------------------------ 0.01s
```

Profiling printouts for container-based VMs included the "wait for SSH server" task:

{{<cc>}}Ansible profiling printout: configuring vjunos-router VM -in-a-container{{</cc>}}
```
Execute local ssh command to check vjunos-router readiness ----------------------------------------------------------------- 86.33s
Wait for ge-0/0/0 to appear ------------------------------------------------------------------------------------------------ 16.14s
junos_config: deploying initial from /home/****/net101/tools/netsim/ansible/templates/initial/junos.j2 ---------------------- 4.84s
Check if 'sshpass' is installed --------------------------------------------------------------------------------------------- 0.15s
Check for 'timeout' command ------------------------------------------------------------------------------------------------- 0.09s
Find configuration deployment deploy_script for initial --------------------------------------------------------------------- 0.04s
Find configuration template for initial ------------------------------------------------------------------------------------- 0.03s
Find device readiness script ------------------------------------------------------------------------------------------------ 0.03s
Figure out whether to deploy the module initial on current device ----------------------------------------------------------- 0.03s
Set variables that cannot be set with VARS ---------------------------------------------------------------------------------- 0.03s
Confirm r SSH server works -------------------------------------------------------------------------------------------------- 0.02s
Deploy initial configuration ------------------------------------------------------------------------------------------------ 0.01s
Wait for ge-0/0/0 interface ------------------------------------------------------------------------------------------------- 0.01s
Deploy initial configuration ------------------------------------------------------------------------------------------------ 0.01s
Wait for device to become ready --------------------------------------------------------------------------------------------- 0.01s
Print deployed configuration when running in verbose mode ------------------------------------------------------------------- 0.01s
Wait for SSH server --------------------------------------------------------------------------------------------------------- 0.01s
fail ------------------------------------------------------------------------------------------------------------------------ 0.01s
```

Here are the test results:

| Device | SSH wait time{{<br>}}(containers only) | Interface{{<br>}}wait time | Initial{{<br>}}configuration |
|---------------------------|--:|--:|--:|
| vjunos-evolved VM (23.2R2.21-EVO) | | 73s | 3.51s |
| Cisco NXOS VM (9.3.10)[^RAM] | | 34s | 33s |
| vjunos-evolved container (23.2R2.21-EVO) | 61s | 66s | 2.98s |
| vjunos-switch container (23.4R2-S2.1) | 86s | 16s | 4.16s |
| vjunos-router container (23.4R2-S2.1 )| 82s | 21s | 4.84s |
{.fmtTable}

[^RAM]: Yeah, you can tell me it's an old release. No, I will not waste time building a newer RAM-guzzling monster.

**Notes:**

* The *SSH wait times* are precise to a few seconds. The Ansible playbook tries to establish an SSH connection and waits for X seconds if the attempt fails. I reduced the **delay** parameter to two seconds to make the measurements more precise, but they're still highly variable.
* The precision of the *interface wait times* is unknown. netlab is using **nxos_command** and **junos_command** modules with **wait_for** option. The interface wait times for VMs in containers also depend on when the previous step (*waiting for SSH server*) decides the device is ready -- compare the vPTX (vjunos-evolved) container and VM timings.
* The *initial configuration* time should be relatively precise. It's the time it takes **nxos_config** and **junos_config** to get the job done.

**Takeaway:** Some bloatware is incredibly slow. Use something else if you want to enjoy virtual labs ;)