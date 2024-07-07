---
date: 2007-04-05 10:55:00+02:00
tags:
- network management
- EEM
title: Reload a Router When Ping Fails
url: /2007/04/reload-router-when-ping-fails/
---
One of my readers has [asked an interesting question](/2007/01/youve-asked-for-it-series/): can you reload a router when pinging a specific IP address from it fails? While there are other ways of dealing with stuck interfaces or routing processes, sometimes such a drastic measure is the only workaround, so here\'s how you do it:
<!--more-->
-   Configure an IP SLA measurement. You might want to use the **after** parameter in the **ip sla schedule** command to ensure the router does not get reloaded immediately after the startup due to IP routing table not being populated.
-   Configure a tracked object based on the IP SLA measurement with the **track *object-id* rtr *sla-id* reachability** command
-   Configure an EEM applet that will reload the router if the tracked object enters the down state

Use configuration similar to the one below for the EEM applet:

``` {.code}
event manager applet PingHasFailed
 event track 100 state down
 action 1.0 syslog msg "Ping has failed, reloading the router"
 action 2.0 reload
```
