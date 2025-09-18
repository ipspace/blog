---
title: "Arista EOS Hates a Routing Instance with No Interfaces"
date: 2025-09-18 07:20:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
I always ask engineers [reporting a _netlab_ bug](https://github.com/ipspace/netlab/issues) to provide a minimal lab topology that would reproduce the error, sometimes resulting in "interesting" side effects. For example, I was trying to debug a BGP-related Arista EOS issue using a _netlab_ topology similar to this one:

```
defaults.device: eos
module: [ bgp ]
nodes:
  a: { bgp.as: 65000 }
  b: { bgp.as: 65001 }
```

Imagine my astonishment when the two switches failed to configure BGP. Here's the error message I got when running the netlab's *deploy device configurations* Ansible playbook:
<!--more-->
```
TASK [eos_config: deploying bgp from /netsim/ansible/templates/bgp/eos.j2] **********************************
fatal: [b]: FAILED! => changed=false
  data: |-
    bgp advertise-inactive
    % Invalid input
    b(config-s-ansible_17)#
  msg: |-
    bgp advertise-inactive
    % Invalid input
    b(config-s-ansible_17)#
fatal: [a]: FAILED! => changed=false
  data: |-
    bgp advertise-inactive
    % Invalid input
    a(config-s-ansible_17)#
  msg: |-
    bgp advertise-inactive
    % Invalid input
    a(config-s-ansible_17)#
```

Fortunately, the error was easy to reproduce within an interactive session, but the results totally stumped me.

```
$ netlab connect a
Connecting to clab-X-a using SSH port 22
Last login: Thu Sep 18 05:28:50 2025 from 192.168.121.1
a#conf t
a(config)#router bgp 65000
% Unavailable command (not supported on this hardware platform)
a(config)#
```

{{<note warn>}}
Note that the **router bgp** command failed, but Ansible only reported a failure with the subsequent **bgp advertise-inactive** command -- another example of ~~sloppy~~ suboptimal screen-scraping. It looks like they consider only "Invalid input" to be an error message.
{{</note>}}

Following the *when in doubt, reboot* approach familiar to anyone who contacts a vendor's TAC often enough, I rebooted the server, thinking it might be a container error. Of course, that did not help[^RBH].

[^RBH]: Rebooting a device helps only when you're instructed to do so by a vendor TAC engineer ;) Also, [this](https://www.mentalfloss.com/posts/definition-of-insanity-albert-einstein).

Even worse, the device refused to enable IP routing in the global routing instance, producing the same confusing "not on this hardware platform" error message. The behavior was consistent across various EOS releases running as containers or virtual machines.

```
$ netlab connect a
Connecting to clab-X-a using SSH port 22
Last login: Thu Sep 18 05:30:31 2025 from 192.168.121.1
a#conf t
a(config)#ip routing
% Unavailable command (not supported on this hardware platform)
a(config)#
```

After a pretty long fruitless head-banging, I decided to start a lab topology I knew worked in the past, and it started flawlessly. Now I was onto something: I "only" had to identify the differences between the two topologies... and then it hit me like a ton of bricks. The "test" lab topology had no links, so the default VRF had no interfaces:

```
a#show vrf default
   VRF           Protocols       State         Interfaces
------------- --------------- ---------------- ----------
   default       IPv4            no routing    Lo0
   default       IPv6            no routing
```

Arista EOS obviously hates having no interfaces in the default VRF (I can't blame it; it must feel really lonely), but its error message could be a bit more on-target.
