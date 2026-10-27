---
title: "Nexus OS Fails to Send Syslog Records to a Silent Host"
date: 2026-10-27 11:02:00+0100
tags: [ netlab ]
netlab_tag: quirks
---
Here's another *you can't make this up* ~~SNAFU~~ observation I made when running [integration tests](https://release.netlab.tools/_html/coverage.services) for _netlab_ [Syslog functionality](https://netlab.tools/module/services/): Cisco Nexus OS cannot send Syslog messages to a directly connected silent host.

The setup is as trivial as it can get: a Cisco Nexus OS VM (running version 10.6(2)) connected to a dnsmasq container running rsyslogd.
<!--more-->
| Node/Interface | IPv4 Address | IPv6 Address | MTU | Description |
|----------------|-------------:|-------------:|----:|-------------|
| **sw** |  10.0.0.1/32 |  | | Loopback |
| Ethernet1/1 | 172.16.0.1/24 |  |  | sw -> nms |
| **nms** | 
| eth1 | 172.16.0.2/24 |  | 1500 | nms -> sw |
{.fmtTable}

After the lab is started, I connected to the Nexus OS switch, enabled **terminal monitor** and configured a syslog server:

```
sw# terminal monitor
sw# configure
sw(config)# logging server 172.16.0.2 7
sw(config)#
sw# 2026 Oct 27 10:01:11 sw %VSHD-5-VSHD_SYSLOG_CONFIG_I: Configured from vty by admin on 192.168.121.1@pts/3
```

The **tcpdump** command listening to the SW-NMS link showed no traffic. The ARP cache on Nexus OS was empty:

```
sw# show ip arp

Flags: * - Adjacencies learnt on non-active FHRP router
       + - Adjacencies synced via CFSoE
       # - Adjacencies Throttled for Glean
       CP - Added via L2RIB, Control plane Adjacencies
       PS - Added via L2RIB, Peer Sync
       RO - Re-Originated Peer Sync Entry
       D - Static Adjacencies attached to down interface

IP ARP Table for context default
Total number of entries: 0
Address         Age       MAC Address     Interface       Flags
```

Just to be on the safe side, I checked the routing table. The destination (syslog server) was reachable:

```
sw# show ip route 172.16.0.2
IP Route Table for VRF "default"
'*' denotes best ucast next-hop
'**' denotes best mcast next-hop
'[x/y]' denotes [preference/metric]
'%<string>' in via output denotes VRF <string>

172.16.0.0/24, ubest/mbest: 1/0, attached
    *via 172.16.0.1, Eth1/1, [0/0], 00:02:53, direct
```

I also checked **show logging**, and the output claimed the Syslog server is configured:

```
sw# show logging

Logging console:                enabled (Severity: critical)
Logging monitor:                enabled (Severity: notifications)
Logging linecard:               enabled (Severity: notifications)
Logging timestamp:              Seconds
Logging source-interface :      disabled
Logging rate-limit:             enabled
Logging server:                 enabled
{172.16.0.2}
        server status:          Configured
        server severity:        debugging
        server facility:        local7
        server VRF:             default
        server port:            514
Logging origin_id :             disabled
Logging RFC :                   disabled
Logging logflash:               enabled (Severity: notifications)(threshold percentage: 0)
Logging logfile:                enabled
        Name - messages: Severity - notifications Size - 4194304


Facility        Default Severity        Current Session Severity
--------        ----------------        ------------------------
aaa                     3                       3
```

Next, I pinged 172.16.0.2 from Nexus OS to populate the ARP cache. **tcpdump** observed ARP/ICMP traffic between the two nodes, but no UDP traffic:

```
sw# ping 172.16.0.2 count 2
PING 172.16.0.2 (172.16.0.2): 56 data bytes
36 bytes from 172.16.0.1: Destination Host Unreachable
Request 0 timed out
64 bytes from 172.16.0.2: icmp_seq=1 ttl=63 time=1.085 ms

--- 172.16.0.2 ping statistics ---
2 packets transmitted, 1 packets received, 50.00% packet loss
round-trip min/avg/max = 1.085/1.085/1.085 ms
sw# show ip arp

Flags: * - Adjacencies learnt on non-active FHRP router
       + - Adjacencies synced via CFSoE
       # - Adjacencies Throttled for Glean
       CP - Added via L2RIB, Control plane Adjacencies
       PS - Added via L2RIB, Peer Sync
       RO - Re-Originated Peer Sync Entry
       D - Static Adjacencies attached to down interface

IP ARP Table for context default
Total number of entries: 1
Address         Age       MAC Address     Interface       Flags
172.16.0.2      00:00:14  aac1.abb8.c3d5  Ethernet1/1
```

Finally, I entered the configuration mode once more to generate yet another logging message:

```
sw# conf t
Enter configuration commands, one per line. End with CNTL/Z.
sw(config)#
sw#
2026 Oct 27 10:10:53 sw %VSHD-5-VSHD_SYSLOG_CONFIG_I: Configured from vty by admin on 192.168.121.1@pts/3 (message repeated 1 time)
```

At that time, **tcpdump** recorded several UDP packets sent from Nexus OS to the adjacent Syslog server:

```
$ netlab capture nms eth1 ip or arp
Starting packet capture on nms/eth1: sudo ip netns exec clab-X-nms tcpdump -i eth1 --immediate-mode -l -vv ip or arp
tcpdump: listening on eth1, link-type EN10MB (Ethernet), snapshot length 262144 bytes
09:59:01.589880 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has ethernet1-1.sw (Broadcast) tell ethernet1-1.sw, length 46
09:59:03.590592 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has ethernet1-1.sw (Broadcast) tell ethernet1-1.sw, length 46
10:10:09.124390 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has nms.netlab.local (Broadcast) tell ethernet1-1.sw, length 46
10:10:09.124414 ARP, Ethernet (len 6), IPv4 (len 4), Reply nms.netlab.local is-at aa:c1:ab:b8:c3:d5 (oui Unknown), length 28
10:10:11.126333 IP (tos 0x0, ttl 255, id 40063, offset 0, flags [none], proto ICMP (1), length 84)
    ethernet1-1.sw > nms.netlab.local: ICMP echo request, id 34923, seq 256, length 64
10:10:11.126375 IP (tos 0x0, ttl 64, id 35893, offset 0, flags [none], proto ICMP (1), length 84)
    nms.netlab.local > ethernet1-1.sw: ICMP echo reply, id 34923, seq 256, length 64
10:10:16.146686 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has ethernet1-1.sw tell nms.netlab.local, length 28
10:10:16.147948 ARP, Ethernet (len 6), IPv4 (len 4), Reply ethernet1-1.sw is-at ca:f0:00:01:00:01 (oui Unknown), length 46
10:10:59.942358 IP (tos 0x0, ttl 64, id 40062, offset 0, flags [none], proto UDP (17), length 142)
    ethernet1-1.sw.59839 > nms.netlab.local.syslog: [udp sum ok] SYSLOG, length: 114
	Facility local7 (23), Severity notice (5)
	Msg: : 2026 Oct 27 10:01:12 UTC: %VSHD-5-VSHD_SYSLOG_CONFIG_I: Configured from vty by admin on 192.168.121.1@pts/3
	0x0000:  3c31 3839 3e3a 2032 3032 3620 4f63 7420
	0x0010:  3237 2031 303a 3031 3a31 3220 5554 433a
	0x0020:  2025 5653 4844 2d35 2d56 5348 445f 5359
	0x0030:  534c 4f47 5f43 4f4e 4649 475f 493a 2043
	0x0040:  6f6e 6669 6775 7265 6420 6672 6f6d 2076
	0x0050:  7479 2062 7920 6164 6d69 6e20 6f6e 2031
	0x0060:  3932 2e31 3638 2e31 3231 2e31 4070 7473
	0x0070:  2f33
10:10:59.942459 IP (tos 0x0, ttl 64, id 40063, offset 0, flags [none], proto UDP (17), length 168)
    ethernet1-1.sw.59839 > nms.netlab.local.syslog: [udp sum ok] SYSLOG, length: 140
	Facility local7 (23), Severity notice (5)
	Msg: : 2026 Oct 27 10:10:53 UTC: %VSHD-5-VSHD_SYSLOG_CONFIG_I: Configured from vty by admin on 192.168.121.1@pts/3 (message repeated 1 time)
	0x0000:  3c31 3839 3e3a 2032 3032 3620 4f63 7420
	0x0010:  3237 2031 303a 3130 3a35 3320 5554 433a
	0x0020:  2025 5653 4844 2d35 2d56 5348 445f 5359
	0x0030:  534c 4f47 5f43 4f4e 4649 475f 493a 2043
	0x0040:  6f6e 6669 6775 7265 6420 6672 6f6d 2076
	0x0050:  7479 2062 7920 6164 6d69 6e20 6f6e 2031
	0x0060:  3932 2e31 3638 2e31 3231 2e31 4070 7473
	0x0070:  2f33 2028 6d65 7373 6167 6520 7265 7065
	0x0080:  6174 6564 2031 2074 696d 6529
```

Check the timestamps in the **Msg** field. The first syslog message had been generated nine minutes before it was sent. It looks like Nexus OS buffers syslog messages when it cannot send them, but it never triggers the ARP request that would populate the ARP cache and allow it to send the UDP packets.

This is the only comment that came to my mind after observing that behavior:

{{<figure src="/images/triple-facepalm.jpg">}}
