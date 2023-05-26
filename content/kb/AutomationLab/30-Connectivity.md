---
kb_section: AutomationLab
minimal_sidebar: true
title: Accessing Network Devices from Your Automation Environment
url: /kb/AutomationLab/30-Connectivity.html
---
The network automation environment you build [in the first step](10-Ansible_Environment.html) has to be able to access your networking lab.

If you’re running a physical lab or a virtual lab on another server, make sure your workstation can access the devices (how to get there is out of scope of this document - but hey, you're a networking engineer). If you can access the lab from your workstation, you’ll be able to access it from the Ansible VM, as all desktop hypervisor products use either bridging between VM Ethernet interface and workstation Ethernet interface or NAT on the workstation to access the outside world.

If you're running your networking lab in a wrapper product like GNS3 or VIRL, read their instructions on accesing the network devices from outside. Once you're able to reach the devices in the networking lab from your workstation you're almost there.

## Running Your Environment on a Single Machine

If you run the networking lab and the automation environment on a single workstation you'll have to figure out the internal virtual networking provided by your virtualization platform, and if you decide to use a static environment in which you start the virtual machines by hand, simply connect the network automation VM to the same virtual segment as your network device VMs (or GNS3 or VIRL VM).

<div class='stop' markdown='1'>Whatever you do, don't try to mix multiple virtualization products on the same workstation. Trying to run VIRL in VMware Workstation, and Ansible VM in VirtualBox (just so you won't have to buy VMware plugin for Vagrant) won't end well.</div>

Getting the job done with Vagrant is just a bit more complex. You have to modify Vagrantfile to connect your virtual machines to multiple segments anyway (or you wouldn't be building a networking lab). Just add an out-of-band management network and connect all network devices and the network automation VM to it.

Here are a few topologies to get you started:

- [Ansible VM with VIRL](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/VIRL) running on VMware Fusion or Workstation (you cannot run VIRL on VirtualBox)
- [Adding vSRX to VIRL](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/vSRX%2BVIRL)

## Running With Scissors

If you're exceedingly brave you can try to set up a Vagrant-based topology without an out-of-band management network. It's quite simple to do if you're using VMware virtualization products with Vagrant: you’ll have to find out the IP addresses configured on the management interfaces of Vagrant-managed devices (use **vagrant ssh-config** to get them) and enter those IP addresses into your Ansible inventory file. See [creating Ansible inventory from Vagrant SSH configuration](../Ansible/Ansible_Inventory_Vagrant.html).

Vagrant running on VirtualBox is great fun: it doesn’t use an internal network to communicate with the virtual machines like it does on VMware Fusion/Workstation, but creates a NAT adapter for every VM. While that makes it possible to access all VMs from the host operating system (that’s how **vagrant ssh** works), it's harder to use that adapter to communicate between the VMs like you could in VMware-based environment (although [it can be done](..//Ansible/Running_Ansible_Vagrant_VM.html)) and I'm using it in [this topology](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/EOS-Leaf-and-Spine)).

Inter-VM communication in Vagrant-controlled VirtualBox environments is thus easiest to achieve with an additional internal network (OOB management network). However, Vagrant does not configure the extra interface(s) by default – you have to configure them yourself (for example, using **sudo ifconfig eth1 *ip* netmask *mask*** command on the Ansible VM).

