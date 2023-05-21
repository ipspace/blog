---
date: 2023-02-20 06:52:00+00:00
netlab_tag: guidelines
series_title: Start Multiple Lab Instances on the Same Server
tags:
- netlab
title: Start Multiple netlab Labs on the Same Server
---
A heavy _netlab_ user sent me an email along these lines:

> We're running multiple labs in parallel on the same server, and we're experiencing all sorts of clashes like overlapping management IP addresses. We "solved" that by using static device identifiers in our labs, but I'm wondering if there's a better way of doing it?

That's exactly the sort of real-life challenges I love working on, so it wasn't hard to get me excited, and the results are [bundled in _netlab_ release 1.5](https://netlab.tools/plugins/multilab/).
<!--more-->
## The Problem

Let's start with _what problem are we trying to solve?_:

* _netlab_ assumes that the underlying provisioning system creates a management network that can be used to access network devices.
* *vagrant-libvirt* plugin and *containerlab* have a default name for the management network, and so _netlab_ (by default) doesn't mess with it.
* *vagrant-libvirt* does not adjust the `/etc/hosts` file (_containerlab_ does), so it's crucial to have well-known management IP addresses assigned to the network devices. _netlab_ solves that by using the default *vagrant-libvirt* management network subnet together with static MAC addresses and DHCP bindings.

Starting two labs on the same server will inevitably result in overlapping IP addresses unless you specify unique node **id** values in every lab topology. Obviously not something one can rely on for a stable production-grade solution.

But wait, it gets worse. *vagrant-libvirt* and *containerlab* augment VM names or container names with a prefix to make them unique. _netlab_ uses the same approach to name *libvirt* networks or Linux bridges it needs to create. The default prefix is the current directory name, which means that when two users start the same lab all sorts of weird things could happen.

Finally, the UDP tunnels used to implement *libvirt* point-to-point links used IP addresses calculated from node **id** and interface **ifindex**. Starting two labs with point-to-point links might also have some interesting side effects.

## Use Cases

It quickly became evident that different users might want to use the _multiple labs per server_ functionality in different ways:

* A single user starting multiple labs in different directories.
* Multiple users starting parallel labs (using the same or different lab topology) on the same system.
* Some environments would want to have an even more flexible approach with on-demand allocation of lab resources.

The solution has to be flexible enough to support all three use cases, and simple enough that it could be used without external components.

## The Solution

Here's what we decided to implement:

* The _multiple labs_ functionality is implemented with a new [_multilab_ plugin](https://netlab.tools/plugins/multilab/), making the changed behavior completely optional. If you don't use that plugin, you get the traditional _netlab_ setup.
* Every lab instance using _multilab_ plugin must have a unique lab ID. Assigning the lab ID, and making sure it's unique[^NC], is the users' responsibility.
* _multilab_ plugin uses the lab ID to make _netlab_ parameters like the management subnet, the management network name, the VM/container prefix, VIF interface names and libvirt tunnel endpoints unique.
* Modified parameters are used when creating `Vagrantfile`, *containerlab* topology or Ansible inventory, ensuring that each lab instance gets a unique set of resources.

[^NC]: In release 1.5.0, the uniqueness of the lab ID is not checked. I hope to have at least rudimentary checks in release 1.5.1.

Here's how you can use this functionality to support the three use cases:

* **Multiple labs per user**: set the **defaults.multilab.id** parameter in lab topology or as a CLI parameter. 
* **Multiple users** with one lab per user: set the user-wide **multilab.id** default in `~/.netlab.yml` file.
* **Flexible allocation**: build an external component that keeps track of lab IDs and a wrapper around _netlab_ command that sets **defaults.multilab.id** CLI parameter.

If you have a better idea, please open a [GitHub](https://github.com/ipspace/netlab) issue or discussion.

Finally, it would be an interesting exercise in futility to try to enforce the use of *multilab* plugin with every lab topology, so I added the capability to specify the default list of plugins used by all lab topologies as **plugin** parameter in a [defaults file](https://netlab.tools/defaults/) -- add `plugin: [ multilab ]` to `~/.netlab.yml` file and you're good to go.

### Getting Started

To get more details and learn about additional features included in release 1.5.0, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
