---
title: "Underscores (in Hostnames) Strike Again"
date: 2025-12-15 07:23:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
I don't know why I decided to allow underscores in _netlab_ node names. Maybe it's a leftover from the ancient days when some network devices refused to accept hyphens in hostnames, or perhaps it's a programmer's subconscious hatred of hyphens in identifiers (no programming language I'm aware of allows them for a very good reason).

Regardless, you can use underscores in [*netlab* node names](https://netlab.tools/nodes/) (and plugins like *[multilab](https://netlab.tools/plugins/multilab/)* use them to create unique hostnames), and they work great on Linux distributions we recommend... until they don't.

What follows is a story about the [weird dependencies](https://xkcd.com/2347/) that might bite you if you ignore [ancient RFCs](https://datatracker.ietf.org/doc/html/rfc952).
<!--more-->
It started with an [issue](https://github.com/ipspace/netlab/issues/2911) saying "Arista EOS containers don't work with the multilab plugin." The user creating the issue even suggested a workaround: replace `ml_xx` as a prefix that generates unique host names with `ml-xx`.

{{<note info>}}
Thanks a million to [@leec-666](https://github.com/leec-666) for reporting this problem. While we encounter plenty of issues when using _netlab_ ourselves, it's invaluable to get error reports as soon as something weird or unexpected happens (even if you managed to work around it).
{{</note>}}

I could have implemented that fix and moved on, but I learned the hard way not to [ignore dead canaries in coal mines](https://blog.ipspace.net/2012/09/dear-vmware-bpdu-filter-bpdu-guard/), so I decided to investigate.

I'm using *multilab* extensively for [_netlab_ integration tests](https://blog.ipspace.net/2024/05/netlab-integration-tests/), and Arista EOS containers are among the most-tested platforms, so I started my troubleshooting assuming the error was caused by some less-common Linux distro (we've [been there](https://github.com/ipspace/netlab/issues/2424)). Alas, I was quickly able to reproduce it on a fresh Ubuntu 24.04 installation.

After tons of digging and dependency checks, the root cause turned out to be a new version of the *ansible-pylibssh* library. Version 1.3.0 (released on October 12th) rejects underscores in hostnames, even on Linux distributions that happily resolve them and allow them in the **ssh** command. To make matters worse, there's nothing in that library (I ran a diff against a "working" version) that would check hostnames, so the altered behavior must have been caused by the changes in how they call *libssh*.

Anyway, while it's good to know the root cause, pinning the package version isn't exactly a long-term solution, so I started looking for alternatives and got my "ah-ha!!!" moment when I noticed that my Ansible playbooks crash when trying to configure Arista EOS *containers*, but they work on Arista EOS *virtual machines*.

Ages ago, I decided to use management IPv4 addresses instead of node names in Ansible inventory (because I didn't want to deal with the hassle of setting up hostname resolution). I used container names instead of IPv4 addresses for all containers because *containerlab* does a great job modifying and cleaning up `/etc/hosts`. Taking that shortcut proved to be a terrible choice indeed.

Changing the way _netlab_ is building the Ansible inventory from *use container names as **ansible_host** for all containers* to *use container names as **ansible_host** only for nodes using **docker exec** for configuration* solved the problem and made containers with SSH servers identical (from the configuration perspective) to virtual machines.

**Lessons learned:**

* Taking shortcuts will bite you
* Ignoring RFCs and best practices is not a good idea

But we knew all that for ages and keep ignoring it all the time, right?

Anyway, the patch is available in [_netlab_ release 25.12.03](https://netlab.tools/release/25.12/). You don't have to upgrade _netlab_ if you're not affected by that particular bug, but the bug fix is available if you need it (and will be applied automatically to all new installations).
