---
title: Zero-Touch Provisioning with Salt
date: 2020-05-25 07:28:00
tags: [ automation ]
---
Helping a friend of mine figure out the details of using Salt in Zero-Touch-Provisioning environments, [Zach Moody](https://www.linkedin.com/in/zachmoody/) sent me a description of their process, and was kind enough to allow me to turn it into a blog post.
- - -
We follow the same basic ZTP process you would with anything else. Salt drives the parts that interface with the network devices with information from our source-of-truth, NetBox.
<!--more-->
The process starts with some automation that adds a new build into NetBox with nearly everything we need to put the boxes through ZTP. Someone does need to import the MAC addresses we'd expect to see on the DHCP server, but that's mostly just copying and pasting from spreadsheets into NetBox imports. 

When we're ready to kick off ZTP we'll move the device's status in NetBox from _planned_ to _staged_. Every hour or so, our ZTP server looks to NetBox for any devices in the staged state. When it finds any, it configures dhcpd with the hostname, IP, hardware address, and whatever vendor options are needed for that device to get firmware and config. 

We keep a map of the model number to firmware in a pillar and just use the file.managed state to pull that image down from S3 into a directory served by httpd. For the config, we render a minimal bootstrap; just enough to get the box reachable from the other part of Salt that's responsible for managing it in prod (proxy-minions and sproxy) where we send the remainder of the config it needs before accepting traffic.
- - -
For more details explore:

* [Zero-touch provisioning tutorial](https://networklore.com/ztp-tutorial/) by Patrick Ogenstad and his [ZTP presentation](https://my.ipspace.net/bin/list?id=NetAutSol&module=4#M4S3B) from our [Network Automation online course](https://www.ipspace.net/Building_Network_Automation_Solutions).
* [Salt and SaltStack podcast](/2017/04/salt-and-saltstack-on-software-gone-wild/) we recorded with Mircea Ulinic, and his [Using Salt for Event-Driven Automation](https://my.ipspace.net/bin/list?id=NetAutSol&module=8#M8S2) presentation from our automation course.
