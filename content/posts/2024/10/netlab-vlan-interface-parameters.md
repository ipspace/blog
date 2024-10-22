---
title: "netlab: How do I Specify VLAN Interface Parameters"
series_title: "Specifying VLAN Interface Parameters"
date: 2024-10-28 07:53:00+0200
tags: [ netlab ]
netlab_tag: vlan_vrf
---
Similarly to how it [handles VRFs](/2024/05/netlab-vrf-instantiation/), *netlab* automatically creates VLANs on a lab device if the device uses them on any access- or trunk link or if the VLAN is mentioned in the node **vlans** dictionary.

If the VLAN is an IRB VLAN (which can be modified globally or per node with the [VLAN **mode** parameter](https://netlab.tools/module/vlan/#vlan-forwarding-modes)), *netlab* also creates the VLAN (or SVI, or BVI) interface. But how do you specify the parameters of the VLAN interface?
<!--more-->
Here's the correct answer: you have to [specify them in the node VLAN definition](https://netlab.tools/module/vlan/#vlan-interface-parameters). For example, if you want to change the OSPF cost of the VLAN subnet for a single node connected to that VLAN, use something along these lines:

{{<cc>}}Changing the OSPF cost for a single VLAN interface{{</cc>}}
```
vlans:
  red:
    ospf.cost: 10
    
nodes:
  sw1:
    vlans:
      red:
        ospf.cost: 20
```

The above snippet will set the OSPF cost to 20 on SW1's *red* VLAN interface but keep it at 10 on all other nodes' *red* VLAN interfaces.

**Is there another way to set VLAN interface attributes?** No. To be fair, we did copy them from the first VLAN link but then decided that was too confusing and potentially unpredictable and switched to the **vlans** dictionary model.

**But I can still set X on the first access interface.** Please don't. The next time someone reports a related bug and we have to touch the code, that functionality will disappear.

**But setting Y in the vlans dictionary does not work.** Sadly, you might be correct, but we're working on it. We already fixed [the **gateway.vrrp** stuff](https://github.com/ipspace/netlab/issues/1349) and are working on fixing the [static IP addressing bug](https://github.com/ipspace/netlab/issues/1411). If you find anything else, please [open a GitHub issue](https://github.com/ipspace/netlab/issues/new/choose). Thank you!
