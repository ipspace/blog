---
kb_section: AutomationLab
minimal_sidebar: true
title: Creating Ansible Development Environment
url: /kb/AutomationLab/10-Ansible_Environment.html
---
Looking for a quick recipe? [Read this document](https://my.ipspace.net/bin/get/Ansible/Create%20a%20Simple%20Ansible%20Test%20Environment.pdf). Still here? Let's go

## Where will you run Ansible playbooks?

Ansible runs on Linux and Mac OSX. While some people install Ansible on their Macs (potentially using Python virtual environments), I’d strongly recommend installing it in a Linux virtual machine for these reasons:

- Mac OSX is *almost* Unix, but there might be slight discrepancies between Linux and OSX behavior that would result in hard-to-troubleshoot Ansible failures, particularly when using Ansible network modules. Running Ansible on Linux usually results in fewer problems.
- I managed to completely mess up my Python environment while trying to work with multiple Ansible versions simultaneously. Fortunately I messed up my Linux virtual machine and not my Mac, and because I’m using Vagrant and install scripts (see below) I was back in business in less than 10 minutes.

Please note:

- If you feel confident in your Python or sysadmin skills, it's perfectly fine to install Ansible and NAPALM on your OSX machine. I would use [homebrew](https://brew.sh/) to do it.
- If you’re running Windows you have no options anyway – Ansible doesn’t run on Windows.
- An alternative if you're trying to solve the *Ansible platform* problem not the *build the lab* problem is to run [Ansible in a Docker container](https://github.com/cidrblock/ansible-docker) ([[another recipe](https://packetpushers.net/building-a-docker-network-automation-container/)). Docker containers run on Linux, OSX and Windows.

## Selecting the Virtualization Environment

If you decide to run your network automation tools, you have to start with a virtualization environment. Use VirtualBox (free) if you can. It runs on Windows, Mac OSX or Linux.

If you need nested virtualization (for example, to run Cisco VIRL), use VMware Workstation on Windows, or VMware Fusion on Mac OSX. They are not free but also not outrageously expensive. On Linux you’d probably want to use KVM... and if you're a Hyper-V fan use that on Windows.

## Creating the Ansible Virtual Machine

Another strong recommendation: use Vagrant. While you might love to build your VMs from ISO images (or kernel sources), deploying a Linux VM within Vagrant environment is a breeze.

Vagrant works with all virtualization products I mentioned. VirtualBox plugin is free and included with Vagrant. I had to buy the VMware plugins.

Vagrant also takes care of creating a username, SSH keys, **sudo** setup, and maps one or more directories of your physical machine into a directory within Linux VM. Long story short: if you’re not a Linux guru, use Vagrant.

To use Vagrant you have to create a *Vagrantfile* (it has to have *exactly that name*) describing your topology. While I always believe in reading the documentation and understanding how things work behind the scenes, you’ll find a few useful links and tutorials at the end of this document, and if all you need is a single virtual machine running Ansible use **vagrant init** (also described in the [quick recipe](https://my.ipspace.net/bin/get/Ansible/Create%20a%20Simple%20Ansible%20Test%20Environment.pdf))

## Installing Ansible

Ansible is easy to install on most Linux distributions (I use Ubuntu). Follow the [instructions on Ansible web site](http://docs.ansible.com/ansible/intro_installation.html) or use [my installation scripts](https://github.com/ipspace/NetOpsWorkshop/tree/master/install).

When you’re done you should be able to SSH from your Ansible virtual machine to external network devices (example: your home router) and execute **show** ***something*** on them using Ansible **raw** module (see *Using Ansible* section of the [Ansible for Networking Engineers webinar](https://my.ipspace.net/bin/list?id=Ansible) for details).

