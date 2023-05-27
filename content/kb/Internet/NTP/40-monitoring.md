---
kb_section: NTP
minimal_sidebar: true
title: Monitoring NTP
url: /kb/Internet/NTP/40-monitoring.html
pre_scroll: true
---
Cisco IOS provides two commands to monitor the status of the embedded NTP server:

* The **show ntp status** command displays the state of the internal clock. This printout indicates the synchronization status, the stratum of the local NTP server, the internal clock frequency, the current time (reference time) and the offset and dispersion to the NTP server to which the router has synchronized.

{{<cc>}}Time synchronization status on S1{{</cc>}}
```
S1#show ntp status
Clock is synchronized, stratum 7, reference is 10.0.0.10
nominal freq is 250.0000 Hz,actual freq is 250.0005 Hz, precision is 2\*\*18
reference time is CB6D3483.720B1C23 (12:35:15.445 UTC Mon Feb 25 2008)
clock offset is 0.7809 msec, root delay is 1.51 msec
root dispersion is 41.38 msec, peer dispersion is 29.30 msec
```

{{<note>}}When the synchronization process with an upstream server reachable over high-speed links has completed, the clock offset and the dispersion should both be not more than 100 milliseconds.{{</note>}}

* The **show ntp associations** command displays all configured and dynamically acquired NTP servers and peers, their stratum values, reference clocks (IP addresses of the upstream NTP servers), polling intervals, reachability information, delays and offsets (Listing 3).

{{<cc>}}NTP associations on S1{{</cc>}}
```
S1#show ntp associations

    address      ref clock   st when  poll reach delay offset   disp
+~10.0.0.5     10.0.0.10      4   33   512  377   45.9  18.60    4.1
 ~192.168.0.6  0.0.0.0       16    -  1024    0    0.0   0.00  6000.
 ~127.127.7.1  127.127.7.1    9   22    64  377    0.0   0.00    0.0
*~10.0.0.10    127.127.1.0    3  436   512  377   45.6 -22.51    6.0
* master (synced), # master (unsynced), + selected, - candidate, ~ configured
```

A single NTP neighbor is selected as the NTP master. If the local clock is synchronized to the NTP master, its status is *master (synced*), otherwise it’s *master (unsynced).* Other NTP neighbors could be *selected* for potential synchronization should the current master fail or be *candidates* for synchronization.

In-depth NTP association information can be displayed with the **show ntp associations detail** command. Unfortunately, this command does not accept the IP address of the NTP neighbor; the only means of reducing its output is to use the output filters:

{{<cc>}}Detail of NTP association between S2 and NTP server 10.0.0.5{{</cc>}}
```
S1#show ntp associations detail | begin ^10.0.0.5
10.0.0.5 configured, selected, sane, valid, stratum 4
ref ID 10.0.0.10, time CB6D36DE.B61F1589 (12:45:18.711 UTC Mon Feb 25 2008)
our mode active, peer mode active, our poll intvl 256, peer poll intvl 256
root delay 2.55 msec, root disp 53.92, reach 276, sync dist 59.280
delay 0.66 msec, offset -7.9848 msec, dispersion 2.87
precision 2**18, version 3
org time CB6D3716.B5B90617 (12:46:14.709 UTC Mon Feb 25 2008)
rcv time CB6D3716.B7DA45D6 (12:46:14.718 UTC Mon Feb 25 2008)
xmt time CB6D375F.710E25CA (12:47:27.441 UTC Mon Feb 25 2008)
filtdelay =    0.66   1.80  -0.34   2.30   1.98   2.49   6.68  12.79
filtoffset =  -7.98  -8.56 -10.49 -12.60 -11.89 -10.21  -4.59  13.11
filterror =    0.85   2.81   4.76   6.71   7.69   9.09  10.07  11.05

10.0.0.10 configured, our_master, sane, valid, stratum 3
ref ID 127.127.1.0, time CB6D36E7.BDA843E2 (12:45:27.740 UTC Mon Feb 25 2008)
… rest of printout deleted …
```
