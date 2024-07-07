---
title: "Cumulus Linux Network Command Line Utility (NCLU)"
date: 2022-09-29 06:07:00
tags: [ Cumulus Linux ]
---
While [ranting about Linux data plane configuration](/2022/09/linux-data-plane-configuration/), I mentioned an interesting solution: Cumulus Linux Network Command Line Utility (NCLU), an attempt to make Linux networking more palatable to more traditional networking engineers.

NCLU is a simple wrapper around *ifupdown2* and *frr* packages. You can execute **net add** and **net del** commands to set or remove configuration parameters[^Junos], and NCLU translates those commands into changes to corresponding configuration files.
<!--more-->
[^Junos]: Similarly to how you can add stuff to device configuration with Junos

For example, to change the MTU size on interface **swp1**, you could edit the `/etc/network/interfaces` file and execute `ifreload -a`, or execute `net add interface swp1 mtu` followed by `net apply`.

Like on Junos or Arista EOS[^CS], the changes made with **net add** and **net del** commands are not executed immediately but collected in a staging area that you can inspect with the **net pending** command. I used that feature extensively when developing the *netlab* Cumulus Linux configuration templates. I would:

[^CS]: When you're using configuration sessions

* Figure out what I need to change
* Execute the corresponding **net add** command
* Use **net pending** to see how that command translates into changes to configuration files
* Fix my configuration templates and use **net abort** to discard the changes

Continuing the MTU example:

```
$ net add interface swp1 mtu 1600
$ net pending
--- /etc/network/interfaces	2021-05-25 16:21:56.000000000 +0000
+++ /run/nclu/ifupdown2/interfaces.tmp	2022-09-24 16:14:04.467093808 +0000
@@ -1,13 +1,18 @@
 # interfaces(5) file used by ifup(8) and ifdown(8)
 auto lo
 iface lo inet loopback

+auto swp1
+iface swp1
+    bridge-access 1000
+    mtu 1600
+
 auto mgmt
 iface mgmt
     vrf-table auto
```

NCLU does have a glitch or two. For example, I'm using a set of interface configuration files in `/etc/network/interfaces.d` directory, and NCLU cannot change those files. It does extract the current interface configuration (probably using `ifquery` command) and makes changes to it in `/etc/network/interfaces`, so it's trying to do the best it can -- I am to blame for trying to juggle a bunch of square pegs when the tool supports a single round hole.

NCLU also supports a bunch of **show** commands so you don't have to deal with a combo of FRR commands executed in `vtysh` and `ip` commands executed in `bash`.

The only major issue I have with NCLU: someone in their infinite wisdom decided to kill it. While the **net** command is still available in Cumulus Linux 5.x, you cannot use it to configure the box, you're forced to use the NVIDIA User Experience (more about that wonderful experience in another blog post).

On a slightly sarcastic note, maybe that doesn't matter anyway. Cumulus Linux 5.x is [supported](https://www.nvidia.com/en-us/networking/ethernet-switching/hardware-compatibility-list/) only on Mellanox switches. The Mellanox/NVIDIA acquisition transformed a promising Linux-based operating system running on a dozen brands of whitebox and britebox into yet another NOS running on niche hardware. Great job!
