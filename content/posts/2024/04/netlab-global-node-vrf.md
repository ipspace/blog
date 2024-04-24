---
title: "netlab: Global and Node VRFs"
date: 2024-04-29 08:37:00+0200
tags: [ netlab ]
netlab_tag: vlan_vrf
series_title: Global and Node VRFs
---
When designing the _netlab_ VRF configuration module, I tried to make it as flexible as possible while using the minimum number of awkward nerd knobs. As is often the case[^CP], the results could be hard to grasp, so let's walk through the various scenarios of using *global* and *node* VRFs.

[^CP]: See also: C, Perl

*netlab* allows you to define a VRF in the lab topology **vrfs**  dictionary (global VRF) or in a node **vrfs** dictionary (node VRF). In most cases, you'd define a few global VRFs and move on.
<!--more-->
### Global VRFs

The following lab topology defines a single (global) VRF and creates a VRF link between nodes R1 and R2:

{{<printout>}}
defaults.device: eos
module: [ vrf ]

vrfs:
  red:
    links: [ r1-r2 ]

nodes:
  r1:
  r2:
{{</printout>}}

_netlab_ assigns an ID, a route distinguisher, and import/export route targets to the global VRF. As both nodes use the same VRF, that information is copied into the node **vrfs** dictionary. 

You can use the `netlab create` command (to perform the data model transformation) followed by the `netlab inspect --node` command to see the resulting values[^NR]. As expected, both nodes use the same RD and RT for the **red** VRF.

[^NR]: The ability to specify multiple nodes in the **netlab inspect** command is brand new and will be included in the 1.8.2 release.

{{<ascii>}}
% netlab inspect --node r1,r2 vrfs.red
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ r1            ┃ r2            ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ af:           │ af:           │
│   ipv4: true  │   ipv4: true  │
│ export:       │ export:       │
│ - '65000:1'   │ - '65000:1'   │
│ id: 1         │ id: 1         │
│ import:       │ import:       │
│ - '65000:1'   │ - '65000:1'   │
│ rd: '65000:1' │ rd: '65000:1' │
│ vrfidx: 100   │ vrfidx: 100   │
└───────────────┴───────────────┘
{{</ascii>}}

### Global and Node VRFs

You can also define a VRF that is used by a single node. For example, let's add **blue** VRF to the R1 and connect it to a global interface on R2:

{{<printout>}}
defaults.device: eos
module: [ vrf ]

vrfs:
  red:
    links: [ r1-r2 ]

nodes:
  r1:
    vrfs:
      blue:
  r2:

links:
- r1:
    vrf: blue
  r2:
{{</printout>}}

R1 has two VRFs (**red** and **blue**), R2 has a single VRF (**red**). The ID/RD/RT values of the **red** VRF match between R1 and R2:

{{<ascii>}}
% netlab inspect --node r1,r2 vrfs
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ r1              ┃ r2              ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ blue:           │ red:            │
│   af:           │   af:           │
│     ipv4: true  │     ipv4: true  │
│   export:       │   export:       │
│   - '65000:2'   │   - '65000:1'   │
│   id: 2         │   id: 1         │
│   import:       │   import:       │
│   - '65000:2'   │   - '65000:1'   │
│   rd: '65000:2' │   rd: '65000:1' │
│   vrfidx: 101   │   vrfidx: 100   │
│ red:            │                 │
│   af:           │                 │
│     ipv4: true  │                 │
│   export:       │                 │
│   - '65000:1'   │                 │
│   id: 1         │                 │
│   import:       │                 │
│   - '65000:1'   │                 │
│   rd: '65000:1' │                 │
│   vrfidx: 100   │                 │
└─────────────────┴─────────────────┘
{{</ascii>}}

### Node VRFs

It's also possible to define node VRFs without defining any global VRFs. When doing that, don't reuse the same VRF name on multiple nodes, as the seemingly identical VRFs won't have the same RD/RT values; netlab treats every node VRF that does not match a global VRF as an independent object.

Let's modify our first example and define the **red** VRF on R1 and R2 without defining it globally:

{{<printout>}}
defaults.device: eos
module: [ vrf ]

nodes:
  r1:
    vrfs:
      red:
  r2:
    vrfs:
      red:

links:
- vrf: red
  r1:
  r2:
{{</printout>}}

_netlab_ does not try to match the **red** VRF across nodes and generates different ID/RD/RT values for each VRF instance. That probably doesn't matter in a VRF Lite scenario, but it definitely wouldn't work in an MPLS/VPN or EVPN environment where route targets matter.

{{<ascii>}}
% netlab inspect --node r1,r2 vrfs
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ r1              ┃ r2              ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ red:            │ red:            │
│   af:           │   af:           │
│     ipv4: true  │     ipv4: true  │
│   export:       │   export:       │
│   - '65000:1'   │   - '65000:2'   │
│   id: 1         │   id: 2         │
│   import:       │   import:       │
│   - '65000:1'   │   - '65000:2'   │
│   rd: '65000:1' │   rd: '65000:2' │
│   vrfidx: 100   │   vrfidx: 100   │
└─────────────────┴─────────────────┘
{{</ascii>}}

**Long story short:** Only use node VRFs if you have an excellent reason to do it.
