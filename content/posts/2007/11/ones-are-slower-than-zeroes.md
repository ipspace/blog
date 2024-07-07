---
url: /2007/11/ones-are-slower-than-zeroes/
title: "Ones Are Slower than Zeroes"
date: "2007-11-11T06:59:00.000+01:00"
tags: [ WAN ]
---
Thinking about the implications of [bit stuffing I wrote about in the SDLC post](/2007/11/back-to-roots-it-all-started-with-sdlc/), I realized that long sequences of ones would be transmitted slower than long sequences of zeroes due to an extra bit being inserted after every fifth consecutive one. The theory would predict a 20% decrease in transmission speed.

Of course I wanted to test this phenomenon immediately. I connected two routers with a low-speed (64 kbps) link, and started a series of pings. Not surprisingly, the results confirmed the theory:
<!--more-->
```
Internal-Core#ping 197.1.1.49 data 0000 size 1200 repeat 50
Sending 50, 1200-byte ICMP Echos to 197.1.1.49, timeout is 2 seconds:
Packet has data pattern 0x0000
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (50/50), round-trip min/avg/max = 608/608/632 ms

Internal-Core#ping 197.1.1.49 data FFFF size 1200 repeat 50
Sending 50, 1200-byte ICMP Echos to 197.1.1.49, timeout is 2 seconds:
Packet has data pattern 0xFFFF
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (50/50), round-trip min/avg/max = 724/724/728 ms
```

The results are almost too close to the predicted ones, but they are real :)

