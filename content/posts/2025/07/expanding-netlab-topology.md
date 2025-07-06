---
title: "Expanding a Running Netlab Topology"
date: 2025-07-07 08:11:00+0200
tags: [ netlab ]
netlab_tag: guidelines
---
One of the happy _netlab_ users sent me an interesting challenge:

* He's built a large lab and added tons of extra configuration to the lab devices.
* Afterwards, he realized he'd like to add a few more devices to the lab and was worried about losing all the changes he had made.

Unfortunately, you cannot add new devices to an already-running lab. You must shut down the lab, change the topology description, and start a new lab. However, there are things you can do to preserve the extra work you already did:
<!--more-->
* Save the current device configurations with **netlab collect -o _folder_**. Make sure you specify an output folder; by default, _netlab_ saves the configurations in the **config** folder, which the **netlab down \-\-cleanup** command removes..
* Check whether you can load the saved configurations with **netlab config *your_folder* \-\-check** (the **\-\-check** option is passed to Ansible)
* Shut down the lab, change the topology file, and restart the lab.
* Add the saved configurations to the lab devices with **netlab config _your_folder_**. The command will fail for all devices you added to the lab, but should _merge_ the saved configurations with those generated from the modified lab topology.

{{<note warn>}}
Whatever changes you make to the lab topology, do not remove links connecting existing devices and add new links to the end of the **links** list.

Merging saved configurations to devices with a different set of interfaces is a nice recipe for a total mess.
{{</note>}}

The above procedure definitely works on most Cisco platforms (IOS/XE, NX-OS, IOS-XR) and Arista EOS, Aruba AOS, and Dell OS10; it most probably works on Juniper platforms. Here's what the actual limitations are:

* You have to get the whole device configuration with **netlab collect**
* **netlab collect** must save the device configuration in a single text file
* **netlab config** must be able to take that text file and push it as a new configuration to the device.

I never tested VyOS or Mikrotik, but I know you'll experience problems in these scenarios:

* You cannot save the Linux or Fortinet configurations ([details](https://netlab.tools/platforms/#configuration-deployments)).
* You cannot save the data-plane configuration for FRR.
* You can reload only the FRRouting configuration onto FRR, Cumulus Linux 4.x, and SoNIC devices.
* Due to the way _netlab_ configures Nokia SR Linux and Nokia SR-OS, you cannot use the saved device configuration with the **netlab config** command.

Finally, you could use **netlab config \-\-reload** to reload the saved configurations to Nokia devices, but then you'd lose all the changes _netlab_ made to configure the links and routing protocol parameters between the already-existing and the new devices. You could, however, run another **netlab initial** command (hopefully limited to Nokia devices; see below) after reloading the saved configurations.

{{<note info>}}
_netlab_ defines an Ansible group for every device type, and the **netlab config** command passes extra arguments to Ansible, allowing you to merge saved configurations on some devices and reload them on others. For example:

```
$ netlab config saved --limit eos,iosv,iol
$ netlab config --reload saved --limit srlinux
$ netlab initial --limit srlinux
```
{{</note>}}

Fortunately, the networking engineer who wanted to expand his lab used Arista EOS devices, and the migration worked flawlessly.
