---
title: "How Does Netlab Deal with Server Reboots?"
date: 2024-10-24 08:15:00+0200
tags: [ netlab ]
netlab_tag: guidelines
pre_scroll: True
---
Now and then, someone asks how *[netlab](https://netlab.tools/)* deals with reboots (or power failures or crashes) of the server it's running on.

**TL&DR:** It doesn't. However...

*netlab* is a CLI command that acts as an umbrella orchestration layer for Vagrant and Containerlab. It does not run as a cron job, init script, or service and thus cannot be invoked when a server is booted.
<!--more-->
However, *netlab* uses a simple file-based locking mechanism that should stop a user from:

* Starting a second lab in the directory where another lab is already running[^CD]
* Starting a second lab instance with the same set of system parameters[^DAD]. You must use the [**multilab** plugin](https://netlab.tools/plugins/multilab/) to run multiple lab instances on the same server.

[^CD]: Cleaning up that mess is a Mission Impossible. I learned the hard way why *netlab* needs a locking mechanism.

[^DAD]: That could result in virtual machines from different lab instances having the same management IP address. Not a good idea. At least it's not too hard to clean up.

The locking files are not removed after a system reboot. To remove them, you must "shut down" the lab with **netlab down** (even though it's no longer running). That command tells Vagrant or Containerlab they should remove the virtual machines or containers, resulting in a clean system[^FORCE]. After the cleanup, you can restart the lab with **netlab up**.

[^FORCE]: Sometimes, the underlying virtualization system might dislike the idea of *netlab* telling it to shut down stuff that is not running. Use **netlab down --force** if needed.

### But I Don't Want to Lose My Work

Oh, well, if you insist ;) You can try to save the day *if you're using virtual machines*.

The VM definitions and virtual disks are not lost when the server reboots. For example, this is what you will see after a reboot if you were running a lab with two Arista EOS virtual machines:

```
$ netlab status
Lab default in /home/pipi/net101/tools/X
  status: configuration deployment complete
  provider(s): libvirt

┏━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ node ┃ device ┃ image               ┃ mgmt IPv4       ┃ connection  ┃ provider ┃ VM/container ┃ status  ┃
┡━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ r1   │ eos    │ arista/veos:4.28.3M │ 192.168.121.101 │ network_cli │ libvirt  │ X_r1         │ shutoff │
├──────┼────────┼─────────────────────┼─────────────────┼─────────────┼──────────┼──────────────┼─────────┤
│ r2   │ eos    │ arista/veos:4.28.3M │ 192.168.121.102 │ network_cli │ libvirt  │ X_r2         │ shutoff │
└──────┴────────┴─────────────────────┴─────────────────┴─────────────┴──────────┴──────────────┴─────────┘
```

You could restart the virtual machines with **vagrant up**, but nobody would [tweak the Linux bridges to pass IEEE 802.1 frames](https://blog.ipspace.net/2020/12/linux-bridge-lldp/). 

However, if you execute **netlab up --snapshot**, you tell *netlab* to bypass its locking logic[^LL] and start the lab without further questions. Even better, if you add the **--no-config** flag, *netlab* won't try to (re)configure the lab. Assuming you saved the device configuration, you'll be as close as possible to the state you had before the disaster.

[^LL]: The **netlab up --snapshot** command reads the lab topology from the transformed snapshot file, usually created simultaneously with the Vagrant and Containerlab configuration files. Assuming that you can tell Vagrant or Containerlab to (re)start existing stuff is thus relatively safe.

Containers are a different story. They do not have persistent storage, so you cannot expect them to retain device configuration across failures or reboots. Even worse, **containerlab** complains that the containers already exist; it wants to see the **--reconfigure** flag to stop and redeploy them. Cleaning up the artifacts with **netlab down** and starting the lab from scratch seems to be the only option.

**Notes:**

* You can use **netlab restart** instead of **netlab down** followed by **netlab up**.
* It looks like it's OK to use the containerlab **--reconfigure** flag regardless of the lab state; we might add this functionality in the next *netlab* release. I promise to update this blog post if we improve the restart functionality ;)