---
kb_section: RouterConfigManagement
minimal_sidebar: true
pre_scroll: true
title: What’s Going On?
date: 2025-01-15 08:01:00+0100
---
Network managers who implemented centralized Authentication, Authorization, and Accounting (AAA) with Cisco’s proprietary TACACS+ protocol could log any command executed on the routers in their network for ages; the rest of us could only guess what someone configuring our routers did to them. The Configuration Change Notification feature, first introduced in IOS release 12.3(14)T and integrated into the mainstream release 12.4, solves this problem. After you configure it, all the configuration commands entered on the router are stored in a circular buffer (you can even specify its length) and optionally sent to a *syslog* server. A typical configuration is shown in the following printout:

{{<cc>}}Configuration commands for Configuration Change Notification and Logging feature{{</cc>}}
```
archive
 log config
  logging enable
  logging size 200
  notify syslog
  hidekeys
```

{{<note>}}The **hidekeys** command hides the passwords and other sensitive information in the log buffer and syslog messages.{{</note>}}

After configuring the Configuration Change Logging, all configuration commands are stored in a circular buffer in the router’s memory. You can inspect the commands with the **show archive log config** command, which displays all configuration commands recently entered on the router or commands entered by a particular user or even within a single configuration session (from the moment you enter **configure terminal** to the time you exit the configuration mode). A sample printout of this command is shown below:

{{<cc>}}Display of logged configuration commands{{</cc>}}
```
fw#show archive log config all
 idx   sess           user@line      Logged command
    1     1        console@console  |  logging enable
    2     1        console@console  |  logging size 200
    3     1        console@console  |  notify syslog
    4     2        console@console  |archive
    5     2        console@console  | log config
    6     2        console@console  |  hidekeys
```

If you’ve configured the **notify syslog** option of the **log config** configuration command, all configuration commands entered on a router are also sent to the logging subsystem, which delivers them to various logging destinations, including console and *syslog* hosts. The syslog messages usually contain the username and the configuration command, but they could also report changes in significant data structures. For example, if you add a local user with the **username** command, the router will generate the two *syslog* messages:

{{<cc>}}Syslog messages generated by security-relevant configuration command{{</cc>}}
```
fw#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
fw(config)#user x password y
01:43:06: %PARSER-5-CFGLOG_LOGGEDCMD: User:console  logged command:username x password *****
01:43:06: %PARSER-5-CFGLOG_LOGGEDCMD: User:console  logged command:!config: USER TABLE MODIFIED
```
