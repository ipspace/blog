---
title: "Content: New Parameter in Multiple something_config Ansible Modules"
date: 2026-07-15 07:22:00+0200
tags: [ ansible ]
---
Last December, I wrote a [pretty ranty post](/2025/12/ansible-abandoned-network-automation/) explaining how Ansible release 12 broke (some?) network device configuration playbooks. The inevitable anonymous troll (why are they always anonymous?) couldn't resist asking whether I [opened an issue on GitHub](https://blog.ipspace.net/2025/12/ansible-abandoned-network-automation/#2821). I didn't (more about that later), but when the [solution to that rant](https://github.com/ansible-collections/ansible.netcommon/pull/743) was "_we're deprecating using templates in **src**_" parameter, I opened an issue arguing [why that's not a good idea](https://github.com/ansible-collections/ansible.netcommon/issues/745).
<!--more-->
That issue led to the idea of adding another parameter to `something_config` Ansible modules — the rendered **content** (as a string) — and then all quieted down until I got an email that the issue was closed as *not planned*.

To my pleasant surprise, that was just bad issue management. New versions of **cisco.ios.ios_config** and **arista.eos.eos_config** modules have `content` parameter, and a good explanation of why you should use it, and when templating the `src` parameter will be deprecated. I didn't check more than   a few modules, but I'm positive the Ansible team did a good job and added the same parameter to other device configuration modules. Nice job, thank you!
