---
date: 2008-04-03 06:34:00.001000+02:00
tags:
- network management
- ERM
title: Use UDP flood to increase router's CPU load
url: /2008/04/use-udp-flood-to-increase-router-cpu/
---
If you want to test the [ERM policies](/2008/03/detect-routers-operating-in-process/) in a controlled environment, it\'s almost mandatory to have tools that allow you to overload the router. One way to overload a router is to flood it with UDP packets. Flooding a router\'s IP address, you\'re guaranteed to raise the CPU to 100%, with majority of the *process* CPU being used by the *IP Input* process (the *interrupt* CPU load will also be significant).

This phenomenon illustrates very clearly why it\'s so important to have inbound access lists protecting the router\'s own IP addresses on all edge interfaces.
<!--more-->
If you want to stress-test the router\'s forwarding functionality, you could use the host route to the **null0** interface; all packets sent to that IP address will be CEF-switched, so the only impact of the UDP flood to the unreachable IP address will be the increased *interrupt* CPU load. I was able to increase the interrupt CPU load to close to 50% on a 2800 router using a virtual PC with a Fast Ethernet interface.

And just in case you need it, here is the configuration from my test router. All packets sent to 10.0.0.22 are CEF-switched and dropped (the CPU load from the *IP input* process is negligible).

```
interface FastEthernet 0/0
 ip address 10.0.0.1 255.255.255.0
!
ip route 10.0.0.22 255.255.255.255 null 0
```
