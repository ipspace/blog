---
title: "Measuring Virtual Network Device Boot Times"
date: 2023-02-22 06:45:00
lastmod: 2023-03-02 15:13:00
tags: [ automation ]
---
A senior engineer at Juniper Networks wasn't happy with me [mentioning](/2023/02/cisco-ios-bgp-update-delay.html#fn:2) *resource hogs* and *Junos platforms* in the same statement. Instead of engaging in never-ending _angels dancing on pins_ deliberations comparing the virtues of Junos with other network operating systems, I decided to throw a bit of real-life data into the mix -- I [created a simple script](https://github.com/ipspace/netlab-examples/tree/master/timing) that measures:

* The time it takes to execute **vagrant up** to start a single network device.
* The time it takes to deploy simple initial configuration on that device.
<!--more-->

Before going into the details, it's worth acknowledging that the device boot time is not something most customers care deeply about[^NXOS], and thus not something that vendors would invest into. It's just that I get annoyed every single time I have to go and make a sandwich while waiting for my lab to start.

[^NXOS]: Unless you brought down your whole network for a few days reloading your second core Nexus switch before the first one finished its lengthy startup sequence.

Back to the facts. The following table contains the boot time as measured with `netlab up --no-config` (which effectively translates into `vagrant up`) The measured times obviously depend heavily on the underlying hardware, so take them with a grain of salt and consider the relative times (index).
 
| Device      | SW release | Boot time | Index |
|-------------|-----------:|----------:|------:|
|Cumulus Linux| 4.4.0      | 0:31.42   |  100 |
|Cisco IOSv   | 15.6T      | 0:51.44   |  163 |
|Arista EOS   | 4.28.3M    | 1:25.96   |  273 |
|Cisco CSR    | 17.03.04   | 1:38.85   |  314 |
|Cisco NX-OS  | 9.3.10     | 2:52.13   |  547 |
|Juniper vSRX | 21.4R1.12  | 3:14.12   |  617 |
|Cisco IOS XR | 7.4.2      | 4:53.08   |  932 |
{.fmtTable}

**Notes:**

* All network devices apart from Cisco IOSv got [two vCPU cores plus the recommended minimum amount of memory](https://netlab.tools/platforms/#supported-virtualization-providers)[^NR].
* The lab server I was using has 8 cores and 32GB of memory. Nothing else was running on it during the measurement process.
* `vagrant up` exits once it can log into a device with SSH. The boot time is thus the time from the moment the VM is started to the moment SSH server accepts an incoming session. 

Some devices also need a lot of time to figure out what to do with their interfaces: Cisco NX-OS took over five minutes (5:13.35) to boot when I started it with 32 Ethernet interfaces.

But that's not all. A network device has to be configured to be useful. The following table lists the time needed to deploy initial device configuration with `netlab initial`. That command starts an Ansible playbook; a few seconds of the configuration time might be consumed by Ansible, but obviously not more than ~4 seconds (the lowest configuration time) 

| Device      | SW release | Configuration time | Index |
|-------------|-----------:|-------------------:|------:|
|Cumulus Linux| 4.4.0      |       0:04.32 |  100 |
|Cisco IOSv   | 15.6T      |       0:06.01 |  139 |
|Cisco CSR    | 17.03.04   |       0:05.80 |  134 |
|Arista EOS   | 4.28.3M    |       0:07.14 |  165 |
|Cisco NX-OS  | 9.3.10     |       0:14.66 |  339 |
|Cisco IOS XR | 7.4.2      |       0:24.01 |  555 |
|Juniper vSRX | 21.4R1.12  |       1:36.66 | 2237 |
{.fmtTable}

**Notes:**
* `netlab initial` deployed minimal initial configuration, including a loopback interface and one physical interface with an IPv4 address.
* It looks like the SSH server on vSRX starts working way before the device is in a steady state. The configuration time fell down to 45 seconds if I inserted a 120-second delay between lab initialization and initial configuration.

### Containers Are Faster

Frustrated by my obnoxious opinions, the Juniper engineer suggested a workaround that should make Junos shine:

> If you want to run only routing, Juniper cRPD would be a better choice. And will likely beat the pants off any type of cloud, including cumulus, in boot time.

I would love to try out his idea, but it looks like I'm too stupid to be able to download Juniper cRPD. First I was asked to _contact customer care_ after logging in with my Juniper account, then I was asked to update my account. I did that, and was told that the _compliance team_ has to look at my data. The next day my account stopped working. I tried to reset the password and the new password was accepted but didn't work when I tried to log in. A few days later the new password still didn't work and the password reset page produced a very helpful error message: _Invalid User Status. Please contact customer care for further assistance_ At that point I gave up; if a vendor web portal team can't get their act together, I have better things to do with my life.

Anyway, the last time I was able to test cRPD it had minimal data plane awareness, making it impossible to configure it with Ansible. That made it completely useless as a potential  _netlab_ network device.

It's worth noticing that all other container solutions I tried out have a configurable data plane, and can be configured in exactly the same way using the same tools as virtual machines or physical devices. While Arista's implementation [has a few quirks](/2022/03/dataplane-quirks-virtual-devices/), Cumulus Linux container works surprisingly well (although [it cannot handle MLAG](https://containerlab.dev/manual/kinds/cvx/)), and the FRR container managed to run MPLS and L3VPN out of the box.

Not surprisingly, the container start times are much lower than the VM start times. Here are the results for the three containers I have installed on my lab server:

| Device      | SW release | Boot time | Configuration |
|-------------|-----------:|----------:|--------------:|
|Arista EOS   | 4.27.2F    | 0:25.09   |       0:07.32 |
|Cumulus Linux| 5.0.6      | 0:01.16   |       0:03.29 |
|FRR          | 8.4.0      | 0:01.08   |       0:03.09 |
{.fmtTable}

Somehow I doubt that cRPD (if I ever manage to download it) would _beat the pants off_ 1 second FRR or Cumulus Linux container start time.

### Reproducing the Results

It's trivial to reproduce the results if you disagree with my measurements:

* [Install netlab](https://netlab.tools/install/)
* [Build Vagrant boxes](https://netlab.tools/labs/libvirt/) for the networking devices you want to test
* Download the [measuring script](https://github.com/ipspace/netlab-examples/tree/master/timing) into an empty directory and execute `./timing.sh <list-of-devices>`

If you just want to check the initial device configurations:

* Install netlab
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/timing/topology.yml) used by the measurement script into an empty directory
* Execute `netlab create -d <device>` followed by `netlab initial -o` and inspect the `config` subdirectory.

[^NR]: I'm not rich enough to buy the amount of RAM some vendors think their devices need.

### Revision History

2023-03-02
: Documented drastic increase in boot time for Nexus OS VM with many interfaces.
