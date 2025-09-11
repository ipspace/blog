---
title: "The Curious Case of 'ip host' Configuration Command"
date: 2025-09-11 09:51:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
Since time immemorial, I have used the **ip host** router configuration command to get host-to-IP mappings in networking labs without going through the hassle of setting up a DNS server. Some devices even accepted multiple IP addresses in the **ip host** command, allowing you to list all router interfaces in a single command and get reverse (IP-to-host) mapping working like a charm. Or so I thought 🤦‍♂️

It turns out I'm too old, and what I know is sometimes no longer true. It seems that the last implementation working as I expected is Cisco IOS Classic ☹️
<!--more-->
I tested the device behavior with the simplest possible lab topology -- two routers with loopbacks running OSPF over a pair of links:

{{<cc>}}Lab topology{{</cc>}}
```
nodes: [ a, b ]
module: [ ospf ]
links: [ a-b ]
```

{{<note info>}}
[Setting up _netlab_](https://netlab.tools/install/) on a Ubuntu server and [building Vagrant boxes](https://netlab.tools/labs/libvirt/#building-vagrant-boxes) (or [vrnetlab containers](https://netlab.tools/labs/clab/#using-vrnetlab-containers)) for all devices you're interested in wastes a day or so of your life, but then tests like this one are a breeze. If you're forced to live in a multi-platform or multi-vendor world, wasting that day might be a good long-term investment. #JustSaying 😉
{{</note>}}

This is the **ip host** command _netlab_ generates for router A running Cisco IOS or Arista EOS. The B's loopback IP address (`10.0.0.2`) is listed first, followed by its Ethernet IP address (`10.1.0.2`).

```
ip host b 10.0.0.2 10.1.0.2
```

On Cisco IOSv (release 15.6.1), the loopback IP address is displayed as the first IP address with the **show hosts** command, and used in pings:

{{<cc>}}The impact of multiple IP addresses specified in **ip host** command on Cisco IOSv{{</cc>}}
```
a#show hosts
Default domain is lab.local
Name/address lookup uses static mappings

Codes: UN - unknown, EX - expired, OK - OK, ?? - revalidate
       temp - temporary, perm - permanent
       NA - Not Applicable None - Not defined

Host                      Port  Flags      Age Type   Address(es)
b                         None  (perm, OK)  0   IP    10.0.0.2
                                                      10.1.0.2
a#ping b
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```

The behavior changed on Cisco IOS/XE. The **show hosts** command produces DNS zone information (OK), the IP addresses are listed in reverse order (for no good reason I could discover), and the **ping** command uses the *last* IP address specified in the **ip host** command.

{{<cc>}}The impact of multiple IP addresses specified in **ip host** command on Cisco IOS/XE (Cisco IOL release 17.12.1){{</cc>}}
```
a#show hosts
Default domain is lab
Name servers are 255.255.255.255
NAME  TTL  CLASS   TYPE      DATA/ADDRESS
-----------------------------------------
 2.0.0.10.in-addr.arpa	10	IN	PTR	b
 2.0.1.10.in-addr.arpa	10	IN	PTR	b
 b	10	IN	A	10.1.0.2
 b	10	IN	A	10.0.0.2

a#ping b
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.1.0.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```

Changing the order of the IP addresses "fixes" the problem. The IP addresses are *always* transformed into the DNS zone information *in reverse order* and *the last one* is always used:

{{<cc>}}Adding a few bogus IP address to **ip host** command on Cisco IOS/XE{{</cc>}}
```
a#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
a(config)#no ip host b
a(config)#ip host b 10.1.0.2 10.2.2.2 10.3.3.3 10.4.4.4 10.0.0.2
a(config)#^Z
a#show hosts
Default domain is lab
Name servers are 255.255.255.255
NAME  TTL  CLASS   TYPE      DATA/ADDRESS
-----------------------------------------
 2.0.0.10.in-addr.arpa	10	IN	PTR	b
 2.0.1.10.in-addr.arpa	10	IN	PTR	b
 2.2.2.10.in-addr.arpa	10	IN	PTR	b
 3.3.3.10.in-addr.arpa	10	IN	PTR	b
 4.4.4.10.in-addr.arpa	10	IN	PTR	b
 b	10	IN	A	10.0.0.2
 b	10	IN	A	10.4.4.4
 b	10	IN	A	10.3.3.3
 b	10	IN	A	10.2.2.2
 b	10	IN	A	10.1.0.2

a#ping b
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```

Then there's Arista EOS (the only other platform for which we implemented multiple IP addresses in the host-to-IP mappings). Here's what it does when faced with the initial lab configuration:

```
a#show hosts

Default domain is not configured
Name/address lookup uses domain service
Name servers are:
IP Address VRF Priority
---------- --- --------

Static Mappings:
Hostname IP   Addresses
-------- ---- ---------
b        IPV4 10.0.0.2
              10.1.0.2

a#ping b
PING b (10.1.0.2) 72(100) bytes of data.
80 bytes from b (10.1.0.2): icmp_seq=1 ttl=64 time=0.036 ms
80 bytes from b (10.1.0.2): icmp_seq=2 ttl=64 time=0.009 ms
80 bytes from b (10.1.0.2): icmp_seq=3 ttl=64 time=0.008 ms
80 bytes from b (10.1.0.2): icmp_seq=4 ttl=64 time=0.008 ms
80 bytes from b (10.1.0.2): icmp_seq=5 ttl=64 time=0.009 ms
```

Changing the order of IP addresses in the **ip host** command does not help. The addresses are always sorted in the **show hosts** printout, and `10.1.0.2` is always used as the target of the **ping** command.

Next, I thought that Arista EOS might use a host's highest IP address, but changing the IP address of B's loopback interface to `10.42.42.42/32` didn't help a bit.

The only (somewhat dubious) explanation I could come up with is that Arista EOS uses the IP routing table to sort the IP addresses specified in the **ip host** command, and then tries to use them according to their distance. For example, when I added a bogus IP address (not reachable through the IP routing table) to the **ip host b** configuration command, the **telnet b** command tried the specified B's IP addresses in the following order:

* The Ethernet IP address (directly connected)
* The loopback IP address (OSPF route)
* The bogus IP address (no route in the routing table)

```
a#telnet b
Trying 10.1.0.2...
telnet: connect to address 10.1.0.2: Connection refused
Trying 10.0.0.2...
telnet: connect to address 10.0.0.2: Connection refused
Trying 10.42.42.42...
telnet: connect to address 10.42.42.42: Network is unreachable
```

Changing the loopback IP address on B to `10.42.42.42/32` reversed the order of the last two lines, which seems to prove my conjecture.

If you happen to know more, please leave a comment!
