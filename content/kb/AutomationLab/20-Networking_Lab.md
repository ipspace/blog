---
kb_section: AutomationLab
minimal_sidebar: true
title: Networking Lab
url: /kb/AutomationLab/20-Networking_Lab/
---
You could build a physical or a virtual networking lab, or use a third-part virtual lab like [Network To Code labs](https://labs.networktocode.com/).

The only requirement when building non-local lab (be it using physical gear or hosted virtual lab) is to have SSH access from your host (and VMs running within it) to the networking devices. When working with physical devices you might want to use out-of-band management network for SSH access in case you badly mess up device configurations.

Still keen on building your own virtual lab? Keep reading...

## Selecting Virtual Lab Environment

You can build your virtual networking lab in a number of ways. You could decide to run the whole setup on your laptop (in which case you might be limited by the amount of RAM you can squeeze into it - many networking devices are resource hogs), buy a dedicated server to run the virtual lab on ([Intel NUC](https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html) seems to be an interesting option), or even run the whole thing in the cloud.

Whatever you do, you'll need a virtualization environment, and images for network device virtual machines. Some attendees of the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course decided to use ESXi and create virtual machines from ISO images, others use GNS3 or EVE-NG, Cisco VIRL is an interesting option if you're focused on Cisco devices and don't want to get into the hassles of obtaining semi-illegal device images...

## Finding or Building Vagrant Boxes

If you decide to build a virtual networking lab on your laptop, consider Vagrant. Building a networking lab with Vagrant has never been easier - Arista, Cumulus and Juniper provide their software in Vagrant box format ready to be deployed within a Vagrant environment:

- [Juniper Vagrant boxes](https://app.vagrantup.com/juniper/)
- [Using vEOS with Vagrant and VirtualBox](https://eos.arista.com/using-veos-with-vagrant-and-virtualbox/)
- [Using Cumulus VX with Vagrant](https://docs.cumulusnetworks.com/display/VX/Using+Cumulus+VX+with+Vagrant)

Cisco is still a bit skittish - [IOS-XRv Vagrant box seems to be in private beta](https://xrdocs.io/application-hosting/tutorials/iosxr-vagrant-quickstart) and you have to [use a pretty convoluted process](http://binarynature.blogspot.si/2016/04/cisco-iosv-vagrant-box-for-vmware-fusion.html) to create your own Vagrant box from IOSv image or [CSR 1000v](https://codingpackets.com/blog/cisco-csr-vagrant-box-install/). To be fair, Juniper is no better when it comes to vMX.

## Building Your Own Vagrantfile

Building a Vagrantfile describing your lab topology is the biggest hurdle you'll face when building a networking lab with Vagrant. Vagrantfile is really Ruby source code and thus a bit hard to create/modify if you're not at least vaguely familiar with programming languages. Here are two approaches that you might find easier to work with:

- Specify your topology in a YAML file - use the Vagrantfile from [YAML-with-Vagrant](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/YAML-with-Vagrant) directory.
- Specify your topology as a graph in a DOT file - Cumulus Networks provides a [DOT-to-Vagrant conversion tool](https://github.com/cumulusnetworks/topology_converter).

I also [created several sample topologies](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies) to help you get started. They include:

- [Ansible VM running on VMware desktop virtualization product](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/VIRL) together with VIRL
- [Ansible VM and Juniper vSRX running on VMware desktop virtualization product](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/vSRX%2BVIRL) together with VIRL
- [Ansible VM and a leaf-and-spine fabric built from four Arista vEOS switches](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies/EOS-Leaf-and-Spine)
