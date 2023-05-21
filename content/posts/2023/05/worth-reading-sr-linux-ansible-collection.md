---
title: "Worth Reading: Official Ansible Collection for SR Linux"
date: 2023-05-14 07:22:00
tags: [ automation ]
---
Roman Dodin wrote an article [describing Nokia's Ansible collection for SR Linux](https://learn.srlinux.dev/blog/2023/official-ansible-collection-for-sr-linux/). Although I don't use SR Linux (even though it was the first container supported by [netlab](https://netlab.tools/) ;), it was still very interesting to read about the design tradeoffs they had to make:
<!--more-->
* Even though SR Linux uses REST API, they decided to implement a dedicated Ansible module because using the URI module results in playbooks that are too verbose (plus you might get into interesting fights if your REST API expects you to login and use session cookies).
* Using a dedicated module also simplifies error handling -- the module can return a cleaned-up error message, not a raw HTTP error.
* A dedicated module can also implement diffs and idempotent operations (read state, do a diff, send only the required updates).

Most interestingly, they decided to build a generic module that would be driven by configuration data structures (SR Linux uses data structures not text lines to configure the device), not a maze of dozens of tiny little modules (all alike) that would configure interfaces, IP addresses, routing protocols... like what the Ansible developers produced ([Cisco IOS](https://docs.ansible.com/ansible/latest/collections/cisco/ios/index.html), [Arista EOS](https://docs.ansible.com/ansible/latest/collections/arista/eos/index.html)) in one of their [many  incompatible attempts to get networking modules right](https://blog.ipspace.net/2019/09/measure-twice-cut-once-ansible.html).
