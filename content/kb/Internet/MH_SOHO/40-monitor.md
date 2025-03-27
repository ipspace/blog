---
kb_section: MH_SOHO
minimal_sidebar: true
title: Monitoring Reliable Static Routing
alt_section: posts
---
Reliable static routes silently appear or disappear from the IP routing table based on the state of the attached **track** object; the only way to monitor their state is to use the **show ip route track-table** command.

{{<cc>}}Show tracked routes{{</cc>}}
```
GW#show ip route track-table
 ip route 0.0.0.0 0.0.0.0 Serial0/0/0 10 name ISP_A track 100 state is [down]
```

However, state tracking generates logging messages, and you can use the **debug track** command to get even more details.
 
{{<cc>}}Track state logging and debugging{{</cc>}}
```
GW#debug track
06:49:44: Track: 100 Down change delayed for 10 secs
06:49:54: Track: 100 Change #24 ip sla 100, reachability Up->Down
06:49:54: %TRACK-6-STATE: 100 ip sla 100 reachability Up -> Down
06:50:24: Track: 100 Up change delayed for 20 secs
06:50:34: Track: 100 Up change delay cancelled
06:58:59: Track: 100 Up change delayed for 20 secs
06:59:19: Track: 100 Change #25 ip sla 100, reachability Down -> Up
06:59:19: %TRACK-6-STATE: 100 ip sla 100 reachability Down -> Up
```

{{<note>}}The debugging printout illustrates a real-life scenario where the next-hop router became temporarily reachable during the bootstrap process and disappeared a few seconds later (the *change delay cancelled* printout).{{</note>}}

Suppose you need more than the logging messages the **track** objects generate. In that case, you can use the *Embedded Event Manager* with the **event track** configuration command to trigger EEM applets (or TCL scripts) whenever a **track** object’s state changes.

For example, we'll define two EEM applets: one triggered on the **down** change, and another triggered on the **up** change. We'll use a simple **syslog msg** action; you can add other actions, like emailing the network manager or even reconfiguring the router (the complete router configuration is [available on GitHub](https://github.com/ipspace/netlab-examples/blob/master/multihoming/small-site/gw-eem-applet.cfg)).

The following printouts show a sample EEM configuration and the printouts it generates.

{{<cc>}}IOS EEM applet generates syslog messages on tracked object state change{{</cc>}}
```
event manager applet ISP_A_down
 event track 100 state down
 action 1.0 syslog msg "ping to 172.16.1.2 from GigabitEthernet 0/2 failed"
event manager applet ISP_A_up
 event track 100 state up
 action 1.0 syslog msg "172.16.1.2 is reachable"
```

{{<cc>}}Sample track logging and EEM printouts{{</cc>}}
```
00:38:52: %TRACK-6-STATE: 100 ip sla 100 reachability Up -> Down
00:38:52: %HA_EM-6-LOG: ISP_A_down: ping to 172.16.1.2 from GigabitEthernet 0/2 failed
00:39:22: %TRACK-6-STATE: 100 ip sla 100 reachability Down -> Up
00:39:22: %HA_EM-6-LOG: ISP_A_up: 172.16.1.2 is reachable
```

### Revision History

2025-03-31
: * Recreated the router configurations and printouts with IOSv release 15.6(1)T.
  * Object tracking generates logging messages in newer IOS releases

