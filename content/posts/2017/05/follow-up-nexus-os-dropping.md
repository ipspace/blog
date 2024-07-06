---
cli_tag: challenge
date: 2017-05-08 09:30:00+02:00
series:
- cli
title: 'Follow-up: Nexus-OS Dropping Configuration Commands'
url: /2017/05/follow-up-nexus-os-dropping.html
tags: [ automation ]
---
Not long after I published the [*let's drop some configuration commands*](/2017/04/lets-drop-some-random-commands-shall-we.html) rant I got a very nice email from [Nicolas Delecroix](https://www.linkedin.com/in/nicolasdelecroix/), Technical Marketing Engineer in Cisco INSBU, effectively saying "*Would you have time for a short WebEx call to discuss the root cause of the problem and what we did to fix it*?"

Of course I agreed and here's what they told me:
<!--more-->
-   They were able to reproduce the problem;
-   The drops were caused by a very old bug in Linux TTY device driver [introduced in 2009](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3a54297478e6578f96fd54bf4daa1751130aca86), [discovered in Ubuntu \~4 years ago](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1208740) and present in [all Linux distributions](https://lkml.org/lkml/2013/7/25/205) with kernels between 2.6.31 and 3.11.0.

{{<note>}}On Linux-based platforms the router configuration process is usually run as a regular process within a login shell, which means that the path your data has to take goes through ssh server, kernel TTY driver (to make SSH connection appears as just another VT100 terminal), and finally the user process.{{</note>}}

-   The bug was sitting in NX-OS for years, but got more visible due to shift to model-based device configuration architecture that added some delay in the configuration path.
-   They couldn't upgrade the Linux kernel used by Nexus-OS (currently 3.4.91) but backported the bug fix into TTY device driver used by Nexus-OS.
-   The fixed TTY driver will ship with Nexus OS releases 7.0(3)I6(1) and 7.0(3)I4(7). Nicholas told me they're targeting to ship both releases before end of May.

Now that we know what the problem is, it's easy to figure out the workarounds. They recommended:

-   Copy configuration file to the device and then use **copy** ***file*** **running-config**
-   Use NX-API

These two should also work:

-   Use **scp** ***file router*:running config**
-   Use an **expect** script that waits for prompt before sending the next command.

Of course I had to snoop around a bit and found that:

-   The bug is easy to reproduce in **bash** and has nothing to do with router configuration.
-   The bug is causing large pastes (5K or more) to fail in any program that uses **readline** (the library that handles line editing) or anything similar, and is thus present on any server or network device running Linux with affected Linux kernel.
-   Unless a device vendor backported the fix into the Linux TTY driver they're using (it seems Ubuntu developers decided to do this as well) every device running affected Linux kernel might experience the same behavior.

If you're running a network device that runs on top of a Linux kernel, it's relatively easy to get the kernel version: go into shell, type **uname --a**... and let me know what you find out ;)

Finally, I'd like to thank again Nicholas and the Cisco INSBU engineers for an extremely professional approach to this problem.
