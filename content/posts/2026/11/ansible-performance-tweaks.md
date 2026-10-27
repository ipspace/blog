---
title: "Ansible Performance Tweaks"
date: 2026-11-30 11:33:00+0100
tags: [ ansible ]
draft: True
---
[Cora R](https://www.linkedin.com/in/corarain/) wrote a comment documenting several Ansible performance tweaks. It's too good to waste, and she agreed to have it republished as a blog post, so here we go:

---

* If each node is independent, you can use the "free" strategy and increase "forks" and "serial". This will increase concurrency at the expense of requiring more memory.
* Linear playbooks can be tricky... If any node in the batch becomes unresponsive, it can slow down the entire play.
* There is Ansible pipelining, but only for some devices.
<!--more-->
Next, she described several TCP settings that can help:

* Enable TCP BBR on the control host and end nodes if possible. 
* Make sure to set "ConnectTimeout" on the SSH client, especially when connecting over cellular! Sometimes there can be enough throughput to keep TCP alive, yet enough latency or packet loss to make SSH drop and re-negotiate indefinitely without progressing the play!

Finally: Depending on the end device, you can use Ansible with a Jinja2 template file to generate the config files locally, then use something else or another playbook to push or pull the configs to the end device. This could make sense if you are already sourcing from a dynamic inventory, want a version-controlled copy of the configs, or just want to separate generating the configs from deploying them due to scaling needs.

---

Thanks a million!