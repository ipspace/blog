---
title: "Testing bgpipe with netlab"
date: 2024-08-21 06:46:00+0200
tags: [ netlab, BGP ]
netlab_tag: use
---
Ever since [Pawel Foremski](https://ripe88.ripe.net/speakers/pawel-foremski/) talked about [BGP Pipe @ RIPE88 meeting](https://ripe88.ripe.net/archives/video/1365/), I wanted to kick its tires in _[netlab](https://netlab.tools/)_. [BGP Pipe](https://github.com/bgpfix/bgpipe/?tab=readme-ov-file) is a Go executable that runs under Linux (but also FreeBSD or MacOS), so I could add a Linux VM (or container) to a _netlab_ topology and install the software after the lab has been started. However, I wanted to have the BGP neighbor configured on the other side of the link (on the device talking with the BGP Pipe daemon).

I could solve the problem in a few ways:
<!--more-->
* Use an existing BGP daemon like BIRD and tweak its settings and the configuration files;
* Start the lab topology without BGP and configure BGP manually;
* Define a new device and tell _netlab_ it supports BGP.

However, there's [another neat trick](https://github.com/bgplab/bgplab/blob/master/basic/1-session/topology.1.6.4.yml) (that I [used in the very first BGP lab exercise](https://bgplabs.net/basic/1-session/)): define **bgp** to be a generic node attribute without any data validation. That allows me to configure BGP AS on a device that does not support BGP, tricking _netlab_ into configuring the BGP neighbors on adjacent devices.

Here's the [lab topology I used](https://github.com/ipspace/netlab-examples/blob/master/BGP/bgpipe/topology.yml):

{{<printout>}}
defaults.attributes.node.bgp:

provider: clab
defaults.devices.linux.group_vars.docker_shell: bash

nodes:
  rtr:
    module: [ bgp ]
    device: frr
    bgp.as: 65000
  probe:
    device: linux
    image: netlab/bgpipe:latest
    bgp.as: 65100

links:
- rtr:
  probe:
{{</printout>}}

The solution's crux is the first line: tell _netlab_ any node can have **bgp** attributes (otherwise, _netlab_ requires a node with **bgp** attributes to use the BGP configuration module).

The rest of the configuration should be self-evident if you used _netlab_ in the past:

* The lab is using containers (line 3)
* We should be using **bash** as the shell on the Linux containers (line 4)
* The lab has a router running BGP on FRRouting. It has BGP AS number 65000 (lines 7-10)
* The other node in the lab is a Linux host using the `netlab/bgpipe:latest` container image. It's expected to have BGP AS number 65100 (lines 11-14)
* The lab topology has a single link with both nodes attached to it.

I could have used the Ubuntu container image and installed **bgpipe** every time the lab started, but I decided it would be better to build a new container image (`netlab/bgpipe:latest`) and use that. The [`Dockerfile`](https://github.com/ipspace/netlab-examples/blob/master/BGP/bgpipe/Dockerfile) is trivial:

* It takes the baseline Ubuntu image
* It installs a few utilities
* It downloads **bgpipe** executable into `/usr/local/bin`[^FS]

[^FS]: Hint: downloading an executable from the Internet and running it as root is probably not a good security practice. At least I can pretend I downloaded it from a reputable site (GitHub).

```
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

LABEL maintainer="Netlab project <netlab.tools>"
LABEL description="bgpipe container"

RUN apt-get update && \
  apt-get install -y bash iputils-ping net-tools iproute2 wget jq && \
  wget https://github.com/bgpfix/bgpipe/releases/download/v0.8.8/bgpipe-linux-amd64 -q -O /usr/local/bin/bgpipe && \
  chmod a+x /usr/local/bin/bgpipe

WORKDIR /root

CMD /usr/bin/bash
```

After spending a few seconds building the container, I was ready to test the lab. After the few seconds it took **[netlab up](https://netlab.tools/netlab/up/)** to start the lab (FRRouting starts ridiculously fast), I was able to log into the Linux container and establish a BGP session with the router:

```
$ netlab connect probe
Connecting to container clab-bgpipe-probe, starting bash
root@probe:~# bgpipe -o speaker --asn 65100 172.16.0.1
2024-08-11 15:03:31 INF dialing 172.16.0.1:179 stage="[2] connect"
2024-08-11 15:03:31 INF connected 172.16.0.2:54132 -> 172.16.0.1:179 stage="[2] connect"
["L",1,"2024-08-11T15:03:31.615",97,"OPEN",{"bgp":4,"asn":65000,"id":"10.0.0.1","hold":9,"caps":{"MP":["IPV4/UNICAST"],"ROUTE_REFRESH":true,"EXTENDED_MESSAGE":true,"GRACEFUL_RESTART":"0xc078","AS4":65000,"ADDPATH":"0x00010101","ENHANCED_ROUTE_REFRESH":true,"LLGR":"0x00010180000000","FQDN":{"host":"rtr"},"VERSION":"0x144652526f7574696e672f31302e302e315f676974"}},{}]
["R",1,"2024-08-11T15:03:31.615",-1,"OPEN",{"bgp":4,"asn":65100,"id":"10.0.0.0","hold":90,"caps":{"MP":["IPV4/UNICAST","IPV4/FLOWSPEC","IPV6/UNICAST","IPV6/FLOWSPEC"],"ROUTE_REFRESH":true,"EXTENDED_MESSAGE":true,"AS4":65100}},{}]
["R",2,"2024-08-11T15:03:31.615",0,"KEEPALIVE",null,{}]
["L",2,"2024-08-11T15:03:31.615",0,"KEEPALIVE",null,{}]
2024-08-11 15:03:31 INF negotiated session capabilities caps="{\"MP\":[\"IPV4/UNICAST\"],\"ROUTE_REFRESH\":true,\"EXTENDED_MESSAGE\":true,\"AS4\":65100}"
2024-08-11 15:03:31 INF event bgpfix/pipe.ESTABLISHED seq=15 vals=[1723388611]
["L",3,"2024-08-11T15:03:32.716",37,"UPDATE",{"reach":["10.0.0.1/32"],"attrs":{"ORIGIN":{"flags":"T","value":"IGP"},"ASPATH":{"flags":"TX","value":[65000]},"NEXTHOP":{"flags":"T","value":"172.16.0.1"},"MED":{"flags":"O","value":0}}},{}]
["R",3,"2024-08-11T15:03:34.616",0,"KEEPALIVE",null,{}]
["L",4,"2024-08-11T15:03:34.616",0,"KEEPALIVE",null,{}]
["R",4,"2024-08-11T15:03:37.616",0,"KEEPALIVE",null,{}]
["L",5,"2024-08-11T15:03:37.616",0,"KEEPALIVE",null,{}]
```

As always, you can [find the source code on GitHub](https://github.com/ipspace/netlab-examples/tree/master/BGP/bgpipe), and you can [start the lab in GitHub Codespaces](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/):

* After [starting the codespace](https://github.com/codespaces/new/ipspace/netlab-examples), change the working directory to `BGP/bgpipe`
* Execute `docker build . -t netlab/bgpipe:latest` to build the container with **bgpipe**
* Execute `netlab up` to start the lab.
