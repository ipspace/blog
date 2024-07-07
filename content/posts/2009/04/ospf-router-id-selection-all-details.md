---
date: 2009-04-28 06:36:00.001000+02:00
lastmod: 2020-11-18 13:37:00
ospf_tag: details
tags:
- OSPF
title: 'OSPF Router ID Selection: the Gory Details'
url: /2009/04/ospf-router-id-selection-all-details/
---
After I wrote the [OSPF router ID selection trivia](/2009/04/ospf-router-id-selection-trivia/) post, I wanted to figure out all the details of the OSPF router ID selection algorithm. As I’ve expected, the [common wisdoms are mostly correct](/2007/10/ospf-router-id-does-not-change-when/), but they fail to cover the [interesting border cases](/2008/08/ospf-in-vrf-requires-box-unique-router/). 

Here's the complete algorithm (as observed on Cisco IOS in 2009):
<!--more-->

---

Every OSPF process running in Cisco IOS requires a router-wide unique router ID. An IP address of an active interface is commonly used as the OSPF router ID; you can also use the **router-id _address_** router configuration command to ensure the OSPF router ID does not change even when the interface IP addresses change.

{{<note info>}}Although the OSPF router ID looks like an IP address in the configuration command, it's just a 32-bit quantity and can be anything.{{</note>}}

OSPF router ID should not be changed after the OSPF process has been started. OSPF router ID change resets all OSPF adjacencies, resulting in temporary router outage. The router also has to originate new copies of all its LSAs with the new router ID. Stale copies of the LSAs originated by the “old” OSPF process remain in the OSPF topology databases of all routers until they expire (their age increases beyond *max-age*).

### Router ID Selection Algorithm

If the **router-id** is specified in the OSPF configuration, the specified value is used. If the value configured with the **router-id** command overlaps with the router ID of another already active OSPF process, the **router-id** command fails.

If OSPF router ID was not set with the **router-id** configuration command (no **router-id** command was used in the OSPF configuration or there was a router ID overlap with another OSPF process), OSPF uses an interface IP address as its router ID.

The following algorithm is used to select an interface IP address as the OSPF router ID:

-   IP addresses of all applicable loopback interfaces are collected. Addresses already used as OSPF router ID of other OSPF processes are removed. If any addresses are left, the highest IP address is used as the OSPF router ID.

{{<note>}}*Applicable interfaces* are operational (line protocol is up) interfaces in the same routing domain (VRF or the global IP routing table) as the OSPF process.{{</note>}}

-   If the OSPF router ID has not been selected in the first step, IP addresses of all other applicable interfaces are collected. OSPF router IDs of other active OSPF processes in the same routing domain are removed from the list and the highest IP address is used.
-   If the router was still not able to select an OSPF router ID, an error message is logged and the OSPF process does not start.

An OSPF process that failed to select a router ID retries the selection process every time an IP address becomes available (an applicable interface changes its state to *up* or an IP address is configured on an applicable interface).

### Changing the OSPF router ID

Once an OSPF router ID is selected, it is not changed even if the interface that was used to select it changes its operational state or its IP address.

{{<note info>}}Early Cisco IOS releases changed the OSPF router ID when the underlying interface state changed, resulting in unnecessary network instabilities.{{</note>}}

To change the OSPF router ID, you have to reset the OSPF process with the **clear ip ospf process** command (even when the new router ID was requested with the **router-id** router configuration command).
