---
date: 2020-12-02 07:13:00+00:00
networking-fundamentals_tag: deep
tags:
- switching
- data center
- networking fundamentals
title: Chasing CRC Errors in a Data Center Fabric
---
One of my readers encountered an interesting problem when upgrading a data center fabric to 100 Gbps leaf-to-spine links:

* They installed new fiber cables and SFPs;
* Everything looked great... until someone started complaining about application performance problems.
* Nothing else has changed, so the culprit must have been the network upgrade.
* A closer look at monitoring data revealed CRC errors on every leaf switch. Obviously something was badly wrong with the whole batch of SFPs.

Fortunately, my reader took a closer look at the data before they requested a wholesale replacement... and spotted an interesting pattern:
<!--more-->

* All leaf switches _apart from one_ had _input_ CRC errors on _one of the uplinks_ but not the other. What if there was a problem with the spine switch?
* The spine switch on the other side of the "faulty" uplinks had _input_ CRC errors on the link toward the one leaf switch with no CRC errors, and _output_ CRC errors on all other links.

{{<figure src="/2020/12/DC_CRC_Observations.png" caption="Weird pattern of CRC errors">}}

Knowing Ethernet fundamentals, one should ask a naive question at this point: "_isn't CRC checked when receiving packets and how could you get one on the transmit side?_" Fortunately my reader also understood the behavior of cut-through switching and quickly identified what was really going on:

* The one link with no errors on the leaf switch had a bad cable, resulting in CRC errors on the spine switch, but no errors in the other direction;
* The spine switch was configured for cut-through switching, so it propagated the corrupted packets, and _stomped the CRC on egress ports_ to prevent the downstream devices from accepting the packet... increasing the _transmit CRC error_ counter at the same time.
* Downstream leaf switches received corrupted packets originally sent over the faulty link and increased their _receive CRC error_ counters.

{{<figure src="/2020/12/DC_CRC_Errors.png" caption="Fabric-wide errors caused by a single faulty transceiver">}}

They replaced the faulty cable, the errors disappeared, and life was good. As for the original performance problem... maybe it wasn't the network ;)

For more details watch the *[Store-and-Forward versus Cut-Through Switching](https://my.ipspace.net/bin/get/Net101/SW6%20-%20Store-and-Forward%20and%20Cut-Through%20Switching.mp4)* video in *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar and read [this excellent article](http://thenetworksherpa.com/cut-through-corruption-and-crc-stomping/) by John Harrington.