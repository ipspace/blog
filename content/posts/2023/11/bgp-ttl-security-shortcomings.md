---
title: "Is BGP TTL Security Any Good?"
date: 2023-11-21 07:38:00
tags: [ BGP, security, netlab ]
pre_scroll: True
netlab_tag: use
---
After checking what routers do when they [receive a TCP SYN packet from an unknown source](https://blog.ipspace.net/2023/10/reject-unknown-bgp-session.html), I couldn't resist checking how they cope with TCP SYN packets with too-low TTL when using TTL security, formally known as The Generalized TTL Security Mechanism (GTSM) defined in [RFC 5082](https://datatracker.ietf.org/doc/html/rfc5082).

**TL&DR:** Not bad: most devices I managed to test did a decent job.
<!--more-->
In this blog post:

* [The not-so-small print](#nssp)
* [Test setup](#setup)
* [Test results](#results) from Arista EOS, Cisco IOSv, Cisco Nexus OS and Cumulus Linux
* [Real-life impact](#reallife)

## The Not-So-Small Print{#nssp}

I want to make a few things crystal clear before someone writes a _you have no clue_ comment:

* I wanted to show how easy it is to run some basic tests to expose potential flaws in security features. It's the methodology that matters, not the specific test results.
* Things change. You will probably test a different software version than I did and get different results. That's OK.
* I was running tests with virtual machines to ensure every network device uses its own TCP stack. Don't use containers, as they use the host TCP stack.
* Hardware boxes might implement hardware-based protection. Run your own tests.

### Test Setup{#setup}

I created a simple _netlab_ topology with two routers:

* Device under test (`dut`) with a *passive* BGP peer (to ensure it won't try to establish a TCP session) configured with GTSM.
* A BGP peer (`peer`) implemented with a FRR container

```
provider: libvirt

plugin: [ bgp.session ]
module: [ bgp ]

nodes:
  dut:                  # Device under test, change with 'netlab up -d'
    bgp.as: 65000
  peer:                 # A valid peer -- FRR daemon running in a container
    bgp.as: 65001
    device: frr
    provider: clab

links:
- dut:
    bgp.gtsm: True
    bgp.passive: True
  peer:
```

The lab devices will get the following IP addresses:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **dut** |  10.0.0.1/32 |  | Loopback |
| Ethernet1 | 172.16.0.1/24 |  | dut -> peer |
| **peer** |  10.0.0.2/32 |  | Loopback |
| eth1 | 172.16.0.2/24 |  | peer -> dut |
{.fmtTable}

This is the EBGP session configured between them:

| Node | Router ID /<br />Neighbor | Router AS/<br />Neighbor AS | Neighbor IPv4 |
|------|---------------------------|----------------------------:|--------------:|
| **dut** | 10.0.0.1 | 65000 |
| | peer | 65001 | 172.16.0.2 |
| **peer** | 10.0.0.2 | 65001 |
| | dut | 65000 | 172.16.0.1 |
{.fmtTable}

## Test Results{#results}

This time I got three clusters:

* [Arista EOS](#arista), [Cisco IOSv](#iosv), and [Cisco Nexus 9300v](#nxos) ignore incoming TCP SYN packets with too-low TTL
* [Cumulus Linux](#cl) (and FRR in general) accept the TCP session, get stuck, and eventually drop it.
* Juniper never implemented GTSM. Their best recommendations are "[write your own ACLs](https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/ref/statement/multihop-edit-protocols-bgp.html)" and "[use this script to generate the ACL for you](https://community.juniper.net/blogs/elevate-member/2020/10/22/scripting-how-to-use-the-ttl-security-script-to-turn-on-ttl-based-security-gtsm)".

### Arista EOS{#arista}

Arista vEOS is doing the right thing: it ignores TCP SYN packets with low TTL:

```
08:54:03.549025 IP (tos 0xc0, ttl 1, id 5089, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.36328 > 172.16.0.1.bgp: Flags [S], cksum 0x3525 (correct), seq 3579150169, win 64240, options [mss 1460,sackOK,TS val 3231390688 ecr 0,nop,wscale 7], length 0
08:54:04.550936 IP (tos 0xc0, ttl 1, id 5090, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.36328 > 172.16.0.1.bgp: Flags [S], cksum 0x313a (correct), seq 3579150169, win 64240, options [mss 1460,sackOK,TS val 3231391691 ecr 0,nop,wscale 7], length 0
08:54:06.567079 IP (tos 0xc0, ttl 1, id 5091, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.36328 > 172.16.0.1.bgp: Flags [S], cksum 0x295a (correct), seq 3579150169, win 64240, options [mss 1460,sackOK,TS val 3231393707 ecr 0,nop,wscale 7], length 0
```

The behind-the-scenes magic: Arista EOS modifies the **iptables** rule that protects its BGP daemon to include the TTL check:

```
-A BGP -s 172.16.0.2/32 -m ttl --ttl-lt 254 -j DROP
-A BGP -s 172.16.0.2/32 -j BGPSACL
-A BGP -j DROP
```

### Cisco IOSv{#iosv}

Cisco IOS is also ignoring incoming TCP SYN packets if the TTL is too low:

```
09:00:51.398798 IP (tos 0xc0, ttl 1, id 62613, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.33056 > 172.16.0.1.bgp: Flags [S], cksum 0xc867 (correct), seq 2920867562, win 64240, options [mss 1460,sackOK,TS val 3231798539 ecr 0,nop,wscale 7], length 0
09:00:55.558855 IP (tos 0xc0, ttl 1, id 62614, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.33056 > 172.16.0.1.bgp: Flags [S], cksum 0xb827 (correct), seq 2920867562, win 64240, options [mss 1460,sackOK,TS val 3231802699 ecr 0,nop,wscale 7], length 0
09:00:58.378973 IP (tos 0xc0, ttl 1, id 1942, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.47504 > 172.16.0.1.bgp: Flags [S], cksum 0xe2a1 (correct), seq 2871753705, win 64240, options [mss 1460,sackOK,TS val 3231805519 ecr 0,nop,wscale 7], length 0
```

According to Cisco IOSv BGP debugging, the TCP SYN packets don't reach the BGP daemon. You can see them with **debug ip tcp transactions** -- it looks like Cisco IOS is doing the right thing and dropping them in the TCP stack.

```
*Nov  8 09:04:24.208: TCP0: bad seg from 172.16.0.2 -- Discard the invalid TTL packets, packet ttl 1: port 179 seq 4283340001 ack 0 rcvnxt 0 rcvwnd 16384 len 0
*Nov  8 09:04:26.934: TCP0: bad seg from 172.16.0.2 -- Discard the invalid TTL packets, packet ttl 1: port 179 seq 3043807377 ack 0 rcvnxt 0 rcvwnd 16384 len 0
```

### Cisco Nexus 9300v{#nxos}

Like Arista EOS and Cisco IOSv, Nexus 9300v ignores the incoming TCP SYN packets with TTL = 1.

```
09:41:38.310886 IP (tos 0xc0, ttl 1, id 43480, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.46732 > 172.16.0.1.bgp: Flags [S], cksum 0x8cf9 (correct), seq 502212273, win 64240, options [mss 1460,sackOK,TS val 3234245451 ecr 0,nop,wscale 7], length 0
09:41:41.016330 IP (tos 0xc0, ttl 1, id 51281, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.41054 > 172.16.0.1.bgp: Flags [S], cksum 0xe12e (correct), seq 3771145024, win 64240, options [mss 1460,sackOK,TS val 3234248156 ecr 0,nop,wscale 7], length 0
09:41:42.022859 IP (tos 0xc0, ttl 1, id 51282, offset 0, flags [DF], proto TCP (6), length 60)
    172.16.0.2.41054 > 172.16.0.1.bgp: Flags [S], cksum 0xdd3f (correct), seq 3771145024, win 64240, options [mss 1460,sackOK,TS val 3234249163 ecr 0,nop,wscale 7], length 0
```

Similar to Arista vEOS, Cisco Nexus 9300v uses **iptables** to block incoming TCP packets from known BGP peers where the TTL is not high enough:

```
-A INPUT -p tcp -m tcp --dport 179 -j default-bgp-chain
-A default-bgp-chain -s 172.16.0.2/32 -m ttl --ttl-lt 254 -j DROP
```

### Cumulus Linux{#cl}

I tested a recent community cumulus-vx image (version 5.6.0), starting the lab with **netlab up -d cumulus -s nodes.dut.image=CumulusCommunity/cumulus-vx:5.6.0 -s nodes.dut.memory=4096**. FRR BGP daemon running on Cumulus Linux happily accepted the TCP session, but then got stuck in the exchange of BGP OPEN messages[^TDTM]:

[^TDTM]: The **tcpdump** printout is too messy to include.

```
dut# show ip bgp sum

IPv4 Unicast Summary (VRF default):
BGP router identifier 10.0.0.1, local AS number 65000 vrf-id 0
BGP table version 1
RIB entries 1, using 192 bytes of memory
Peers 2, using 40 KiB of memory

Neighbor         V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt Desc
peer(172.16.0.2) 4      65001         2         3        0    0    0 00:09:01       Active        0 peer
```

Every now and then, the BGP daemon resets the TCP session due to BGP OPEN exchange timeout, resulting in a number of half-closed TCP sessions:

```
$ netstat -t -n | grep 172.16.0.2
tcp        0    117 172.16.0.1:179          172.16.0.2:41362        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:48610        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:58326        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:49568        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:57868        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:32996        FIN_WAIT1
tcp        0     95 172.16.0.1:179          172.16.0.2:55720        ESTABLISHED
tcp        0    117 172.16.0.1:179          172.16.0.2:59040        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:39206        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:53782        FIN_WAIT1
tcp        0    117 172.16.0.1:179          172.16.0.2:42500        FIN_WAIT1
```

Root cause of that behavior: the minimum TCP TTL is set in the FRR BGP daemon after the TCP session has been accepted. That's the best the FRR team can do without messing with the underlying Linux data structures, but the vendor integrating FRR into their solution (~~Cumulus Linux~~, oops ~~Mellanox~~ Nvidia) should do better.

Unfortunately I don't have the VM images for other network operating systems using FRR (example: SONiC), so I can't test what they're doing. Feedback is (as always) highly appreciated.

### Real-Life Impact{#reallife}

There are two scenarios you might want to prevent with GTSM:

* Establishing a BGP session with an intruder after it manages to inject a more specific route toward a valid EBGP peer. All devices I tested would pass this (pretty much hypothetical) scenario with flying colors[^DCI] 
* Preventing denial-of-service TCP SYN attacks. Arista EOS and Cisco Nexus OS would do a much better job than Cumulus Linux because they drop packets with too-low TTL before they reach the TCP code in the Linux kernel. Obviously, once the volume of the DoS traffic exceeds the CPU capacity, your box quickly starts resembling a brick.

Hardware ACLs are the only way to go if you want to have a robust high-speed solution. [Control-plane protection](https://blog.ipspace.net/2008/11/control-plane-protection-overview.html) might be a decent first step, but it might drop good traffic together with the volumetric DoS attack. It's much better to deploy ACLs checking TCP port numbers and IP TTL on external interfaces, assuming your box has enough hardware resources to do that.

Finally, remember that you cannot apply GTSM to IBGP sessions in most BGP implementations. The only way to protect IBGP routers from external intruders is to deploy ACLs at the network edge or to establish IBGP sessions between IP addresses that are not announced to the outside world. That might be why we sometimes see RFC 1918 address space used for router loopbacks (and BGP router IDs).

[^DCI]: All bets are off if the intruder is directly connected to your router. After all, we're all friends on link-local, right?
