---
kb_section: AutomationLab
index: True
minimal_sidebar: true
title: Building a Network Automation Lab
toc_title: Introduction
url: /kb/AutomationLab/
tags: [ automation ]
---
To complete the exercises included in the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course (or to do your own exploration into the world of network automation) you’ll need a reliable lab environment. There are three major steps you have to complete to get there:

- [Create an environment capable of running network automation tools](10-Ansible_Environment.html) you want to use. We'll focus on getting Ansible and NAPALM up and running.
- [Build a networking lab](20-Networking_Lab.html) using either physical or virtual devices.
- [Establish connectivity](30-Connectivity.html) between your network automation environment and your networking lab.

The rest of this document describes some of the potential approaches to building a network automation lab. Don’t limit yourself to what’s described here – go out and experiment.

You might also be interested in these alternative approaches:

- [Full-blown development environment created by Carl Buchmann](https://blog.ipspace.net/2018/10/network-automation-development.html)
- [Building a Docker network automation container](https://packetpushers.net/building-a-docker-network-automation-container/)

## Don't Create a Science Project

Some networking engineers severely overestimate their skills in adjacent areas. Building a virtual lab for the first time with Vagrant and VirtualBox while fighting bugs in vendor Vagrant boxes can be a daunting task. If you're new to Linux and virtual labs please try to keep things as simple as possible. Here are a few ideas (in increasing order of complexity):

- Use my [quick recipe](https://my.ipspace.net/bin/get/Ansible/Create%20a%20Simple%20Ansible%20Test%20Environment.pdf) to create your network automation environment and use physical network devices (if nothing else, configure your home router);
- Install a workstation virtualization product (VirtualBox or VMware Fusion/Workstation) and create Linux VM and network devices from ISO images using GUI. You can still use my recipe and [installation scripts](https://github.com/ipspace/NetOpsWorkshop/tree/master/install) to set up the network automation environment.
- Instead of creating individual VMs for network devices, set up VIRL or GNS3 and enable outside access to network devices.
