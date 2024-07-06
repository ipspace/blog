---
date: 2008-06-03 07:02:00.001000+02:00
tags:
- network management
title: Another Way to Generate SNMP Trap on High CPU Load
url: /2008/06/another-way-to-generate-snmp-trap-on.html
---
When testing the [ERM functionality that together with an EEM applet generates SNMP traps whenever the CPU load exceeds predefined thresholds](/2008/06/generate-snmp-trap-on-high-cpu-load.html), I started to wonder what the **snmp-server enable traps cpu threshold** command does. 

After lenghty conversation with uncle Google and Cisco documentation, I found that there\'s another way to detect and report high CPU load in Cisco IOS: the [CPU threshold notification](http://www.cisco.com/en/US/docs/ios/netmgmt/configuration/guide/nm_cpu_thresh_notif_ps6441_TSD_Products_Configuration_Guide_Chapter.html) introduced in IOS release 12.3T.
<!--more-->
To use this feature, you have to configure the thresholds with the **process cpu threshold** configuration command and enable related SNMP traps with the **snmp-server enable traps cpu threshold**. For example, to send SNMP traps whenever the total CPU load measured over a 30-second interval exceeds 40%, use the following configuration:

``` {.code}
snmp-server enable traps cpu threshold
process cpu threshold type total rising 40 interval 30
```
