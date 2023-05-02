---
title: "Silent Hosts in EVPN Fabrics"
date: 2023-05-04 06:46:00
tags: [ EVPN, bridging ]
---
The [Dynamic MAC Learning versus EVPN](https://blog.ipspace.net/2023/04/evpn-dynamic-mac-learning.html) blog post triggered tons of interesting responses describing edge cases and vendor ~~bugs~~ implementation details, including an age-old case of silent hosts [described by Nitzan](https://blog.ipspace.net/2023/04/evpn-dynamic-mac-learning.html#1792):

> Few years ago in EVPN network, I saw drops on the multicast queue (ingress replication goes to that queue). After analyzing it we found that the root cause is vMotion (the hosts in that VLAN are silent) which starts at a very high rate before the source leaf learns the destination MAC.

I can't entirely agree with the root cause analysis, but the behavior is interesting enough to dig deeper into the details.
<!--more-->
Let's define **silent hosts** first. They are nodes that never send any traffic, so the switches cannot learn their MAC addresses and are forced to flood the traffic sent to those MAC addresses. Typical examples would be Syslog servers or traffic monitoring/inspection appliances; we'll ignore monstrosities like [Microsoft NLB](https://blog.ipspace.net/2012/02/microsoft-network-load-balancing-behind.html) for the moment.

{{<note info>}}vMotion uses TCP. The vMotion VLAN (the VLAN used for vMotion traffic) has plenty of bidirectional traffic and no silent hosts; so let's assume the comment means that the *virtual machines migrated between ESXi hosts are silent*.{{</note>}}

One would expect silent hosts to communicate with the external world in one way or another, but that won't help if they don't use the same VLAN for the outbound communication as transparent bridging uses per-VLAN MAC address tables.  

However, **vMotion should fix the problem**, not make it worse. ESXi servers [send RARP packets on behalf of the moved virtual machines](https://kb.vmware.com/s/article/90045) after completing vMotion to inform the switches that the VM MAC address has moved. Unfortunately, you could turn off the *notify switches* option making the vMotion events invisible, but that would result in traffic blackholes -- the switches would think the VM MAC address is still present on the origin ESXi server -- not flooding.

Now for the elephant in the room: **whoever is sending the traffic to a silent host must know its MAC address**. While one could use static ARP entries, we usually don't, so the senders must send ARP queries now and then, and the silent hosts must respond to them, enabling the switches to learn all the MAC addresses in the VLAN.

Time to go back to first principles: the only way to solve the *silent host* challenge is to **ensure MAC address entries time out later than ARP entries**. That's easy to do if the traffic is entering the VLAN through a router and a bit more cumbersome if you have to adjust the ARP timeouts on all hosts in the VLAN.

Fortunately, modern TCP/IP stacks use short ARP timeouts -- default value on Linux is 30 seconds (randomized into 15-45 seconds), and the kernel removes stale entries (mappings without incoming traffic) every 60 seconds. ARP entries for silent hosts should become stale almost immediately and be refreshed in approximately two minutes.

Switches and routers have a different perspective. Cisco IOS and Arista EOS still age out ARP entries in four hours; Cisco Nexus OS does it in 1500 seconds (25 minutes). No wonder we get flooding in VLANs with silent hosts.  

Back to the comment:

> The quick and ugly solution was to scan the vMotion VLAN with NMAP every few minutes so the leafs would have all of the MAC addresses in their EVPN database.

And now we know why that works (assuming the Linux host running NMAP is attached to the same VLAN): ARP entries in the Linux kernel would become stale between NMAP runs, triggering ARP requests and responses from silent hosts regardless of whether the silent hosts would answer NMAP probes.

**Long story short:** the ancient challenge often used in vendor certification written exams did not disappear just because we replaced STP with EVPN. You might get flooded traffic whenever the ARP timeouts in your network are larger than the MAC address table timeouts.

**Want to know more about EVPN?** Check out the _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_ webinar.