---
date: 2018-05-03T07:19:00.000+02:00
tags: [ automation ]
title: 'Automation Win: Zero-Touch Provisioning'
---
Listening to the networking vendors it seems that zero-touch provisioning is a no-brainer … until you try to get it working in real life, and the device you want to auto-configure supports only IP address assignment via DHCP, configuration download via TFTP, and a DHCP option that points to the configuration file.

As Hans Verkerk discovered when he tried to [implement zero-touch provisioning with Ansible](https://github.com/hans-vvv/NetAutLab) while attending the [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) course you have to:
<!--more-->

-   Use a DHCP server to assign IP addresses to devices, combined with a TFTP server to push initial configuration to newly-attached devices;
-   Detect a new IP address has been assigned by DHCP server;
-   Find the MAC address associated with the IP address if you want to provision devices based on their MAC address. He used ARP cache to find it;
-   Generate SSH keys on the device and add those keys to **known\_hosts** file (you could also turn off key checking… maybe not such a great idea);
-   Generate the final device configuration;
-   Push the configuration to the device.

[All his playbooks are on Github](https://github.com/hans-vvv/NetAutLab) – explore and adapt them, and submit a pull request when you improve them ;)

{{<note update>}}In October 2020 Hans [ported his ZTP solution to Nornir](https://github.com/hans-vvv/NetAutLab/tree/master/nornir-ztp).{{</note>}}

**Notes:**

-   Before doing anything else, go and read the awesome [Zero-Touch Provisioning DIY Tutorial](https://networklore.com/ztp-tutorial/) by Patrick Ogenstad.
-   Some vendors neatly solved the problem with automated procedures that can do anything from figuring out where their device is in the network to upgrading software and downloading tailored configuration. Similar to [network automation RFP requirements](/2016/10/network-automation-rfp-requirements/), make ease of zero-touch provisioning using a well-documented standards-based approach a mandatory requirement when buying the next batch of hardware;
-   If you have to provision Cisco Catalyst switches, check out the [FreeZTP server](https://github.com/convergeone/freeztp);
-   I know someone who solved the same problem with Salt – have to persuade him to talk about it one of these days.

*This blog post was initially sent to the subscribers of my SDN and Network Automation mailing list. *[*Subscribe here*](http://www.ipspace.net/Subscribe/Five_SDN_Tips)*.*
