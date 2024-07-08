---
title: "Use FRR Containers to Learn Routing Protocol Fundamentals"
date: 2023-06-21 06:42:00
lastmod: 2024-07-08 07:34:00
tags: [ BGP, netlab ]
netlab_tag: use
---
An anonymous commenter [asked this highly relevant question](/2023/06/bgp-leak-lab/#1859) about my [Internet routing security lab](/2023/06/bgp-leak-lab/):

> What are the smallest hardware requirements to run the lab?

**TL&DR:** 2 GB RAM, 2 vCPU

Now for the more precise answer (aka "*it depends*").
<!--more-->
The lab has nine routers. If you run them as virtual machines [^MD], each device needs between 256MB (Mikrotik) and 8GB (Cisco IOS XR). Add 2 GB for the host operating system and the virtualization environment[^LT], and we're quickly getting into the 8GB—16 GB ballpark. Also, you should expect every network device to use at least half a CPU core[^ST].

[^MD]: For more details, check out the *netlab* [Supported Platforms](https://netlab.tools/platforms/) page.

[^LT]: Way more if you want to run the lab on your laptop: my Mac consumes 4GB while doing nothing.

[^ST]: Way more during the startup phase, but once the devices reach a steady state, there's no reason they should burn more CPU cycles... which obviously doesn't mean some of them won't. Cisco CSR1000v and Juniper vSRX are probably the worst offenders -- they burn a CPU core constantly checking whether any packets are to be forwarded.

Fortunately, there's another way: Linux containers. Instead of a full-blown virtual machine, every network device gets another copy of the Linux TCP/IP stack and becomes just a set of isolated processes running on top of a shared Linux kernel. 

_netlab_ supports six easy-to-get[^ETG] network-device-as-container implementations[^NCL]: Arista EOS, Cumulus Linux 4.x and 5.x, FRR, Nokia SR-Linux, and VyOS. Downloading Arista cEOS requires registration; all the others can be downloaded from public container registries.

[^ETG]: The condition that automatically excludes most Cisco virtual devices.

[^NCL]: _netlab_ supports [many other platforms](https://netlab.tools/labs/clab/#container-images) packaged as containers, but in those cases, you'd be [running a virtual machine inside a container](https://netlab.tools/labs/clab/#using-vrnetlab-containers), which does not reduce the memory requirements.

I ran the [BGP Route Leaks](https://github.com/ipspace/netlab-examples/tree/master/BGP/Route-Leaks) lab with all of them[^NCL5] and got the following printouts from the **free** command after the lab was started and configured. The relevant column is the **used** column, where you should subtract 1GB (the idle system memory utilization) to get the memory consumed by the lab containers.

[^NCL5]: Excluding Cumulus Linux 5.x because _netlab_ NVUE support is not something to boast about, and you're just wasting memory if you're running Cumulus Linux 5.x and configuring FRR.

{{<cc>}}Idle system (no lab is running){{</cc>}}
```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       1.0Gi        16Gi        19Mi        44Gi        60Gi
Swap:          8.0Gi          0B       8.0Gi
```

{{<cc>}}Arista cEOS{{</cc>}}
```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi        11Gi       4.8Gi       961Mi        45Gi        48Gi
Swap:          8.0Gi          0B       8.0Gi
```

{{<cc>}}Cumulus Linux 4.x container (unofficial image by Michael Kashin){{</cc>}}
```
free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       2.6Gi        11Gi       468Mi        47Gi        58Gi
Swap:          8.0Gi          0B       8.0Gi
```

{{<cc>}}FRR containers{{</cc>}}
```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       1.2Gi        16Gi        20Mi        44Gi        59Gi
Swap:          8.0Gi          0B       8.0Gi
```

{{<cc>}}Nokia SR Linux{{</cc>}}
```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi        12Gi       2.0Gi        29Mi        47Gi        48Gi
Swap:          8.0Gi          0B       8.0Gi
```

{{<cc>}}VyOS{{</cc>}}
```
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            62Gi       2.5Gi        50Gi        39Mi       9.1Gi        58Gi
Swap:          8.0Gi          0B       8.0Gi
```

As you can see, you can choose between three lightweight implementations (Cumulus, FRR, and VyOS) and two heavy hitters (Arista cEOS and Nokia SR Linux). Needless to say, Arista and Nokia have much better configuration capabilities and support more features than the others, but that doesn't matter if you're interested in BGP routing and some simple ingress/egress filters.

You can run network device containers and *containerlab* in an [Ubuntu VM](https://netlab.tools/install/ubuntu-vm/) on Windows or MacOS laptop (even on [Apple Silicon](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/)), but you don't have to unless you need more than 16 GB of RAM. It's much easier (and faster) to [use GitHub codespaces](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/) (where you'd be limited to 4 CPU cores and 16 GB of RAM)

### Revision History

2024-07-08
: * Add VyOS
  * Mention GitHub codespaces as the simplest way to get started
