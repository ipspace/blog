---
kb_section: MH_SOHO
minimal_sidebar: true
title: Monitoring Reliable Static Routing
alt_section: posts
---
The reliable static routes silently appear or disappear from the IP routing table based on the state of the attached **track** object; the only means of monitoring their state is with the **show ip route track-table** command or with the **debug track** command.

{{<cc>}}Show tracked routes{{</cc>}}
```
GW#show ip route track-table
 ip route 0.0.0.0 0.0.0.0 Serial0/0/0 10 name ISP_A track 100 state is [down]
```

{{<cc>}}Debug tracking{{</cc>}}
```
GW#debug track
06:49:44: Track: 100 Down change delayed for 10 secs
06:49:54: Track: 100 Down change delay expired
06:49:54: Track: 100 Change #26 rtr 100, reachability Up->Down
06:50:24: Track: 100 Up change delayed for 20 secs
06:50:34: Track: 100 Up change delay cancelled
06:58:59: Track: 100 Up change delayed for 20 secs
06:59:19: Track: 100 Up change delay expired
06:59:19: Track: 100 Change #25 rtr 100, reachability Down->Up
```

{{<note>}}The debugging printout in Listing 10 illustrates a real-life scenario where the next-hop router became temporarily reachable during the bootstrap process and disappeared a few seconds later (the *change delay cancelled* printout).{{</note>}}

While the silent modification of the IP routing table might be acceptable in most situations (after all, you don’t get notified when a regular IP route disappears from the routing table either), you might want to know if your primary ISP is unreachable (similar to the interface up/down events you would get with traditional access methods like leased lines or Frame Relay access). The *Embedded Event Manager 2.2* (introduced in IOS release 12.4(2)T) is the ideal solution, as you can trigger EEM applets (or TCL scripts) whenever a **track** object’s state changes with the **event track** configuration command.

To display the changes in a tracked object state, you can define two EEM applets, one triggered on the **down** change, another one triggered on the **up** change. If you only want to be notified that the state has changed, the only **action** you need to specify is the **syslog msg** action, but you can perform any number of actions you want (for example, send an e-mail to the network manager or even reconfigure the router). The next printouts show a sample EEM configuration and the printouts is generates.

{{<cc>}}IOS EEM applet generates syslog messages on tracked object state change{{</cc>}}
```
event manager applet ISP_A_down
 event track 100 state down
 action 1.0 syslog msg "ping to 172.16.1.2 from Serial 0/0/0 failed"
event manager applet ISP_A_up
 event track 100 state up
 action 1.0 syslog msg "172.16.1.2 is reachable"
```

{{<cc>}}Sample EEM printouts{{</cc>}}
```
07:02:19: %HA_EM-6-LOG: ISP_A_down: ping to 172.16.1.2 from Serial 0/0/0 failed
07:03:19: %HA_EM-6-LOG: ISP_A_up: 172.16.1.1 is reachable
```
