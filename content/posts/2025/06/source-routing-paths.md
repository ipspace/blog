---
date: 2025-06-13 08:10:00+02:00
networking-fundamentals_tag: switching
tags:
- networking fundamentals
title: Finding Source Routing Paths
comment: |
  In September 2020, I created the [Finding Paths Across the Network](https://my.ipspace.net/bin/get/Net101/SW4%20-%20Finding%20Paths%20Across%20the%20Network.mp4?doccode=Net101) video as part of the [How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work). This blog post covers the second half of that video. I used Whisper to generate a raw transcript, cleaned it up with ChatGPT, and restructured it to make it easier to read.
---
In the [previous blog post](/2025/06/finding-paths-across-network/), we discussed the generic steps that network devices (or a centralized controller) must take to discover paths across a network. Today, we'll see how these principles are applied in *source routing*, one of the [three main ways to move packets across a network](/2025/05/forwarding-packets-across-network/).

**Brief recap:** In source routing, the sender has to specify the (loose or strict) path a packet should take across the network. The sender thus needs a mechanism to determine that path, and as always, there are numerous solutions to this challenge. We'll explore a few of them, using the sample topology shown in the following diagram.
<!--more-->
{{<figure src="/2025/06/np-source-routing.png">}}
### Controller-Based Source Routing

Software-defined networking (SDN) reinvented the concept of a centralized controller (now called **SDN controller**) connected to network devices. In an **OpenFlow**-based setup, this controller intercepts control plane traffic. For instance, when X sends an ARP request, it gets intercepted by the SDN controller.

At that point, the controller knows three things:

-   The IP address of X,
-   The MAC address of X,
-   The port of switch A that can be used to reach X.

With that information, the controller can push path information to all nodes. For example, the controller could install the path toward Y as "B → E → Y" in A.

**Segment Routing with Path Computation Elements (PCE)** works in a similar way, but uses a combination of traditional routing protocols and controller-based path setup.

The traditional routing protocols (IS-IS or OSPF) are used to assign labels to nodes, and the PCE controller collects the topology information, calculates the end-to-end paths, and installs label stacks (or IPv6 headers) in the forwarding tables of the edge nodes (for more details, watch the [PCEP and BGP-LS Deep Dive](https://my.ipspace.net/bin/list?id=PCEP) webinar)

### Virtual Circuit Establishment in the Old Days

Before someone decided to call their contraption Software Defined, the devices now pretending to be *SDN controllers* were called **network management systems** (NMS). However, in most cases, the only interaction with those systems was an out-of-band management-plane protocol:

* You’d fill out a form
* You'd fax that form to your provider
* There might be a contract to be negotiated and signed
* Months later, someone at the NMS GUI would click through and provision your circuit. That’s how **Frame Relay** and **ATM** worked.

Some networks allowed dynamic requests for circuits—these were called **switched virtual circuits**, as opposed to **permanent virtual circuits** set up by the NMS. Switched circuits existed in **X.25**, **ATM**, and still exist in **MPLS TE** today.

But again, the same challenges apply:

* Path failures must be detected.
* Failures must be reported back to the NMS, which has to recalculate the paths
* A large number of virtual circuits failing at once—say, due to a core link going down—can overwhelm the control plane.

### Source Route Bridging

**Source route bridging** (the technology used to implement Token Ring networks) used *discovery frames*. Let's say X wants to communicate with Y but has no idea where Y is.

{{<note info>}}
Keep in mind, this is **Token Ring**, so all those lines are actually rings. Bridges connect the rings, and both have identifying numbers.
{{</note>}}

X sends a *discovery frame* (a special unicast frame) to Y. Every bridge intercepts the frame, adds its ID, and forwards it along.

* A receives the frame, adds its info, and sends it to B.
* B adds its info and sends it to E.
* E adds its info and forwards the frame.

A similar process happens along alternative paths. Eventually, Y receives multiple discovery frames—whichever arrives first likely came through the least congested path. This automatically gives a measurement of current network conditions.

The discovery frame includes the full return path, so Y can reply to X using the accumulated return path. When X receives the reply, it sees the path, reverses it, and uses it for future packets. Every frame from X to Y now includes a **Routing Information Field (RIF)**, listing the sequence of bridges. The same goes for the return path from Y to X.

The SRB sounds like a great idea, but it had no built-in mechanism to detect failures. If something failed along the path from X to Y, all the subsequent packets from X to Y would be dropped. Eventually, X would time out, panic, and start sending discovery frames again to locate Y and reestablish the path.

### Segment Routing

In a controller-less **Segment Routing** (SR), all nodes participate in a core routing protocol like **OSPF** or **IS-IS**. Each node advertises a node label (Segment Identifier -- SID) and optional interface and prefix labels. So, if you want to send packets from X to Y through A → C → D → E, you just collect the labels and prepend a label stack to the packet. Done.

SR is also quite effective in handling failures, as it relies on the underlying routing protocol to detect the failure and recalculate the underlying topology. X can then recalculate its label stack and adjust its path to something like A → B → E.

### MPLS Traffic Engineering (MPLS/TE)

In **MPLS TE**, X uses a signaling protocol (RSVP) to establish a unidirectional virtual circuit (often referred to as a tunnel) to Y, using the information provided by an underlying routing protocol (most often IS-IS or OSPF with TE extensions). Alternatively, a PCE controller can calculate the path from X to Y and tell X what path to use in its RSVP request.

If a link fails, the downstream node sends an error message: “Tunnel failed.” X then has to decide what to do next. X could recalculate the path or rely on a PCE SDN controller that must intervene and push new instructions to X. Until that happens, the network stalls—packets are lost or delayed.

In traditional MPLS TE, X reestablishes the tunnel by sending a new RSVP request. It typically works—unless you’re dealing with a large, overprovisioned network full of ~~spaghetti~~ tunnels. That’s what happened (or so I was told) to an Asian service provider during an earthquake. Several core links failed, tearing down thousands of tunnels between end nodes. That triggered thousands of error messages and caused all source nodes to panic, attempting to reestablish tunnels simultaneously.

The resulting control plane overload caused nodes to crash or ignore the traffic. The network was effectively down for a day until things stabilized.
