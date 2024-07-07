---
title: "Stateful Firewall Cluster High Availability Theater"
date: 2024-04-10 07:59:00+0200
tags: [ firewall, high availability ]
ha-cluster_tag: overview
high-availability_tag: ignore
series:
- ha-cluster
---
Dmitry Perets wrote an [excellent description of how typical firewall cluster solutions implement control-plane high availability](/2024/01/bgp-graceful-restart-harmful/#2069), in particular, the routing protocol Graceful Restart feature (slightly edited):

---

Most of the HA clustering solutions for stateful firewalls that I know implement a single-brain model, where the entire cluster is seen by the outside network as a single node. The node that is currently primary runs the control plane (hence, I call it single-brain). Sessions and the forwarding plane are synchronized between the nodes.
<!--more-->
Therefore, in the event of HA failover, all the existing sessions are preserved, and user traffic can just keep flowing. You can get a subsecond failover, delayed only by failure detection (based on HA keepalives sent back-to-back between the nodes and link failure detection).

Since it is a single-brain solution, the BGP daemon runs only on the primary node. Upon HA failover, it starts from scratch on the ex-secondary (new primary). This is where Graceful Restart comes into play. It allows your peers to keep their forwarding state, believing that your HA clustering solution successfully did the same on your side. Hence, you get your Non-Stop Forwarding and don't bother the rest of your network with BGP convergence while the new HA primary re-establishes its BGP control plane.

---

Let's start with a diagram to illustrate our discussion; handwaving should be reserved for academic discussions and podcasts.

{{<ascii>}}
┌────────┐   ┌────────┐       
│   X1   │   │   X2   │  ▲    
└────┬───┘   └────┬───┘  │    
     │            │      │    
─────┼────────────┼────  │ BGP
     │            │      │    
┌────┴───┐   ┌────┴───┐  ▼    
│Firewall│   │Firewall│       
└────┬───┘   └────┬───┘  ▲    
     │            │      │    
─────┼────────────┼────  │ BGP
     │            │      │    
┌────┴───┐   ┌────┴───┐  │    
│   C1   │   │   C2   │  ▼    
└────────┘   └────────┘       
{{</ascii>}}

The two firewalls act as a single control plane. Both inside switches and outside routers have a BGP session with that single control-plane instance.

The firewalls also share an inside- and an outside IP address, forcing us to build a VLAN linking the two firewall boxes and a pair of switches (or routers). Am I allowed to mention that a single VLAN is also a single failure domain?

The "single firewall control plane that is restarted on the other instance" idea results in a single point of failure with non-negligible downtime, which makes the Graceful Restart the only viable option for non-stop forwarding.

Now that we know what we're talking about, let's analyze the various failure scenarios:

* **Firewall power supply failure.** The firewall cluster can deal with that.
* **Firewall forwarding table corruption.** The only people who might be able to comment on the impact of this one are the engineers writing the code. From an end-user perspective, we might be left with an expensive Schroedinger packet destroyer.
* **Session table corruption.** See the previous bullet.
* **Firewall software failure.** See the previous bullet. However, I have seen redundant clusters that failed to switch over the control-plane functionality when the primary node refused to die completely.
* **LAN failure.** Dig deep into the firewall documentation to see how it reacts to keepalive failure on one of the interfaces, and hope the code works as described.

In any case, the only failure scenario this design protects us against is a hardware failure. That approach might have been the right choice in the 1980s (I've seen my share of failed power supplies), but I'm pretty sure we're seeing more software crashes and weird, hard-to-explain bugs in the 2020s than power supply failures.

As always, software developers believe in the quality of their code, create solutions that cope with what they could imagine other people's problems to be[^CD], and keep solving yesterday's problems.

[^CD]: That's why crappy software developers use hardcoded IP addresses. They have no problem imagining DNS failing more often than their code.

Is there an alternative? Of course. Don't believe in the magic of firewall clusters. Instead, use two independent firewalls and run BGP with them. Even better, run BGP across them to determine which one has a working data plane.

Want to know more? Read the [BGP as a High-Availability Protocol](/kb/BGPHighAvailability/) article by Nicola Modena.

