---
date: 2013-10-21 11:17:00.001000+02:00
tags:
- SDN
- OpenFlow
title: Flow Table Explosion With OpenFlow 1.0 (And Why We Need OpenFlow 1.3)
url: /2013/10/flow-table-explosion-with-openflow-10/
---
The number of OpenFlow flows you can use in hardware switches is one of the major roadblocks in a large-scale OpenFlow deployment. Vendors often use hardware TCAM tables to match OpenFlow entries, and as those tables are expensive to implement in silicon, they tend to be small. Typical TCAM tables have a few thousand entries. 

Is that good enough? As always, the answer depends on the use case, the network size, and implementation details. This blog post will focus on the last part.

**TL&DR summary**: Use switches that support OpenFlow 1.3.
<!--more-->
{{<note update>}}The blog post was cleaned up in 2024; I removed all references to ancient products. While you might argue that OpenFlow is dead anyway, we're still dealing with scenarios where we need a Cartesian product of multiple independent match/action tables (for example, when implementing routing policies with route maps){{</note>}}

### Use Case: Data Center Fabric

The simplest possible OpenFlow data center use case is a traditional (non-virtualized) data center network.

The OpenFlow-based network trying to get feature parity with low-cost traditional ToR switches should support

-   Layer-2 and layer-3 forwarding;
-   Per-port or per-MAC ingress and egress access lists.

We'll focus on a single layer-2 segment (you really don't want to get me started on the complexities of scalable OpenFlow-based layer-3 forwarding) implemented on a single hardware switch (expanding the logic beyond that is a homework assignment). Our segment will have two web servers (port 1 and 2), a MySQL server (port 3), and a default gateway on port 4.

{{<note>}}The default gateway could be a firewall, a router, or a load balancer -- it really doesn't matter if we stay focused on layer-2 forwarding.{{</note>}}

### Step 1: Simple MAC-based forwarding

The OpenFlow controller has to install a few forwarding rules in the switch to get the traffic started. Ignoring the multi-tenancy requirements you need a single flow forwarding rule per destination MAC address:

|  Flow match    |    Action         |
|----------------|-------------------|
|  DMAC = Web-1  |   Forward to port 1 |
|  DMAC = Web-2  |   Forward to port 2 |
|  DMAC = MYSQL-1 |  Forward to port 3 |
|  DMAC = GW     |   Forward to port 4 |
{.fmtTable}

Number of flows needed = number of MAC addresses.

{{<note info>}}Smart switches wouldn't store the MAC-only flow rules in TCAM; they would use other forwarding structures available in the switch like MAC hash tables.{{</note>}}

### Step 2: Multi-Tenant Infrastructure

If you want to implement multi-tenancy, you need multiple forwarding tables (like VRFs), which are not available in OpenFlow 1.0, or you have to add the tenant ID to the existing forwarding table. Traditional switches would do it in two steps:

-   Mark inbound packets with VLAN tags;
-   Perform packet forwarding based on destination MAC address and VLAN tag.

Switches using OpenFlow 1.0 forwarding model cannot perform more than one operation during the packet forwarding process -- they must match the input port and destination MAC address in a single flow rule, resulting in a flow table similar to this one:

|  Flow match                |       Action |
|--------------------------------|-------------------|
|  SrcPort = Port 2, DMAC = Web-1 |  Forward to port 1
|  SrcPort = Port 3, DMAC = Web-1 |  Forward to port 1
|  SrcPort = Port 4, DMAC = Web-1 |  Forward to port 1
|  SrcPort = Port 1, DMAC = Web-2 |  Forward to port 2
|  SrcPort = Port 3, DMAC = Web-2 |  Forward to port 2
|  SrcPort = Port 4, DMAC = Web-2 |  Forward to port 2
{.fmtTable
}
Number of flows needed = sum of (number of tenant MAC addresses \* number of tenant ports). The proof is left as an exercise for the reader.

### Step 3: Access Lists

Let's assume we want to protect the web servers with an input (server-to-switch) port ACL, which would look similar to this one:

|  Match                     |          Action |
|-----------------------------------|--------|
|  TCP SRC = 80                     |   Permit
|  TCP SRC = 443                    |   Permit
|  TCP DST = 53 & IP DST = *DNS*    |   Permit
|  TCP DST = 25 & IP DST = *Mail*   |   Permit
|  TCP DST = 3306 & IP DST = *MySql*|   Permit
|  Anything else                    |   Drop
{.fmtTable}

By now you've probably realized what happens when you try to combine the input ACL with other forwarding rules. The OpenFlow controller has to generate a [*Cartesian product*](http://en.wikipedia.org/wiki/Cartesian_product) of all three requirements: the switch needs a flow entry for every possible combination of input port, ACL entry and destination MAC address.

Number of flows needed = sum of (number of tenant MAC addresses \* number of tenant ports \* number of ACL entries)

Plug in realistic numbers and do the math.

### OpenFlow 1.3 to the Rescue

Is the situation really as hopeless as illustrated above? Of course not -- smart people trying to implement real-life OpenFlow solutions quickly realized bare-bones OpenFlow 1.0 works well only in PPT, lab tests, PoCs and glitzy demos, and started working on a solution.

OpenFlow 1.1 (and later versions) have a concept of *tables* - independent lookup tables that can be chained in any way you wish (further complicating the life of hardware vendors).

This is how you could implement our requirements with switches supporting OpenFlow 1.3:

-   Table #1 -- ACL and tenant classification table. This table would match input ports (for tenant classification) and ACL entries, drop the packets not matched by input ACLs, and redirect the forwarding logic to correct per-tenant table.
-   Table #2 .. #n -- per-tenant forwarding tables, matching destination MAC addresses and specifying output ports.

{{<note>}}The first table could be further optimized in networks using the same (overly long) access list on numerous ports. That decision could also be made dynamically by the OpenFlow controller.{{</note>}}

A typical switch would probably have to implement the first table with a TCAM. All the other tables could use the regular MAC forwarding logic (MAC forwarding table is usually orders of magnitude bigger than TCAM). Scalability problem solved.

**Summary:** Buy switches and controllers that support OpenFlow 1.3

### Revision History

2024-09-01
: Cleaned up the irrelevant hardware details. The gist of this blog post is that you need a Cartesian product of (logical) lookup tables if your forwarding hardware does not support multiple lookups into different tables.