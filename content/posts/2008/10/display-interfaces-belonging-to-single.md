---
date: 2008-10-13 07:20:00.004000+02:00
ospf_tag: config
tags:
- OSPF
title: Display Interfaces Belonging to a Single OSPF Process
url: /2008/10/display-interfaces-belonging-to-single.html
---
I'm constantly receiving interesting OSPF-related queries -- the many hidden details of the OSPF specs result in slightly unexpected behavior and constant amazement of engineers studying OSPF. During this week, I'll focus on a few intriguing OSPF details.

Let's start with an easy one: you can use the **show ip ospf interface brief** command to display the OSPF interface status (including the interface area, OSPF cost, link type, and router status on broadcast links). Unfortunately, this command does not allow you to specify the OSPF process ID and displays interfaces belonging to all OSPF processes (if you run multiple OSPF processes on the router).
:::
Here is a sample printout taken from a router running OSPF processes #2 and #13:

{{<cc>}}The printout contains interfaces from multiple OSPF processes{{</cc>}}
``` code
C1#show ip ospf interface brief
Interface    PID   Area    IP Address/Mask    Cost  State Nbrs F/C
Lo102        2     22      10.2.2.2/32        1     LOOP  0/0
Fa0/0        13    0       10.0.1.1/24        10    BDR   1/1
Lo0          13    0       10.0.0.11/32       1     LOOP  0/0
Se1/0.101    13    1       0.0.0.0/0          64    P2P   1/1
Se1/0.100    13    1       0.0.0.0/0          64    P2P   1/1
```

You can use an output filter to display the interfaces of a single OSPF process. The filter is quite convoluted:

{{<cc>}}Use a filter to display interfaces of a single OSPF process{{</cc>}}
``` code
C1#show ip ospf interface brief | include ^[^ ]+ +13
Fa0/0        13    0       10.0.1.1/24        10    BDR   1/1
Lo0          13    0       10.0.0.11/32       1     LOOP  0/0
Se1/0.101    13    1       0.0.0.0/0          64    P2P   1/1
Se1/0.100    13    1       0.0.0.0/0          64    P2P   1/1 
```

It works like this:

-   The initial caret (`\^`) matches the beginning of the line, ensuring that our filter matches precisely what we expect it to match. Without the initial caret, the filter could generate a match anywhere in the line, potentially resulting in false positives.
-   The `[^ ]+` pattern matches any non-empty (the + sign) string of non-space characters (the `[^ ]` expression matches anything but the whitespace). This part of the pattern matches the interface name.
-   The ` +` pattern matches the string of spaces between the interface name and the process ID.
-   The final part of the pattern (`13`) matches the OSPF process ID.
