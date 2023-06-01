---
title: "Source IP Address in Multicast Packets"
date: 2023-06-01 07:22:00
tags: [ IP routing, AI ]
AI_tag: kick
---
One of my readers sent me this (paraphrased) question:

> What I have seen in my network are multicast packets with the IP source address set to 0.0.0.0 and source port set to 0. Is that considered acceptable? Could I use a multicast IP address as a source address?

**TL&DR**: **** NO!!!

It also seemed like a good question to test ChatGPT, and this time it did a pretty good job.
<!--more-->
---

> What should be the source IP address in an IPv4 multicast packet?

In an IPv4 multicast packet, the source IP address should be the IP address of the device (sender) that is generating the multicast traffic. This address should be a valid unicast IP address assigned to the sender's network interface. The source IP address should not be a multicast address (i.e., in the range of 224.0.0.0 to 239.255.255.255), as multicast addresses are reserved for destination (group) addresses in multicast communication.

In summary, the source IP address in an IPv4 multicast packet should be the unicast IP address of the sender, while the destination IP address should be a valid multicast address representing the multicast group to which the packet is being sent.

> Why can't I use a multicast IP address as the source IP address?

Using a multicast IP address as the source IP address in a multicast packet is not allowed for several reasons:

1.  Address ambiguity: Multicast addresses are used to identify multicast groups, not individual devices. If a multicast address were used as the source IP address, it would create ambiguity, as multiple devices could be associated with that address. The receiving devices wouldn't be able to identify the specific sender or respond to the sender correctly.
2.  Routing and forwarding issues: Network devices, such as routers and switches, are designed to handle multicast traffic based on destination multicast addresses. Using a multicast address as the source address would likely cause routing and forwarding issues, as network devices would not know how to handle such packets correctly.
3.  Protocol design: IP multicast protocols, such as Internet Group Management Protocol (IGMP) and Protocol Independent Multicast (PIM), are designed with the assumption that source addresses are unicast IP addresses. Using multicast addresses as source IP addresses could lead to unexpected behavior or errors in these protocols.
4.  Security concerns: Allowing multicast IP addresses as source addresses could enable potential spoofing attacks or create other security vulnerabilities.

By using unicast IP addresses as source addresses in multicast packets, these issues are avoided, and the IP multicast system can function correctly and efficiently.

> Can I use IP address 0.0.0.0 as the source IP address?

Using the IP address 0.0.0.0 as the source IP address in a packet is generally not recommended for normal communication. The address 0.0.0.0 is a special reserved address known as the "unspecified address," and it has a particular meaning in specific contexts:

1.  When a device is first initializing its IP stack and does not yet have a valid IP address assigned, it may use 0.0.0.0 as the source IP address in specific situations, such as DHCP (Dynamic Host Configuration Protocol) requests. In this case, the device is essentially saying, "I don't have an IP address yet, please provide me one."
2.  In some programming or system contexts, 0.0.0.0 is used as a wildcard to indicate that a server should listen on all available network interfaces and IP addresses.

For regular communication, using 0.0.0.0 as the source IP address is not appropriate, as it doesn't uniquely identify the sender. Other devices on the network will not be able to interpret the source of the packet or respond to it correctly. Instead, you should use a valid unicast IP address assigned to the sender's network interface as the source IP address.

---

The only thing it missed is the Reverse Path Forwarding (RPF) check -- when deciding where to forward a multicast packet, an IP router will never send it onto the interfaces that can be used to reach the sender, thus breaking forwarding loops more effectively than blocking the links[^MU]. An IP router will also drop incoming multicast packets if the source IP address of the incoming packet cannot be reached through the incoming interface.

The RPF check effectively blocks the propagation of IP multicast packets with the source IP address set to 0.0.0.0 beyond the first router[^DR], which might explain why an overly smart developer might have decided to use them when trying to solve the "_how do we make sure this stuff never escapes into the wild_" challenge instead of figuring out how to use MAC-level multicasts[^DN].

[^MU]: At least that's my vague understanding of how IP multicast forwarding works based on the few times I had to cram just enough multicast information into my overloaded brains to pass the CCIE recertification exam.

[^DR]: Unless (A) the default route points to the incoming interface and (B) the packet forwarding code in the router does not come to the conclusion that the sender is intoxicated and should be ignored.

[^DN]: The correct way sane people solved this challenge since early 1980s.

Anyway, one has to wonder what makes people ask such weird questions. In this case, my reader noticed a network device sending multicast packets with all-zeroes source IP address as a heartbeat between cluster members. With that information, it wasn't hard to find a potential culprit, for example the [Checkpoint firewalls](https://community.checkpoint.com/t5/Security-Gateways/CCP-packets-sent-to-network-address-instead-of-broadcast-address/td-p/65793).

I used the following image in a blog post in 2015. Unfortunately it's equally appropriate almost a decade later. Some stupidities never change.

{{<figure src="/2015/11/s500-Enough+of+this+shit.jpg">}}

### Revision History

2023-06-01
: Rewrote the _impact of RPF check_ part of the blog post based on the [feedback from Erik Auerswald](https://blog.ipspace.net/2023/06/multicast-source-address.html#1851).