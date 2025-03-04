---
title: "Worth Reading: Traffic Steering into LSPs"
date: 2025-03-10 08:12:00+0100
tags: [ worth reading, MPLS, traffic engineering ]
---
You can use SR-MPLS, MPLS-TE, or an SDN controller to build virtual circuits (label-switched paths) across the network core. The controller can push the LSPs into network devices with PCEP, BGP-LU, or some sort of NETCONF/RESTCONF trickery.

Unfortunately, you're only half done once you have installed the LSPs. You still have to persuade the network devices to use them. Welcome to the confusing world of traffic steering explored in the [Loopback as a Service](https://routingcraft.net/loopback-as-a-service/) blog post by [Dmytro Shypovalov](https://routingcraft.net/contact/).

{{<jump>}}[Keep reading](https://routingcraft.net/loopback-as-a-service/){{</jump>}}