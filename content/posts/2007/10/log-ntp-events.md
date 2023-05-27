---
date: 2007-10-03 06:51:00+02:00
tags:
- NTP
title: Log the NTP events
url: /2007/10/log-ntp-events.html
pre_scroll: true
---
I almost started writing an EEM applet that would detect and log the changes in router's system time caused by NTP synchronizations, but then I've decided to check the IOS documentation first and found the **ntp logging** command.
<!--more-->
For example, if you configure...

``` code
rtr(config)#ntp logging
rtr(config)#ntp server 172.16.0.12
```

... the router will generate the following syslog messages when it synchronizes its time with the NTP server:

```
%NTP-6-RESTART: NTP process starts
%SYS-6-CLOCKUPDATE: System clock has been updated from 17:06:03 UTC Fri Mar 30 2007 to 17:04:07 UTC Fri Mar 30 2007, configured from NTP by 172.16.0.12.
%NTP-5-PEERSYNC: NTP synced to peer 172.16.0.12
```
