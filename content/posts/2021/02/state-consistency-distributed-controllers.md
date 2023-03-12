---
date: 2021-02-10 06:57:00+00:00
distributed-systems_tag: sdn
ha-cluster_tag: sdn
high-availability_tag: ignore
series:
- consistent-state
- ha-cluster
- distributed-systems
series_weight: 2000
subtitle: Why Can't We Have Good Things Like Partition-Resilient SDN Controllers
tags:
- SDN
- design
- high-availability
title: State Consistency in Distributed SDN Controller Clusters
---
Every now and then I get a question along the lines of "_why can't we have a distributed SDN controller (because resiliency) that would survive network partitioning?_" This time, it's not the incompetency of solution architects or programmers, but the fundamental limitations of what can be done when you want to have consistent state across a distributed system.

**TL&DR**: If your first thought was *[CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)* you're absolutely right. You can probably stop reading right now. If you have no idea what I'm talking about, maybe it's time you get fluent in distributed systems concepts after you're finished with this blog post and all the reference material linked in it. Don't know where to start? I put together a [list of resources I found useful](https://www.ipspace.net/kb/tag/distributed-systems.html).
<!--more-->
## What State Are We Talking About?

An SDN controller has to keep an awful lot of information about the current state of the network that was traditionally distributed across network devices. At the very minimum, the controller must have the *network configuration*, including edge ports, core links, VLANs, network segments, IP subnets, access control lists... (to get an idea about the scope of this challenge watch the [Cisco ACI](https://www.ipspace.net/Cisco_ACI_Deep_Dive) or [VMware NSX](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) webinars).

A controller that wants to be more than an umbrella orchestration system must also know about:

* Locations of customer MAC addresses
* Locations of customer IP addresses and ARP caches
* Routing tables
* VXLAN endpoints (VTEPs) and mapping of customer MAC addresses to VTEPs
* Dynamic security group membership (fancy name for ACLs with object lists updated in real time)
* Packet filters deployed at the network edge (because an edge device could belong to one or more security groups with dynamic membership)

A controller providing centralized control plane would need information about:

* STP state of every edge port
* LLDP neighbors
* LACP sessions
* Routing protocol adjacencies
* Routing protocol topology databases

A controller providing network services could also have to deal with:

* DNS mappings (static or dynamic)
* DHCP mappings (static or dynamic)

Finally, someone could be brave enough to keep NAT or load balancing state in a controller cluster. I wish them luck, and don't want to know how badly that will end.

## Consistency Requirements

Some of the state managed by an SDN controller cluster is long-lived (configuration), some of it is ephemeral (MAC address location, routing information), and some of it needs strict consistency guarantees (dynamic DHCP mappings).

MAC address location or routing tables have to be *[eventually consistent](https://en.wikipedia.org/wiki/Eventual_consistency)*:

* They may change at any time in any place
* The change has to be propagated in some reasonable time
* The interim mess we're creating with that approach will result in packet drops or microloops
* We don't care about that and let the higher-level protocols deal with our mistakes.

In most cases, we use *last writer wins* approach when updating the *eventually consistent* state (wherever the MAC address was seen last is probably where it's now).

Configuration information could be *eventually consistent* if you want to deal with irate users (similar to what happens when two CLI jockeys work on the same device). Most systems prefer *[sequential consistency](https://en.wikipedia.org/wiki/Sequential_consistency)* of configuration changes, with some systems like Junos offering all-or-nothing *[atomic consistency](https://en.wikipedia.org/wiki/Atomicity_(database_systems))*

* Configuration changes are made in a well-defined sequential order, so we don't have to deal with concurrent updates or [edit (merge) conflicts](https://en.wikipedia.org/wiki/Edit_conflict).
* The changes are *eventually* propagated and implemented across the network

Finally, some state like dynamic DHCP mappings MUST be *[strictly consistent](https://en.wikipedia.org/wiki/Consistency_model#Strict_consistency)*. You cannot give the same IP address to two clients and hope they will eventually figure it out.

## Implementing Eventually Consistent State

State that can be *eventually consistent* can be stored into an *eventually consistent distributed database* (sometimes also known as OSPF topology database... just kidding ;) 

We're also not concerned too much with the order of changes. We hope to have timestamps in place that would tell everyone which change is the most recent, and are OK with the last change overwriting whatever previous changes were made to the same data.

A typical example of this approach is OSPF topology database:

* Changes are made by all devices in the network. 
* The changes are eventually propagated across the whole network.
* Any object (LSA) could be modified multiple times, and the LS Sequence Number is used to indicate which change was the most recent one.

Admittedly, an LSA is always changed by the same device, which makes the *[ordering of events](https://en.wikipedia.org/wiki/Lamport_timestamp)* problem trivial.

MAC address location in EVPN is already a bit harder to tackle. EVPN supports MAC mobility, so we can expect multiple PE-devices to see the same MAC address at different times -- a typical case of multiple writers in a *last writer wins* distributed system. 

A seemingly trivial way to figure out order of updates would be to use timestamps and synchronized clocks on all devices... but perfect clock synchronization usually turns out to be a nightmare, so EVPN settled for a simple counter carried in *MAC mobility extended BGP community*. Whenever a PE-device encounters a local MAC address that has already been advertised by another PE-device it increments the sequence number and advertises the new MAC address mapping. Of course it's possible for two devices to get into a chicken fight when both of them see the same local MAC address; apart from [a few guidelines](https://tools.ietf.org/html/rfc7432#section-15.1), RFC 7432 left the details of that interesting corner case as an exercise for the implementers.

## Implementing Sequentially Consistent State

Some SDN controllers implement sequentially consistent state with *update in a central place* approach:

* Changes to any bit of information can be made only by one of the controller nodes;
* Those changes are eventually propagated to all other nodes.
* Some controller clusters use *[shards](https://en.wikipedia.org/wiki/Shard_(database_architecture))* for performance reasons -- different bits of information are "owned" by different cluster members.

If you're thinking about *write* and *read* database replicas with *asynchronous* or *[lazy replication](https://en.wikipedia.org/wiki/Optimistic_replication)*, you're not far off the mark.

A [consensus protocol](https://en.wikipedia.org/wiki/Consensus_(computer_science)#Some_consensus_protocols) like [Paxos](https://en.wikipedia.org/wiki/Paxos_(computer_science)) or [Raft](https://en.wikipedia.org/wiki/Raft_(algorithm)) is another commonly used alternative.

## Implement Strictly Consistent State

Strictly consistent state is typically implemented with a transactional ([ACID](https://en.wikipedia.org/wiki/ACID)) database, although a consensus protocol is also a viable alternative.

Distributed transactional databases are hard to implement and scale (see [two-phase commit](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)). It's more convenient to use lazy replication for backup purposes and make all reads against the *write* replica to ensure strict consistency, yet again using shards if needed to improve performance.

Alternatively, you could avoid this problem altogether by not implementing functionality that requires strict consistency. For example, NSX-T Federation implements static DHCP mappings (configuration change requiring *sequential consistency*) instead of dynamic DHCP mappings (which would require *strict* consistency).

## Why Does It Matter?

We started with "_why can't we have a distributed SDN controller (because resiliency) that would survive network partitioning?_".

**Long story short** (because this blog post is already way too long): systems requiring sequential or strict consistency cannot also have *availability* and *partition tolerance* (aka [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)). They either cannot survive a network partition (bad idea) or cannot be fully available during the partition.
