---
title: "Using wemulate with netlab"
date: 2024-04-02 07:49:00+0200
tags: [ netlab ]
netlab_tag: use
---
An RSS hiccup brought an [old blog post from Urs Baumann](https://infrastructureascode.ch/wemulate-container.html) into my RSS reader. I'm always telling networking engineers that it's essential to set up realistic WAN environments when testing distributed software, and [wemulate](https://wemulate.github.io/wemulate/) (a nice tc front-end) seemed like a perfect match. Even better, it runs in a container -- an ideal component for a netlab-generated virtual WAN network.

wemulate acts as a bump in the wire; it uses Linux bridges to connect two container interfaces. We'll use it to introduce jitter into an IP subnet:

{{<ascii>}}
┌──┐   ┌────────┐   ┌──┐
│h1├───┤wemulate├───┤h2│
└──┘   └────────┘   └──┘                       
◄──────────────────────►
     192.168.33.0/24    
{{</ascii>}}
<!--more-->
*netlab* tries to assign an IP prefix to every link in the lab. While we could cheat with VLANs, I decided to go for static IPv4 prefixes, resulting in the following lab topology:

{{<printout>}}
provider: clab
defaults.device: linux
defaults.devices.linux.image: ghcr.io/hellt/network-multitool
defaults.devices.linux.group_vars.docker_shell: bash -il

nodes:
  h1:
  h2:
  wanem:
    image: ghcr.io/wemulate/wemulate-container

links:
- h1:
  wanem:
    ipv4: False
  prefix.ipv4: 192.168.33.0/24
- h2:
  wanem:
    ipv4: False
  prefix.ipv4: 192.168.33.0/24
{{</printout>}}

**Notes:**
* Line 1: we're using containers orchestrated with containerlab
* Line 2: the lab devices are Linux hosts
* Line 3: the default container image for a Linux host is a networking-focused container created by Roman Dodin
* Line 4: the default Docker shell is **bash** (so we get command completion and history)
* Line 10: the `wanem` node uses the wemulate container image
* Line 15 (and 19): the `wanem` node does not have an IPv4 address on the interface attached to the link
* Line 16 (and 20): the link uses a static IP prefix. IPv4-enabled devices attached to the link (h1 and h2) will get IPv4 addresses based on the link prefix and device ID (192.168.33.1 and 192.168.33.2)

### Kicking the Tires

* [Install netlab](https://netlab.tools/install/), copy the topology file into an empty directory, and start the lab with **netlab up**
* Log into h1 with **netlab connect h1** and try to ping **h2**. The ping should fail as we still need to create a *connection* in **wemulate**.

```
Connecting to container clab-wemulate-h1, starting bash
h1:/# ping h2
PING h2 (192.168.33.2) 56(84) bytes of data.
From h1 (192.168.33.1) icmp_seq=1 Destination Host Unreachable
From h1 (192.168.33.1) icmp_seq=2 Destination Host Unreachable
From h1 (192.168.33.1) icmp_seq=3 Destination Host Unreachable
^C
--- h2 ping statistics ---
6 packets transmitted, 0 received, +3 errors, 100% packet loss, time 5120ms
```

* **wemulate** uses its own interface names. Inspect the container interfaces and **wemulate** interface names:

```
Connecting to container clab-wemulate-wanem, starting bash
root@wanem:/# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
3816: eth0@if3817: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:c0:a8:79:67 brd ff:ff:ff:ff:ff:ff link-netnsid 0
3822: eth1@if3823: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether aa:c1:ab:2e:6a:54 brd ff:ff:ff:ff:ff:ff link-netnsid 1
3824: eth2@if3825: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether aa:c1:ab:56:f9:e7 brd ff:ff:ff:ff:ff:ff link-netnsid 2
root@wanem:/# wemulate show interfaces
                 Interfaces
┏━━━━━━━┳━━━━━━━━━━┳━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ NAME  ┃ PHYSICAL ┃ IP ┃ MAC               ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ LAN-A │ eth1     │    │ aa:c1:ab:2e:6a:54 │
│ LAN-B │ eth2     │    │ aa:c1:ab:56:f9:e7 │
└───────┴──────────┴────┴───────────────────┘
```

* Create a **wemulate** connection between LAN-A (eth1) and LAN-B (eth-2):

```
root@wanem:/# wemulate add connection -n test -i LAN-A LAN-B
Successfully added a new connection
```

* Retry the ping between h1 and h2. Now it should work. Notice how fast it is:

```
h1:/# ping h2
PING h2 (192.168.33.2) 56(84) bytes of data.
64 bytes from h2 (192.168.33.2): icmp_seq=1 ttl=64 time=0.051 ms
64 bytes from h2 (192.168.33.2): icmp_seq=2 ttl=64 time=0.048 ms
```

* Add jitter to the LAN-A/LAN-B connection:

```
root@wanem:/# wemulate add parameter -n test -j 200
successfully added parameters to connection test
root@wanem:/# wemulate show connections
                 Connection Information
┏━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ NAME ┃ 1. INTERFACE ┃ 2. INTERFACE ┃ PARAMETERS       ┃
┡━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ test │ LAN-A        │ LAN-B        │ <-> jitter: 200  │
│      │              │              │                  │
└──────┴──────────────┴──────────────┴──────────────────┘
```

* Retry the ping between h1 and h2 and admire the ridiculously long round-trip time:

```
h1:/# ping h2
PING h2 (192.168.33.2) 56(84) bytes of data.
64 bytes from h2 (192.168.33.2): icmp_seq=1 ttl=64 time=136 ms
64 bytes from h2 (192.168.33.2): icmp_seq=2 ttl=64 time=0.059 ms
64 bytes from h2 (192.168.33.2): icmp_seq=3 ttl=64 time=0.063 ms
64 bytes from h2 (192.168.33.2): icmp_seq=4 ttl=64 time=283 ms
64 bytes from h2 (192.168.33.2): icmp_seq=5 ttl=64 time=75.2 ms
64 bytes from h2 (192.168.33.2): icmp_seq=6 ttl=64 time=621 ms
64 bytes from h2 (192.168.33.2): icmp_seq=7 ttl=64 time=389 ms
64 bytes from h2 (192.168.33.2): icmp_seq=8 ttl=64 time=128 ms
64 bytes from h2 (192.168.33.2): icmp_seq=9 ttl=64 time=361 ms
64 bytes from h2 (192.168.33.2): icmp_seq=10 ttl=64 time=282 ms
64 bytes from h2 (192.168.33.2): icmp_seq=11 ttl=64 time=200 ms
64 bytes from h2 (192.168.33.2): icmp_seq=12 ttl=64 time=343 ms
64 bytes from h2 (192.168.33.2): icmp_seq=13 ttl=64 time=116 ms
64 bytes from h2 (192.168.33.2): icmp_seq=14 ttl=64 time=0.053 ms
64 bytes from h2 (192.168.33.2): icmp_seq=15 ttl=64 time=230 ms
64 bytes from h2 (192.168.33.2): icmp_seq=16 ttl=64 time=424 ms
^C
--- h2 ping statistics ---
16 packets transmitted, 16 received, 0% packet loss, time 15076ms
rtt min/avg/max/mdev = 0.053/224.283/621.411/170.767 ms
```

Congratulations. You managed to create a network that emulates the behavior of cable-based Internet access on Sunday evenings.
