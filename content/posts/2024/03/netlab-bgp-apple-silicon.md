---
title: "Running netlab and BGP Labs on Apple Silicon"
date: 2024-03-18 08:01:00+0100
lastmod: 2024-05-17 11:25:00+0200
netlab_tag: use
tags: [ netlab, BGP ]
---
I usually say that you cannot run netlab on Apple Silicon because the vendors don't provide ARM images. However, when I saw an ARM version of the FRRouting container, I wondered whether I could run the BGP labs (admittedly only on FRR containers) on my M2 MacBook Pro.

**TL&DR:** Yes, you can do that.

Now for the recipe:
<!--more-->
* [Install multipass](https://multipass.run/docs/installing-on-macos). I used Homebrew to install it.
* Start the default Ubuntu VM

```
% multipass shell
```

* Once you get the Ubuntu prompt, install Pip3 and netlab:

```
$ sudo apt-get update
$ sudo apt install python3-pip
$ pip3 install networklab
```

* Pip3 creates the `~/.local/bin` directory, which is not yet in the PATH. Logout (`exit` or Ctrl-D) and reconnect to the Ubuntu VM (yet again, using `multipass shell`)
* Use `netlab install` to install Ubuntu tools, Containerlab, and Ansible

```
$ netlab install ubuntu containerlab ansible
```

* The installation script adds the current user to the `docker` group to allow you to start containers. However, the shell process in the current session is not yet a member of that group, and we probably don't have enough disk space for the next step anyway.
* Log out of the Ubuntu instance.
* Increase the instance disk size and restart it.

```
% multipass stop primary
% multipass set local.primary.disk=10G
% multipass shell
```

* The multipass instance [does not have the Linux kernel drivers](https://netlab.tools/caveats/#frr) we need for FRR management VRF and MPLS forwarding. Log into the Ubuntu instance and install the missing generic Linux drivers:

```
sudo apt install linux-generic
```

* Log out of the VM, restart it, and log in:

```
% multipass restart primary
% multipass shell
```

* Start a simple lab to test the installation

```
$ netlab test clab
```

You're ready to run labs using FRR containers on your Apple laptop. Install [BGP labs](https://bgplabs.net/1-setup/#setting-up-the-labs) and have fun ;)
