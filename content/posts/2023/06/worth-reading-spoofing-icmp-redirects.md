---
title: "Spoofing ICMP Redirects for Fun and Profit"
date: 2023-06-10 06:18:00
tags: [ security, IP routing ]
---
Security researches found another ICMP redirect SNAFU: 
[a malicious wireless client can send redirects on behalf of the access point](https://blog.apnic.net/2023/05/29/mitm-attacks-in-public-wi-fi-networks-without-rogue-access-points/) redirecting another client's traffic to itself.

I'm pretty sure the same trick works on any layer-2 technology; the sad part of this particular story is that the spoofed ICMP packet traverses the access point, which could figure out what's going on and drop the packet. Unfortunately, most of the access points the researchers tested were unable to do that due to limitations in the NPUs (a fancier word for SmartNIC) they were using.

{{<jump>}}[Keep reading](https://blog.apnic.net/2023/05/29/mitm-attacks-in-public-wi-fi-networks-without-rogue-access-points/){{</jump>}}