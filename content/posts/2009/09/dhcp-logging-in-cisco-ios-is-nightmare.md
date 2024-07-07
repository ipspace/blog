---
date: 2009-09-28 06:43:00.001000+02:00
tags:
- DHCP
title: DHCP Logging in Cisco IOS Is a Nightmare
url: /2009/09/dhcp-logging-in-cisco-ios-is-nightmare/
---
One of the readers sent me an interesting question: he'd like to know the IP address of his home router (to be able to connect to it from the office), but its IP address is assigned through DHCP and changes occasionally.

I wanted to solve the problem by hooking an EEM applet onto the DHCP-6-ADDRESS_ASSIGN *syslog* message. No good; as it turns out, Cisco IOS generates the logging message only when a DHCP-acquired IP address is assigned to an interface without one. If the IP address is changed via DHCP, the change is not logged.
<!--more-->
One could understand the faulty programmers' logic if the initial address assignment would be different from the address change, but DHCP is such a simple protocol that any [change in client's IP address](/2009/09/expired-dhcp-lease-bounces-interface/) requires the [client to enter the INIT state](http://www.tcpipguide.com/free/t_DHCPGeneralOperationandClientFiniteStateMachine.htm), so acquiring a new IP address is no different from changing an existing one. I guess they had to take special precautions not to log the address change (and ensure we have another interesting challenge to chew on).

Fortunately, the IP routing table changes after every change in interface IP address, and you can catch that event with EEM.
