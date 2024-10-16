---
title: "Comparing IP and CLNP: Finding Adjacent Nodes"
date: 2024-10-17 08:10:00+0100
tags: [ networking fundamentals ]
comment: |
  In early 2020 I created the _[Comparing IP and CLNP Addressing](https://my.ipspace.net/bin/get/Net101/NA3.2%20-%20Comparing%20IP%20and%20CLNP%20Addressing.mp4?doccode=Net101)_ video as part of the _[How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work)_. This blog post is an edited transcript of the first part of that video.
---
Now that we know a bit more about [addresses in a networking stack](/2023/09/addresses-in-network-stack/) (read the whole series) and [why CLNP uses node addresses while TCP/IP uses interface addresses](/2024/02/interface-node-addresses/), let's see how they solve common addressing problems like finding adjacent nodes.

Let's start with the elephant in the room: how do you know whether you can reach a host you want to communicate with directly? In the following diagram, how does A know whether B is sitting next to it?
<!--more-->
{{<figure src="/2024/10/addr-find-adjacent-nodes.png">}}
In TCP IP, the answer is trivial. Every subnet has something called the subnet mask. So you take your IP address, you take the destination IP address, you take the subnet mask, and you clear the remaining bits. Then, you compare whether your subnet and destination subnet match, and if they do, you know you can reach the destination IP address directly; both hosts must be connected to the same data link layer segment.

{{<note info>}}The process is a bit more convoluted in IPv6. Routers can advertise additional on-link IPv6 prefixes in their Router Advertisement messages, and a host has to consider them all while performing the above checks. It's also legal to omit the on-link prefixes from the Router Advertisement messages, in which case a well-behaved IPv6 host has to send all the packets to the first-hop router.{{</note>}}

Next question: How do we reach the destination IP address? We need to use a protocol that (given the destination IP address) will find the destination MAC address, which we can use in the layer-2 encapsulation header to send a packet to the destination host. IPv4 uses ARP on LAN media to get that done, and IPv6 uses Neighbor Discover (ND, part of ICMPv6)[^AE].

[^AE]: In the past, we used static configuration and other ARP-like protocols, but in 2024, almost everything looks like LAN media.

You don't need ARP or ND on a layer-2 point-to-point link[^RARE] because you already know the data link layer address to use for the other guy. For example, in the [Early Data-Link Layer Addressing](/2023/10/data-link-addressing/) blog post, we mentioned that the destination MAC address on a PPP link is always 0xFF (the broadcast address). As we know the destination MAC address, we don't do ARP on PPP or any other point-to-point serial link[^MASL] (IPv6 might still perform Neighbor Discovery).

[^RARE]: True point-to-point links are rare in the days of ubiquitous Ethernet and WiFi. What looks like a point-to-point link might be an Ethernet LAN segment that still needs MAC addresses to work correctly.

[^MASL]: Switched WAN technologies like X.25, Frame Relay, and ATM used a different mechanism. On X.25 and ATM, we had to specify the mappings manually. On Frame Relay, once you have configured a virtual circuit (DLCI), you can figure out the remote router's IP address with Inverse ARP. If you ever encounter these technologies outside a museum or a historical recreation, it might be time to switch jobs.

OSI (CLNP) took a completely different approach than TCP/IP because the CLNP network address (NSAP -- Network Services Access Point) belongs to a node, and a node could have multiple interfaces. You can't use part of the destination network address to determine whether the node is adjacent to you. To solve that problem, every CLNP node sends hello messages -- hosts send End-System Hellos[^OTH](ESH), and routers send Intermediate System Hellos[^OTR](ISH) -- advertising their NSAPs.

[^OTH]: OSI terminology for hosts

[^OTR]: OSI terminology for routers

Each CLNP node on a LAN segment would listen to all hello messages other nodes send on that segment and build a cache of adjacent NSAP addresses. In our example, A would know that B is adjacent because it would see the ESH message from B. Likewise, assuming there's another link connecting A and D (see the following diagram), A would know that D is adjacent (but on a different interface) after it would receive an end system hello from D. Similarly, B would know that D is not adjacent because it has never seen an ESH from D.

{{<figure src="/2024/10/addr-adding-node-d.jpg" caption="Adding another link and another node to the CLNP network">}}

Finally, to make forwarding decisions and send packets, we need more information in the neighbor cache than the neighbor NSAPs. As you see in the case of host A, the neighbor cache entries must contain outgoing interfaces. We also need the destination MAC addresses, which are trivial to collect. The Hello messages contain the MAC address of the sender, and the CLNP nodes can use them to build the mapping between the adjacent NSAPs and layer-2 addresses.

Effectively, the CLNP neighbor cache is functionally equivalent to host routes pointing to interfaces and MAC addresses. 

### Off-Topic: ARP and Virtual Machine Mobility

In data centers using server virtualization, we often deal with virtual machines that move willy-nilly across the data center fabric. It would be convenient if the virtual machine could advertise itself after being moved so that everyone would know that the VM MAC address is now elsewhere. That would work out of the box with CLNP, but unfortunately, we don't have a similar mechanism in IP.

IP hosts have a mechanism called *gratuitous ARP*, where a host sends a broadcast ARP response announcing a new mapping between its IP address and MAC address (hosts use that when their IP- or MAC address changes). Still, that's not the same as the periodic host-generated hello messages.

Many hypervisors track the virtual machine MAC- and IP addresses and send fake gratuitous ARPs after a VM has moved, but IP was not designed to be used that way. Virtualization vendors that tried to keep their investment in the networking stack to an absolute minimum (VMware comes to mind) are not listening to ARP requests and replies. Thus, they cannot generate gratuitous ARPs when the VM is moved.

However, VMware figured there was another totally
obsolete protocol called Reverse ARP (defined in an [RFC from 1984](https://datatracker.ietf.org/doc/html/rfc903) that nobody has used for decades. RARP packets have only MAC addresses but no IP addresses, and as VMware ESXi knows the VM MAC address, it can generate an RARP packet on behalf of the VM after a VM has moved.