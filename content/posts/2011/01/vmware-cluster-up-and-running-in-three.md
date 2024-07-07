---
date: 2011-01-27 06:44:00.001000+01:00
tags:
- data center
- virtualization
title: 'VMware Cluster: Up and Running in Three Hours'
url: /2011/01/vmware-cluster-up-and-running-in-three/
cdate: 2022-07-10
comment: |
  This blog post was written in early 2011. Most of the products mentioned in it are long obsolete, but it's still worth noting the major difference between configuring infrastructure through CLI (or any other form of text configurations) or GUI.
  
  A decade later, I would also try to use some sort of Python-based templating (or Ansible) instead of Notepad-based copy/paste/search/replace.
---
A few days ago I wanted to test some of the new networking features VMware introduced with the vShield product family. I almost started hacking together a few old servers (knowing I would have wasted countless hours with utmost stupidities like trying to get the DVDs to boot), but then realized that we already have the exact equipment I need: a UCS system with two Fabric Interconnects and a chassis with five blade servers -- the lab for our Data Center training classes (the same lab has a few Nexus switches, but that's another story).

I managed to book lab access for a few days, which was all I needed. Next step: get a VMware cluster installed on it. As I never touched the UCS system before, I asked Dejan Strmljan (one of our UCS gurus) to help me.
<!--more-->
09:00 -- if you want to experience an agile UCS deployment (\@bradhedlund and \@omarsultan should be so proud of me ;), Dejan is the guy you need. He'd been developing our UCS labs and had complete UCS configuration nicely split into templates. Twenty minutes of cut-and-paste and search-and-replace editing and our UCS configuration was ready to go... but we still had to wait for our storage guy.

09:30 -- Marko (our storage guy) arrives to create the LUNs I need for my servers. He has to deal with a "fantastic" GUI interface. Thousands of clicks (and a carpal tunnel syndrome) later he's done. I could enjoy my morning coffee and a donut in the meantime. Luckily I only needed a few LUNs or I would have gotten fat while he was frantically clicking away.

10:00 -- The LUNs are ready. Dejan copies the configs into UCS CLI, checks the configuration through the UCS manager, opens console windows to the servers and starts them. Total time spent: 5 minutes (mostly due to an unexpected change of context caused by the particular configuration sequence used in our UCS configuration). Not bad compared to the thousand-click storage experience.

The servers happily boot off Dejan's local copy of the ESX ISO image (another UCS goodie -- its Java console window applet allows you to mount a local ISO image as the server's CD-ROM) and start the ESX install process.

Most of the time is spent transferring the ISO image -- our UCS is in the demo part of the network, which is strictly isolated from the production (where we're sitting) by a rate-limiting firewall (supposedly someone managed to spill a network meltdown from the demo network into the production one a while ago).

10:30 -- ESX installs are done. Time to create a Windows VM and install vCenter. Yet again, most of the time is spent transferring the images to the shared VMFS file system. We have a decent library of prebuilt VM images and I could have used one of them (probably even with vCenter already installed), but I wanted to have a totally clean Windows install. I also wanted to use the latest SW release freshly downloaded from VMware. Sometimes you have to pay the price for your stubbornness.

11:30 -- vCenter is up and running. Adding ESX servers to the cluster. Fighting with Fault Tolerance. Somehow it works better if you have a DNS server; we have none in the demo network. Giving up on FT; it will have to wait for better times. In the meantime, I managed to transfer Fedora 14 ISO image to the shared VMFS LUN. Creating the first client VMs installing Fedora.

12:00 -- Fedora client VM is up and running.

I have zero hands-on experience with blade server platforms from other vendors, so it's a bit hard to guess how good we were... but I can tell you I was mightily impressed. Thanks again, Dejan!
