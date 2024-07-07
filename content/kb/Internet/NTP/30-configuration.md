---
kb_section: NTP
minimal_sidebar: true
title: NTP Configuration on Cisco IOS
url: /kb/Internet/NTP/30-configuration/
---
NTP configuration in Cisco IOS uses global configuration commands that start with the keyword **ntp**. The upstream NTP servers in Cisco IOS are defined with the **ntp server _ip-address_** configuration command and the peers are defined with the **ntp peer _ip-address_** configuration command.

{{<note>}}The router’s behavior will not change if you define all neighboring servers with the **ntp peer** configuration commands, but since the router will send out NTP packets indicating peer-to-peer mode, an unprotected upstream server could decide to synchronize to them.{{</note>}}

Once the router synchronizes with its NTP neighbors, it will insert the **ntp clock-period _some-number_** command in the running configuration. This command specifies an estimate of the actual frequency of the local clock (the internal router’s clock is believed to be highly precise, but not necessarily running at the correct frequency). Don’t change it and make sure it’s stored in the NVRAM after the router’s time synchronization reaches steady state (upstream NTP servers are polled every 1024 seconds).

It’s highly recommended that you track the status of your time synchronization with *syslog* commands; the **ntp logging** command was introduced in IOS release 12.4. Some people [complain that it generates too much output](http://blog.ipspace.net/2007/10/log-ntp-events.html), but the repeating messages about NTP synchronization loss and subsequent resynchronization usually indicate a real problem somewhere in your network:

* The **ntp clock-period** command could be a bad estimate of the drift of the router’s internal clock;
* The NTP server is intermittently unreachable;
* The NTP server is heavily loaded and does not respond to NTP queries;

{{<kb-detail>}}
A heavily-loaded router is not the best choice for an authoritative NTP server in your network. The replies to the incoming NTP requests are sent from the *NTP* process, which is a medium-priority process in Cisco IOS. All packet switching activities as well as high-priority processes will be executed before the router is able to reply to an NTP request. In most UNIX implementations (including Linux) you could [run the NTP processing in the kernel](http://www.cis.udel.edu/~mills/ntp/html/kern.html) to get microsecond-level accuracy.
{{</kb-detail>}}

Optional configuration steps:

* If you use access lists to protect your NTP server, you should ensure that the NTP packets sent by a router are always sent from the same IP address (usually from the router’s loopback interface). To specify the source IP address globally, use the **ntp source _interface_** configuration command. To specify the source IP address for a specific NTP peer or upstream server, use the **ntp peer|server _ip-address_ source _interface_** configuration command.
* If you’re concerned about the memory consumption of a core NTP server, you can limit the number of associations it supports with the **ntp max-associations _number_** configuration command.

And finally, a router will not be able to act as a standalone NTP server (in case all upstream servers and peers are lost) unless you:

* Store the NTP-synchronized time value in the internal battery backed-up clock with the **ntp update-calendar** configuration command;

* Configure the router to become a stratum X server with the **ntp master *stratum*** configuration command. The *stratum* value you use in the **ntp master** configuration command should be at least the maximum possible stratum value of all upstream NTP servers increased by two.

## Configuration Example

We'll configure NTP on a remote site router (S1) running Cisco IOS in the following sample network:

{{<figure src="../config-network.png" caption="Sample network using NTP synchronization">}}

We'll configure the following NTP parameters:

* The central server (NTP Server) and the upstream router (C1) will be NTP servers;
* The redundant router (S2) on the same remote site will be NTP peer;
* The router will act as a standalone NTP server with stratum 10;
* NTP packets toward the NTP servers will be sent with the source address of the loopback interface whereas the NTP synchronization with S2 will use the IP address of the Fast Ethernet interface;
* The router will periodically update its internal clock.

{{<cc>}}NTP configuration on S1{{</cc>}}
```
ntp logging
ntp source Loopback0
ntp master 10
ntp update-calendar
ntp server NTP-Server
ntp peer S2 source FastEthernet0/0
ntp server C1
```

{{<note>}}The hostnames used in the **ntp server** and **ntp peer** commands are resolved immediately and stored as IP addresses in the Cisco IOS router configuration.{{</note>}}
