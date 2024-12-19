---
kb_section: EventDampening
minimal_sidebar: true
pre_scroll: true
title: Configure and Monitor IP Event Dampening
date: 2025-01-08 08:18:00+0100
---
The IP Event Dampening is configured with a single interface-level configuration command **dampening \[ *half-time* *reuse-threshold* *suppress-threshold* *max-suppress-time* \[ restart *penalty* \] \]** (the default values assumed by Cisco IOS are summarized in the next table). You can change as many parameters as you wish; if you specify a different half-time period and don’t specify the maximum suppress time, it’s four times the half-time period.

| Parameter	| Default value |
|-----------|--------------:|
| half time	| 5 seconds |
| reuse threshold	| 1000 |
| suppress threshold | 2000 |
| maximum suppress time	| 20 seconds |
{ .fmtTable style="width: auto" }

The **dampening** command can be applied only on physical interfaces; IP event dampening does not work on subinterfaces or virtual templates. The events triggering the dampening penalty include a change in the interface state (loss of carrier) and the line protocol state.

There are two confusingly similar commands that monitor the IP event dampening feature: the **show dampening interface**  displays an overview of the IP event dampening configuration and the **show interface dampening** displays the actual status of every interface where the IP event dampening is configured.

{{<cc>}}Display a summary of the IP event-dampening configuration{{</cc>}}
```
router#show dampening interface
2 interfaces are configured with dampening.
1 interface is being suppressed.
Features that are using interface dampening:
  IP Routing
  HSRP
```

{{<cc>}}Per-interface status of the IP event dampening{{</cc>}}
```
router#show interfaces dampening
Serial0/0/0
  Flaps Penalty  Supp ReuseTm HalfL ReuseV SuppV MaxSTm MaxP Restart
      0       0 FALSE       0    20   1000  2000   80  16000       0
Serial0/1/0
  Flaps Penalty  Supp ReuseTm HalfL ReuseV SuppV MaxSTm MaxP Restart
      0    2245  TRUE      33    15    500  2000   60   8000     500
```

The IP Event Dampening feature generates no logging messages; the only means to detect when an interface has been suppressed and later unsuppressed is through the **debug dampening interface** command.

{{<note>}}You cannot use the event tracking feature of Cisco IOS, as the **track interface ip routing** command does not consider the dampening status of the interface and reports it as *up* even when it’s dampened.{{</note>}}
