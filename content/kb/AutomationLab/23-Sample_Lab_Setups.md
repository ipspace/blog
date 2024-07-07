---
kb_section: AutomationLab
minimal_sidebar: true
title: Sample Lab Setups
url: /kb/AutomationLab/23-Sample_Lab_Setups/
---
Explore what some of your fellow course attendees did in the past. I included links to their Git repositories or blog posts in the following list, and you might still find them in our Slack team and ask questions about their setup. 

Most of them used VIRL, EVE-NG, or GNS3 (details below); here are a few outliers:

- Chris Crook [built vQFX10K leaf-and-spine topology](https://github.com/ctopher78/network-automation-course/blob/master/Homework2/lab-provision/README.md)
- Daniel Teycheney [used Intel NUC to build an Arista vEOS lab](https://github.com/writememe/BlgNetAutoSol/blob/master/Lab/topology.txt)
- Jean-Baptiste Broguière built a lab [using Arista EOS containers](https://github.com/JB-BR/BuildingNetworkAutomationSolutions/tree/master/GettingStarted).

## VIRL and CML Solutions

- Andy Flint [deployed VIRL on Intel NUC](https://github.com/andyflint/network-automation-solution-examples/tree/master/01_getting_started)
- Stephan Lüscher [combined VIRL running in VMware Workstation with Ansible running in LXD container on a Linux host](https://gitlab.com/tepene/netautsol_labsetup/tree/v1.0), found (in his own words) "_that setup is not for the faint-hearted_", and [migrated from VIRL to EVE-NG](https://gitlab.com/tepene/netautsol_labsetup/tree/v2.0)
- Graeme Danielson [created a lab in Cisco CML using a Ubuntu jumphost](https://github.com/gdanielson/ipspace-bnas)

## EVE-NG Solutions

- Erik Ruiter [decided to run EVE-NG and Ansible VM on ESX host](https://github.com/erikruiter2/ansible_lab)
- Martijn van Overbeek [built a huge topology on EVE-NG-Pro running under VMware Workstation Professional](https://github.com/martijnvanoverbeek/NETAUTOMATION/tree/master/NETAUTOMATION/LABSETUP)
- Jaap de Voos [used Proxmox hypervisor to run EVE-NG and Ubuntu on pretty powerful server](https://github.com/jwdevos/netauto/tree/master/getting-started) and [described how to get it all up and running](https://www.lab-time.it/2018/09/22/building-a-network-automation-lab/)
- Martin Ferfecky used [EVE-NG to build vMX lab](https://github.com/ferfemar/ipspace-training/tree/master/hw-1-lab-test)... and included UNL topology file in his repository so you can recreate what he did.

## GNS3 Solutions

- augustsix [used GNS3 running in VMware Player](https://github.com/augustsix/network_automation/tree/master/1.Build_The_Lab)
- Erik Auerswald [created a large lab in Dynamips](https://github.com/auerswal/bnas2018/tree/master/hw1-the_lab)
- Eder Gernot [used GNS3 on ESXi](https://github.com/edergernot/ederg_lab)
- David Varnum used GNS3 to build a [full-blow Arista EOS leaf-and-spine fabric including attached servers](https://overlaid.net/2019/02/19/arista-bgp-evpn-ansible-lab/)
- Daniel Macuare used GNS3 to build [lab for CCNP TSHOOT course](https://github.com/danielmacuare/CCNP-TSHOOT-GNS3#assignment-1---build-your-own-network-automation-lab)
