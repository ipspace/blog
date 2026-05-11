---
title: "Measuring Virtual Network Device Boot Times"
date: 2023-02-22 06:45:00
lastmod: 2026-05-11 17:58:00+0200
tags: [ automation ]
---
A senior engineer at Juniper Networks wasn't happy with me [mentioning](/2023/02/cisco-ios-bgp-update-delay/#fn:2) *resource hogs* and *Junos platforms* in the same statement. Instead of engaging in never-ending _angels dancing on pins_ deliberations comparing the virtues of Junos with other network operating systems, I decided to throw a bit of real-life data into the mix -- I [created a simple script](https://github.com/ipspace/netlab-examples/tree/master/timing) that measures:

* The time it takes to start a single network device and wait for it to be configurable.
* The time it takes to deploy a simple initial configuration on that device.
<!--more-->

Before going into the details, it's worth acknowledging that the device boot time is not something most customers care deeply about[^NXOS], and thus not something that vendors would invest in. It's just that I get annoyed every single time I have to make a sandwich while waiting for my lab to start.

[^NXOS]: Unless you brought down your whole network for a few days by reloading your second core Nexus switch before the first one finished its lengthy startup sequence.

Back to the facts. The following table shows the time required for a network device to become configurable. It's measured as the time it takes `netlab up --no-config` (which effectively translates to `vagrant up` or `containerlab deploy`) and `netlab initial --ready` (wait for SSH server to start and interfaces to appear). The measured times obviously depend heavily on the underlying hardware, so take them with a grain of salt and consider the relative times (index).
 
| Device | SW release | Boot time | Index |
|----------------------|-------------|--------:|----:|
| Cisco IOSv           | 15.9(3)     | 00:54.5 | 100 |
| Arista vEOS          | 4.34.2F     | 01:17.3 | 142 |
| vJunos-switch (QFX)  | 23.4R2-S2.1 | 01:39.3 | 182 |
| vJunos-router (MX)   | 23.4R2-S2.1 | 01:39.7 | 183 |
| Cisco Catalyst 8000v | 17.16.01a   | 01:49.6 | 201 |
| Cisco 8000v (IOS XR) | 24.4.1      | 02:48.1 | 308 |
| Cisco Nexus OS       | 9.3.10      | 03:21.7 | 370 |
{.fmtTable}

**Notes:**

* Junos, IOS XR, and Nexus OS devices were run as virtual machines within containers (using *vrnetlab*-built containers)
* All network devices got enough CPU cores plus the [recommended minimum amount of memory](https://netlab.tools/platforms/#supported-virtualization-providers)[^NR].
* The lab server I was using has 16 cores and 64GB of memory. Nothing else was running on it during the measurement process.

Some devices also take a long time to figure out what to do with their interfaces: Cisco NX-OS took over five minutes to boot when I started it with 32 Ethernet interfaces.

But that's not all. A network device has to be configured to be useful. The following table lists the time needed to deploy the initial device configuration with `netlab initial`. That command starts an Ansible playbook; a few seconds of the configuration time might be consumed by Ansible, but obviously not more than ~4 seconds (the lowest configuration time) 

| Device | SW release | Configuration time | Index |
|----------------------|-------------|--------:|----:|
| Cisco IOSv           | 15.9(3)     | 00:04.9 | 100 |
| Cisco Catalyst 8000v | 17.16.01a   | 00:05.2 | 106 |
| Cisco 8000v          | 24.4.1      | 00:07.6 | 154 |
| vJunos-switch (QFX)  | 23.4R2-S2.1 | 00:07.8 | 158 |
| Arista vEOS          | 4.34.2F     | 00:08.0 | 164 |
| vJunos-router (MX)   | 23.4R2-S2.1 | 00:08.3 | 168 |
| Cisco Nexus OS       | 9.3.10      | 00:10.6 | 215 |
{.fmtTable}

**Notes:**
* `netlab initial` would often take longer because it has to wait for devices to become configurable (not just started). The timing test ran `netlab initial` after the devices were guaranteed to be configurable (as reported by previously-executed `netlab initial --ready`)
* `netlab initial` deployed a minimal initial configuration, including a loopback interface and one physical interface with an IPv4 address.

### Containers Are Faster

Frustrated by my obnoxious opinions, the Juniper engineer suggested a workaround that should make Junos shine:

> If you want to run only routing, Juniper cRPD would be a better choice. And will likely beat the pants off any type of cloud, including cumulus, in boot time.

{{<long-quote>}}
I tested cRPD ages ago, and it couldn't even report its interfaces. At the time I wrote this blog post, I found it impossible to download cRPD (let's say that the behavior of Juniper's website was suboptimal).

In the meantime, cRPD has improved significantly, got a working data plane, and is now one of my favorite platforms.
{{</long-quote>}}

Not surprisingly, the container start times are much lower than the VM start times. Here are the results for the native containers I have installed on my lab server:

| Device | SW release | Boot time | Config time |
|----------------------|-----------|--------:|--------:|
| FRRouting            | 10.6.1    | 00:02.0 | 00:00.3 |
| Juniper cRPD         | 24.4R1.9  | 00:07.4 | 00:01.7 |
| Nokia SR Linux       | 26.3.2    | 00:11.6 | 00:01.5 |
| Arista cEOS          | 4.35.2F   | 00:20.9 | 00:02.2 |
| Nokia SR-SIM (SR-OS) | 25.7.R1   | 00:23.1 | 00:03.9 |
| Cisco IOL            | 17.16.01a | 00:29.3 | 00:07.1 |
| Cisco IOS XRd        | 25.2.1    | 00:34.6 | 00:06.0 |
{.fmtTable}

cRPD still can't _beat the pants off_ the 2-second FRR boot time, but it's one of the fastest-to-boot containers out there.

### Reproducing the Results

It's trivial to reproduce the results if you disagree with my measurements:

* [Install netlab](https://netlab.tools/install/)
* [Build Vagrant boxes](https://netlab.tools/labs/libvirt/) and [containers](https://netlab.tools/labs/clab/) for the networking devices you want to test
* Download the [measuring script](https://github.com/ipspace/netlab-examples/tree/master/timing) into an empty directory and execute `bash timing.sh <list-of-devices>`. To measure containers, do `NETLAB_PROVIDER=clab bash timing.sh <list-of-devices>`

If you just want to check the initial device configurations:

* Install netlab
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/timing/topology.yml) used by the measurement script into an empty directory
* Execute `netlab create -d <device>` followed by `netlab initial -o` and inspect the `config` subdirectory.

[^NR]: I'm not rich enough to buy the amount of RAM some vendors think their devices need.

### Revision History

2026-05-11
: * Removed Cumulus from test results for [obvious reasons](/2025/02/goodbye-cumulus-community/)
  * Repeated the measurements with new devices and numerous containers

2023-03-02
: Documented a drastic increase in boot time for Nexus OS VM with many interfaces.
