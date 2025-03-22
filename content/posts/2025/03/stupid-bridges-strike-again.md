---
title: "IPv6 and the Revenge of the Stupid Bridges"
date: 2025-03-25 08:08:00+0100
tags: [ bridging, IPv6, netlab ]
netlab_tag: quirks
---
_This blog post describes another "OMG, this cannot possibly be true" scenario discovered during the [netlab](https://netlab.tools/) VRRP [integration testing](https://tests.netlab.tools/)._

I wanted to test whether we got the [nasty nuances of VRRPv3 IPv6 configuration](/2025/01/cisco-vrrp3-ipv6-configuration/) right on [all supported platforms](https://netlab.tools/module/gateway/#platform-support) and created a simple lab topology in which the device-under-test and an Arista cEOS container would be connected to two IPv6 networks (Arista EOS is a lovely device to use when testing a VRRP cluster because it produces JSON-formatted **show vrrp** printouts).

Most platforms worked as expected, but Aruba CX, Cumulus Linux with NVUE, and Dell OS10 consistently failed the tests. We were stumped until Jeroen van Bemmel discovered that the Arista container [forwards IPv6 router advertisements between the two LAN segments](https://github.com/ipspace/netlab/issues/1821).
<!--more-->
### Kicking the Tires

Here's the lab topology I used. You must start the lab with _netlab_ release older than 1.9.4 to get the described behavior (we implemented a [workaround](#wka) in the meantime).

```
module: [ gateway ]
gateway.protocol: vrrp
gateway.id: 1
addressing.lan.ipv6: 2001:db8:1::/56

nodes:
  r1: { device: arubacx }
  r2: { device: eos, provider: clab }
  h1: { device: linux, provider: clab }
  h2: { device: linux, provider: clab }

links:
- interfaces: [ r1, r2, h1 ]
  gateway: True
- interfaces: [ r1, r2, h2 ]
  gateway: True
```

Once the lab runs, log into the Linux hosts and inspect their IPv6 routing tables. This is what I got on H1:

```
h1:/# ip -6 route
2001:db8:1::/64 dev eth1  metric 256  expires 0sec
2001:db8:1:1::/64 dev eth1  metric 256  expires 0sec
fe80::/64 dev eth0  metric 256
fe80::/64 dev eth1  metric 256
default via fe80::800:901:41b:13ed dev eth1  metric 1024  expires 0sec
default via fe80::800:901:81b:13ed dev eth1  metric 1024  expires 0sec
```

H1 claims that both IPv6 prefixes used in the lab are *directly connected*. No wonder VRRPv3 does not work; the hosts don't even try to use the first-hop routers.

### What's Going On?

It took us a while to figure out what was going on, but it's pretty easy to demonstrate it with perfect hindsight:

* Start the lab with `netlab up --no-config` to get the initial device configurations
* Log into the Arista container and inspect its VLANs

Here's what you'll see on an Arista cEOS container running release 4.33.1F-39879738.4331F:

{{<cc>}}All data-plane interfaces are in VLAN 1{{</cc>}}
```
$ netlab connect r2
Connecting to clab-X-r2 using SSH port 22
r2>show vlan
VLAN  Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1     default                          active    Et1, Et2
```

**Long story short:** Without additional configuration, Arista EOS VMs and containers act like stupid bridges: all interfaces are enabled and in VLAN 1. Unfortunately, it's not just Arista. Cisco IOSv L2 and Cisco IOL L2 images are no better.

### Reverse-Engineering the Mishap

Now we know what's happening, but why did it happen only with some devices? The Ansible playbook _netlab_ uses to configure lab devices happens to execute configuration tasks sorted by the device type, and one could observe the above behavior only if:

* The tested device was configured before the EOS switch (that's why we observed this behavior on Aruba, Cumulus Linux 5.x, and Dell OS10)
* The configuration took long enough for the EOS switch to enable the access interfaces in VLAN 1 and start forwarding data between them.
* The tested device started sending IPv6 RA messages before the Ansible playbook managed to configure L3 ports on the EOS switch (that's probably why Cisco CSR and Cumulus Linux 4.x worked).

### Workaround {#wka}

We fixed this anomaly in netlab release 1.9.4 by adding an extra *normalization* configuration step executed before the initial interface configuration. This step shuts down data-plane interfaces on Arista EOS and Cisco IOS L2 devices.

### This Makes Me Sad

Years ago, I tried to persuade security-minded networking engineers that we don't need separate (physical) *inside* and *outside* switches in a DMZ because VLANs provide sufficient isolation.

While doing that, I was also stupid enough to say, "_I don't believe any decent switch vendor would start their devices as stupid bridges, directly linking inside, DMZ, and outside VLAN if the switch has no initial configuration._" I might have been wrong; what's your experience with physical switches?
