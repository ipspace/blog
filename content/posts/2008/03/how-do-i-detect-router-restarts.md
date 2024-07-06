---
date: 2008-03-15 07:13:00.002000+01:00
tags:
- syslog
- EEM
title: How Do I Detect Router Restarts?
url: /2008/03/how-do-i-detect-router-restarts.html
---
Mike Nipp has wondered which *syslog* message to use to [reliably detect router reload](/2007/04/fix-router-configuration-after-reload.html) under all circumstances:

> The problem I had with the SYS-5-RESTART message is I don\'t think you will get one if the power is suddenly pulled from the router. It does do a SNMP-5-COLDSTART and SYS-6-BOOTTIME on boot up.

I did an actual power-cycle test of a router and the SYS-5-RESTART message is reliably generated at every startup, be it from the power cycle or the reload command (I was not able to provoke an on-demand crash ;).
