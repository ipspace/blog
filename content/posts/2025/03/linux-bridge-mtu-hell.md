---
title: "Linux Bridge MTU Hell"
date: 2025-03-10 08:11:00+0100
draft: True
tags: [ virtualization, switching ]
---
When I announced the [Stub Networks in Virtual Labs](/2025/02/virtual-dummy-interfaces/) blog post on LinkedIn, I claimed it was *the last chapter in the "links in virtual labs" saga*. I was wrong; here comes the fourth part of the *virtual links* trilogy.

It all started with an innocuous article [describing the MTU basics](https://packetpushers.net/blog/mtu-deep-dive-part-1/). As the real purpose of the MTU is to prevent packet drops due to fixed-size receiver buffers, I wanted to check how various devices react to incoming oversized packets. As the first step, I created a simple _netlab_ topology in which a single link had a slightly larger than usual MTU... and then all hell broke loose.
<!--more-->
{{<cc>}}netlab topology I used to test VM MTU behavior{{</cc>}}
```
provider: libvirt

nodes:
  r:
    device: eos
  h:
    device: linux

links:
- r:
  h:
  mtu: 1600
```

After starting the lab, both devices could ping each other. However, when I increased the packet size to 1550 bytes, I could ping the Linux VM from the Arista VM but failed in the other direction.

{{<cc>}}Pinging Linux host from the Arista switch{{</cc>}}
```
r#ping h
PING h (172.16.0.2) 72(100) bytes of data.
80 bytes from h (172.16.0.2): icmp_seq=1 ttl=64 time=4.51 ms
80 bytes from h (172.16.0.2): icmp_seq=2 ttl=64 time=0.548 ms
80 bytes from h (172.16.0.2): icmp_seq=3 ttl=64 time=0.506 ms
80 bytes from h (172.16.0.2): icmp_seq=4 ttl=64 time=0.650 ms
80 bytes from h (172.16.0.2): icmp_seq=5 ttl=64 time=0.460 ms

--- h ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 16ms
rtt min/avg/max/mdev = 0.460/1.335/4.513/1.590 ms, ipg/ewma 4.023/2.868 ms

r#ping h size 1600
PING h (172.16.0.2) 1572(1600) bytes of data.
1580 bytes from h (172.16.0.2): icmp_seq=1 ttl=64 time=1.20 ms
1580 bytes from h (172.16.0.2): icmp_seq=2 ttl=64 time=0.922 ms
1580 bytes from h (172.16.0.2): icmp_seq=3 ttl=64 time=0.594 ms
1580 bytes from h (172.16.0.2): icmp_seq=4 ttl=64 time=0.515 ms
1580 bytes from h (172.16.0.2): icmp_seq=5 ttl=64 time=0.401 ms
```

{{<cc>}}Pinging directly connected interface of the Arista switch from the Linux host{{</cc>}}
```
vagrant@h:~$ ping Ethernet1.r -c 3
PING Ethernet1.r (172.16.0.1) 56(84) bytes of data.
64 bytes from Ethernet1.r (172.16.0.1): icmp_seq=1 ttl=64 time=1.30 ms
64 bytes from Ethernet1.r (172.16.0.1): icmp_seq=2 ttl=64 time=1.16 ms
64 bytes from Ethernet1.r (172.16.0.1): icmp_seq=3 ttl=64 time=1.23 ms

--- Ethernet1.r ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 1.160/1.229/1.298/0.056 ms
vagrant@h:~$ ping Ethernet1.r -c 3 -s 1550
PING Ethernet1.r (172.16.0.1) 1550(1578) bytes of data.
^C
--- Ethernet1.r ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2045ms
```

Faced with a bizarre behavior like this, my brain should have been screaming MTU[^NDB], but I must have been sluggish -- it took quite a bit of packet capture to figure things out.

[^NDB]: It couldn't have been DNS or BGP, they were both AWOL.
