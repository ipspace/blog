---
date: 2010-11-22 06:49:00.002000+01:00
tags:
- IP routing
- EEM
title: Time-Based Static Routes
url: /2010/11/time-based-static-routes/
---
Before someone accuses me of being totally FCoE/DCB-focused, here's an interesting EEM trick. Damian wanted to have time-dependent static routes to ensure expensive backup path is only established during the working hours. I told him to use cron with EEM to modify router configuration (and obviously lost him in the acronym forest)\... but there's an even better solution: use reliable static routing and modify just the track object's state with EEM.
<!--more-->
Static route first: we'll create a floating default route (we're solving the backup path problem) tied to a track object.

``` {.code}
ip route 0.0.0.0 0.0.0.0 Tunnel 0 250 track 42
```

Next, we have to create the **track** object itself. We'll create a **stub-object** since it won't track an IP SLA or interface state; we just need a flag that we'll set with EEM. We also have to decide what happens after a router reload. It might be a good idea to have the backup path available, so the default state of the track object should be **up**.

``` {.code}
track 42 stub-object
 default-state up
```

Last step: create two EEM applets. One of them will set the track object's state to *down* at the end of the business day, the other one will set it to *up* in the morning.

``` {.code}
event manager applet DisableBackup
 event timer cron name DisableBackup cron-entry "0 17 * * *"
 action 1.0 track set 42 state down
!
event manager applet EnableBackup
 event timer cron name EnableBackup cron-entry "0 8 * * 1-5"
 action 1.0 track set 42 state up
```

You might wonder why you should use this slightly convoluted solution when you could simply modify the router configuration in EEM applets. The answer is simple: if your EEM applets are modifying the configuration, you never know whether you should save configuration changes before reloading the router... and if you use a configuration monitoring tool, you might get lots of unnecessary alerts.

## More information

Related solutions:

-   [Periodic router reload](/2006/10/periodic-router-reload/)
-   [Kron: poor-man\'s cron](/2007/11/kron-poor-man-cron/)
-   [Time-based BGP policy routing](/2008/02/time-based-bgp-policy-routing/)
