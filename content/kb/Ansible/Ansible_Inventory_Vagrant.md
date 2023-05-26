---
kb_section: Ansible
minimal_sidebar: true
pre_scroll: true
title: Creating Ansible Inventory from Vagrant SSH Configuration
url: /kb/Ansible/Ansible_Inventory_Vagrant.html
---
Vagrant-based labs running on top of VirtualBox use port mapping from host TCP ports in range 2000 – 2500 to SSH ports on managed virtual machines.

It’s relatively easy to create Ansible inventory that works in that environment: all you have to do is to specify **ansible\_host** and **ansible\_port** for every managed device, for example:

```
spine-1    ansible_host=127.0.0.1         ansible_port=2222
spine-2    ansible_host=127.0.0.1         ansible_port=2200
leaf-1     ansible_host=127.0.0.1         ansible_port=2201
leaf-2     ansible_host=127.0.0.1         ansible_port=2202
```

Extracting the information from the printout produced by **vagrant ssh-config** and copying the values into an Ansible inventory file is a perfect job for an automation script. You’ll find [mine](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/tools) in the *topologies* directory of my [Network Automation Workshop](https://github.com/ipspace/NetOpsWorkshop) GitHub repository.

Using Vagrant2Inventory
-----------------------

The Vagrant2Inventory script executes **vagrant ssh-config**, parses the printout and prints Ansible inventory file generated from that information to STDOUT. These command line options are recognized by the script:

-   -a (or --address): specify IP address to use instead of 127.0.0.1. Use **–a 10.0.2.2** if you want to [access Vagrant VMs from within another VM in VirtualBox environment](https://www.ipspace.net/kb/Ansible/Running_Ansible_Vagrant_VM.html).
-   --vm: Ansible is running within a VM in VirtualBox. Use 10.0.2.2 instead of 127.0.0.1
-   -s (or --skip): skip hosts matching a regular expression. I use **-s nms** to remove my Ansible VM from the inventory file.
-   -u (or --username): use alternate username (default: vagrant)
-   -p (or --password): use alternate password (default: vagrant)
