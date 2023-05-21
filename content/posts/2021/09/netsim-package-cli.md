---
date: 2021-09-01 06:07:00+00:00
netlab_tag: overview
series_title: Python Package and Unified CLI
tags:
- netlab
title: netlab Python Package and Unified CLI
---
One of the major challenges of using *netsim-tools* (now renamed to *netlab*) was the installation process -- pull the code from GitHub, install the prerequisites, set up search paths... I knew how to fix it (turn the whole thing into a Python package) but I was always too busy to open that enormous can of worms.

That omission got fixed; *netlab* is now available on PyPI and installed with **pip3 install networklab**.
<!--more-->
I faced two major challenges when creating the package:

* Non-Python files (YAML configuration files, Ansible playbooks, task lists, Jinja2 templates...). In the end I managed to include them in the package -- turns out it's not hard once you know what you're doing -- but they get installed into some weird inconvenient place.
* A dozen Ansible playbooks and scripts that were part of the *netlab* distribution. I could ask **pip** to install them into whatever **bin** directory, but I hate polluting the filesystem. In the end, I decided to hide the complexity behind unified CLI (aka "*one command to rule them all*").

All *netlab* functionality is now available through [**netlab** command](https://netlab.tools/netlab/cli/):

* **[netlab create](https://netlab.tools/netlab/create/)** creates all the configuration files you need.
* **[netlab initial](https://netlab.tools/netlab/initial/)** deploys initial configuration to all lab devices.
* **[netlab config](https://netlab.tools/netlab/config/)** deploys additional configuration using your own Jinja2 templates.
* **[netlab connect](https://netlab.tools/netlab/connect/)** connects to lab devices via Docker or SSH.

I also noticed some users struggled with the *libvirt*-based installation on Ubuntu, so I added **[netlab install](https://netlab.tools/netlab/install/)** that installs:

* Prerequisite Ubuntu software, including Python3 tools, git, sshpass and XML libraries.
* KVM, libvirt, and Vagrant
* Ansible, TextFSM, paramiko, netmiko, ntc-templates...

**[netlab test](https://netlab.tools/netlab/test/)** can also run a comprehensive test of your lab environment including:

* Creating Vagrant/containerlab and Ansible configuration files
* Starting a three node Cumulus VX[^1] lab
* Configuring the network devices, including OSPF configuration
* Destroying the lab

Last but definitely not least, you're most welcome to join the [netlab Slack channel](https://networktocode.slack.com/archives/C022DQHK8BH) @ [network2code Slack team](https://slack.networktocode.com/).

[^1]: Because Cumulus VX happens to be the only no-strings-attached network device available as VirtualBox and libvirt Vagrant box, and a Docker container.
