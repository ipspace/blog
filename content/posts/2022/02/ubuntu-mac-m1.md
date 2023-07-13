---
title: "Running a Ubuntu VM on a Mac M1"
date: 2022-02-28 08:00:00
tags: [ automation ]
pre_scroll: True
---
If you're brand-new to Python and Ansible, you might be a bit reluctant to install a bunch of packages and Ansible collections on your production laptop to start building your automation skills. The usual recommendation I make to get past that hurdle is to create a Ubuntu virtual machine that can be destroyed every time to mess it up.

Creating a virtual machine is trivial on Linux and MacOS with Intel CPU (install VirtualBox and Vagrant). The same toolset no longer works on newer Macs with M1 CPU (VMware Fusion is in tech preview, so we're getting there), but there's an amazingly simple alternative: Multipass by Canonical.
<!--more-->
{{<note info>}}[lima](https://github.com/lima-vm/lima/blob/master/examples/default.yaml) is another option ([more details](https://jvns.ca/blog/2023/07/10/lima--a-nice-way-to-run-linux-vms-on-mac/) by Julia Evans), and it seems to be able to run x86 VM on an ARM CPU. I never tested it though so YMMV.{{</note>}}

Here'a three-step process to getting a running Ubuntu VM on your Mac:

* Install Multipass with `brew install --cask multipass`
* Start the primary Ubuntu VM instance with `multipass start`. Once the VM is started, your home directory is mapped into the `Home` folder of the home directory of `ubuntu` user.
* Connect to the VM with `multipass shell`
* Enjoy ;)

**Notes:**

* *multipass* is just a nice wrapper around the built-in MacOS hypervisor.
* You'll get an ARM version of Ubuntu. It looks like nobody solved the problem of running x86 virtual machines on M1 silicon yet.

```
ubuntu@primary:~$ uname -a
Linux primary 5.4.0-99-generic #112-Ubuntu SMP Wed Feb 2 17:13:12 UTC 2022 aarch64 aarch64 aarch64 GNU/Linux
```

* I added *multipass* as an option to the [Create a Simple Ansible Test Environment](https://my.ipspace.net/bin/get/Ansible/Create%20a%20Simple%20Ansible%20Test%20Environment.pdf?doccode=Ansible).
