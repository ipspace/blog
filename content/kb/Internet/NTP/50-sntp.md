---
kb_section: NTP
minimal_sidebar: true
pre_scroll: true
title: SNTP Configuration
url: /kb/Internet/NTP/50-sntp.html
---
The SNTP configuration in Cisco IOS is (as one would expect) much simpler than the NTP configuration:

* You can configure the SNTP-related logging with the **sntp logging** configuration command;
* Upstream NTP server is configured with the **sntp server *ip-address*** configuration command. You can configure multiple servers for redundancy purposes.

{{<note>}}You cannot configure the SNTP process running on a Cisco IOS router to update the internal clock, as you're supposed to use SNTP solely on the low-end models with no battery backed-up clock.{{</note>}}

The SNTP process will not synchronize to the configured SNTP servers if you’ve previously entered any NTP-related configuration commands on the router (**ntp logging** is enough), as the *NTP* process in Cisco IOS receives replies that should be received by the *SNTP* process (remember: NTP and SNTP use the same UDP port number). The only way to fix this problem is to reload the router.

{{<note warn>}}A router using SNTP synchronization cannot be used to provide NTP services to downstream clients, as these services would require the NTP process to run, thus blocking the SNTP synchronization.{{</note>}}

### Configuration Example

We'll configure SNTP on the WAN edge router (S1) used on a non-redundant small site small-site:

{{<figure src="design-non-redundant.png" caption="Simple remote site using SNTP synchronization">}}

The configuration commands are as simple as they can get:

{{<cc>}}SNTP configuration{{</cc>}}
```
sntp logging
sntp server C1
sntp server C2
sntp server NTP-Server
```

The SNTP process should quickly acquire the correct time from the NTP servers and generate *syslog* messages as it synchronizes with the servers (see the following listing). Multiple synchronizations might occur if the SNTP process reaches a high-stratum NTP server before a low-stratum one.

{{<cc>}}SNTP synchronizations on the Site router{{</cc>}}
```
00:00:56: %SYS-6-CLOCKUPDATE: System clock has been updated from 14:09:51 UTC Mon Feb 25 2008 to 13:29:59 UTC Mon Feb 25 2008, configured from SNTP by 10.0.0.5.
00:01:59: %SYS-6-CLOCKUPDATE: System clock has been updated from 13:31:02 UTC Mon Feb 25 2008 to 13:31:02 UTC Mon Feb 25 2008, configured from SNTP by 10.0.0.10
```

The **show sntp** command can be used to display the current synchronization status:

{{<cc>}}SNTP status on the Site router{{</cc>}}
```
Site#show sntp
SNTP server     Stratum   Version    Last Receive
10.0.0.5           7         1        00:00:56
10.0.0.10          6         1        00:01:03    Synced
10.0.0.6           7         1        00:00:15
```

